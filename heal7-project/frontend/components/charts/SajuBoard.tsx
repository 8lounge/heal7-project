'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { SajuPillar } from '@/types/saju';

interface SajuBoardProps {
  pillars: {
    년주: SajuPillar;
    월주: SajuPillar;
    일주: SajuPillar;
    시주: SajuPillar;
  };
  className?: string;
  showHanja?: boolean;
}

const PILLAR_NAMES = {
  년주: '年柱',
  월주: '月柱', 
  일주: '日柱',
  시주: '時柱',
};

const PILLAR_DESCRIPTIONS = {
  년주: '조상, 유년기',
  월주: '부모, 청년기',
  일주: '본인, 배우자',
  시주: '자식, 노년기',
};

// 천간 오행 매핑
const CHEONGAN_WUXING: { [key: string]: string } = {
  '갑': '목', '을': '목',
  '병': '화', '정': '화', 
  '무': '토', '기': '토',
  '경': '금', '신': '금',
  '임': '수', '계': '수',
};

// 지지 오행 매핑
const JIJI_WUXING: { [key: string]: string } = {
  '자': '수', '축': '토', '인': '목', '묘': '목',
  '진': '토', '사': '화', '오': '화', '미': '토', 
  '신': '금', '유': '금', '술': '토', '해': '수',
};

function getWuxingVariant(wuxing: string) {
  const mapping: { [key: string]: string } = {
    '목': 'wood',
    '화': 'fire',
    '토': 'earth', 
    '금': 'metal',
    '수': 'water',
  };
  return mapping[wuxing] || 'default';
}

interface PillarCardProps {
  pillar: SajuPillar;
  name: string;
  hanja: string;
  description: string;
  showHanja: boolean;
  isMainPillar?: boolean;
}

function PillarCard({ pillar, name, hanja, description, showHanja, isMainPillar = false }: PillarCardProps) {
  const cheongangWuxing = CHEONGAN_WUXING[pillar.천간] || '';
  const jijiWuxing = JIJI_WUXING[pillar.지지] || '';

  return (
    <div className={`pillar-card ${isMainPillar ? 'ring-2 ring-purple-500/50' : ''}`}>
      {/* 기둥 이름 */}
      <div className="text-center mb-3">
        <div className="text-slate-300 font-medium text-sm">{name}</div>
        {showHanja && (
          <div className="hanja text-slate-400 text-xs">{hanja}</div>
        )}
        <div className="text-xs text-slate-500 mt-1">{description}</div>
      </div>

      {/* 천간 */}
      <div className="space-y-2">
        <div className="text-center">
          <div className="text-lg font-bold text-slate-200 mb-1">
            {showHanja ? pillar.한자천간 : pillar.천간}
          </div>
          <Badge variant={getWuxingVariant(cheongangWuxing) as any} className="text-xs">
            {cheongangWuxing}
          </Badge>
        </div>

        {/* 구분선 */}
        <div className="border-t border-slate-600/50"></div>

        {/* 지지 */}
        <div className="text-center">
          <div className="text-lg font-bold text-slate-200 mb-1">
            {showHanja ? pillar.한자지지 : pillar.지지}
          </div>
          <Badge variant={getWuxingVariant(jijiWuxing) as any} className="text-xs">
            {jijiWuxing}
          </Badge>
        </div>
      </div>
    </div>
  );
}

export function SajuBoard({ pillars, className, showHanja = true }: SajuBoardProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-4">
        <CardTitle className="text-slate-200 flex items-center gap-2">
          사주팔자 (四柱八字)
        </CardTitle>
        <div className="text-sm text-slate-400">
          출생년월일시를 바탕으로 한 4개의 기둥
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(pillars).map(([key, pillar]) => (
            <PillarCard
              key={key}
              pillar={pillar}
              name={key}
              hanja={PILLAR_NAMES[key as keyof typeof PILLAR_NAMES]}
              description={PILLAR_DESCRIPTIONS[key as keyof typeof PILLAR_DESCRIPTIONS]}
              showHanja={showHanja}
              isMainPillar={key === '일주'} // 일주가 가장 중요
            />
          ))}
        </div>

        {/* 설명 */}
        <div className="mt-6 p-4 bg-slate-800/30 rounded-lg">
          <h4 className="text-slate-200 font-medium mb-2">사주 해석 가이드</h4>
          <div className="space-y-1 text-xs text-slate-400">
            <div>• <strong>일주</strong>: 본인의 성격과 운명을 나타내는 가장 중요한 기둥</div>
            <div>• <strong>년주</strong>: 조상 덕과 유년기 환경</div>
            <div>• <strong>월주</strong>: 부모와 청년기, 사회적 관계</div>
            <div>• <strong>시주</strong>: 자식과 노년기, 미래</div>
          </div>
        </div>

        {/* 오행 분포 요약 */}
        <div className="mt-4">
          <h4 className="text-slate-300 font-medium mb-2 text-sm">기둥별 오행 분포</h4>
          <div className="flex flex-wrap gap-1">
            {Object.entries(pillars).map(([pillarName, pillar]) => {
              const cheongangWuxing = CHEONGAN_WUXING[pillar.천간];
              const jijiWuxing = JIJI_WUXING[pillar.지지];
              
              return (
                <div key={pillarName} className="flex gap-1">
                  <Badge variant={getWuxingVariant(cheongangWuxing) as any} className="text-xs">
                    {pillar.천간}({cheongangWuxing})
                  </Badge>
                  <Badge variant={getWuxingVariant(jijiWuxing) as any} className="text-xs">
                    {pillar.지지}({jijiWuxing})
                  </Badge>
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}