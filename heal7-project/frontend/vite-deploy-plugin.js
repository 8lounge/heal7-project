import { exec } from 'child_process';
import { promisify } from 'util';
import { existsSync } from 'fs';

const execAsync = promisify(exec);

export function deployPlugin(options = {}) {
  const {
    deployPath = '/var/www/heal7.com/',
    backupDir = '/var/www/backups/',
    reloadNginx = true,
    backup = true,
    dryRun = false
  } = options;

  return {
    name: 'vite-rsync-deploy',
    closeBundle: async () => {
      try {
        console.log('🚀 Starting rsync deployment...');
        
        // dist 폴더 존재 확인
        if (!existsSync('dist')) {
          throw new Error('dist folder not found');
        }
        
        // 백업 디렉토리 생성
        if (backup) {
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
          const backupPath = `${backupDir}heal7.com-${timestamp}/`;
          await execAsync(`sudo mkdir -p ${backupDir}`);
          console.log('📁 Backup directory prepared');
        }
        
        // rsync 옵션 구성
        const rsyncOptions = [
          '-av',                    // archive + verbose
          '--delete',              // 대상에서 삭제된 파일들 제거
          '--exclude=.git',        // git 폴더 제외
          '--exclude=node_modules', // node_modules 제외
          ...(backup ? [
            '--backup',
            `--backup-dir=${backupDir}heal7.com-$(date +%Y%m%d_%H%M%S)`
          ] : []),
          ...(dryRun ? ['--dry-run'] : [])
        ].join(' ');
        
        // rsync 실행
        const rsyncCmd = `rsync ${rsyncOptions} dist/ ${deployPath}`;
        console.log('📦 Running rsync:', rsyncCmd);
        
        const { stdout, stderr } = await execAsync(rsyncCmd);
        if (stdout) console.log('📤 Rsync output:', stdout);
        if (stderr) console.warn('⚠️  Rsync warnings:', stderr);
        
        console.log('✅ Files synced successfully');
        
        // 권한 설정
        await execAsync(`sudo chown -R www-data:www-data ${deployPath}`);
        await execAsync(`sudo chmod -R 755 ${deployPath}`);
        console.log('🔐 Permissions updated');
        
        // Nginx 설정 테스트
        if (reloadNginx) {
          try {
            await execAsync('sudo nginx -t');
            console.log('✅ Nginx config test passed');
            
            await execAsync('sudo systemctl reload nginx');
            console.log('🔄 Nginx reloaded');
          } catch (nginxError) {
            console.error('❌ Nginx reload failed:', nginxError);
            throw nginxError;
          }
        }
        
        // 배포 완료 검증
        try {
          const { stdout: curlOutput } = await execAsync('curl -I http://localhost:80 2>/dev/null | head -1');
          console.log('🌐 Service status:', curlOutput.trim());
        } catch (e) {
          console.warn('⚠️  Could not verify service status');
        }
        
        console.log('🎉 Deployment completed successfully!');
      } catch (error) {
        console.error('❌ Deployment failed:', error.message);
        process.exit(1);
      }
    }
  };
}