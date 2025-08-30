declare module './vite-deploy-plugin.js' {
  export function deployPlugin(options?: {
    deployPath?: string;
    backupDir?: string;
    reloadNginx?: boolean;
    backup?: boolean;
    dryRun?: boolean;
  }): any;
}