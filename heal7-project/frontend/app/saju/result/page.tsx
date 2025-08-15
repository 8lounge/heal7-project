'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Download, Share2, RefreshCw } from 'lucide-react';
import { ModernSajuLayout } from '@/components/layouts/ModernSajuLayout';
import { SajuResult } from '@/types/saju';
import { useSajuStore } from '@/stores/saju-store';

// 임시 샘플 데이터 (실제 API 연동 전까지 사용)
const SAMPLE_SAJU_RESULT: SajuResult = {
  사주: {
    년주: { 천간: '갑', 지지: '인', 한자천간: '甲', 한자지지: '寅' },
    월주: { 천간: '을', 지지: '묘', 한자천간: '乙', 한자지지: '卯' },
    일주: { 천간: '병', 지지: '진', 한자천간: '丙', 한자지지: '辰' },
    시주: { 천간: '정', 지지: '사', 한자천간: '丁', 한자지지: '巳' }
  },
  오행분석: {
    목: 4,
    화: 3,
    토: 2,
    금: 1,
    수: 2
  },
  십신분석: {
    비겁: 2,
    식상: 3,
    재성: 2,
    관살: 1,
    인성: 4
  },
  격국: '정관격',
  대운: [],
  세운: [],
  해석: {
    성격: '적극적이고 도전정신이 강한 성격입니다.',
    재물: '재물운이 좋아 사업 성공 가능성이 높습니다.',
    건강: '건강에 유의하며 규칙적인 생활이 필요합니다.',
    관계: '인간관계가 원만하고 리더십을 발휘할 수 있습니다.'
  },
  계산정보: {
    엔진: 'saju_system_v5',
    계산시간: new Date().toISOString(),
    정확도: 95
  }
};

function ResultContent() {
  const searchParams = useSearchParams();
  const { currentResult, currentInput } = useSajuStore();
  const [result, setResult] = useState<SajuResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // URL 파라미터에서 데이터 복원 또는 스토어에서 가져오기
    const name = searchParams.get('name');
    const date = searchParams.get('date');
    const time = searchParams.get('time');
    
    if (currentResult) {
      setResult(currentResult);
      setLoading(false);
    } else if (name && date) {
      // API 호출하여 결과 가져오기
      fetchSajuResult(name, date, time);
    } else {
      // 샘플 데이터 사용
      setTimeout(() => {
        setResult(SAMPLE_SAJU_RESULT);
        setLoading(false);
      }, 1000);
    }
  }, [searchParams, currentResult]);

  const fetchSajuResult = async (name: string, date: string, time?: string | null) => {
    try {
      // 실제 API 호출 로직
      const response = await fetch('/api/saju/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          date,
          time: time || '12:00'
        })
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        // API 실패시 샘플 데이터 사용
        setResult(SAMPLE_SAJU_RESULT);
      }
    } catch (error) {
      console.error('사주 계산 오류:', error);
      // 오류 발생시 샘플 데이터 사용
      setResult(SAMPLE_SAJU_RESULT);
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    if (!result || !currentInput) return;

    const shareData = {
      title: `${currentInput.name}님의 사주 분석 결과`,
      text: `HEAL7 사주에서 계산한 정밀 사주 분석 결과입니다.`,
      url: window.location.href
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        // Fallback: 클립보드에 URL 복사
        await navigator.clipboard.writeText(window.location.href);
        alert('링크가 클립보드에 복사되었습니다.');
      }
    } catch (error) {
      console.error('공유 실패:', error);
    }
  };

  const handleDownload = () => {
    if (!result || !currentInput) return;

    const resultData = {
      name: currentInput.name,
      birthDate: `${currentInput.birth.year}-${currentInput.birth.month}-${currentInput.birth.day}`,
      birthTime: `${currentInput.birth.hour}:${currentInput.birth.minute}`,
      result: result,
      generatedAt: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(resultData, null, 2)], {
      type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentInput.name}_사주분석결과.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mx-auto mb-4 flex items-center justify-center animate-spin">
            <RefreshCw className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-xl font-medium text-slate-200 mb-2">사주 분석 중...</h2>
          <p className="text-slate-400">잠시만 기다려주세요.</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-medium text-slate-200 mb-4">결과를 불러올 수 없습니다</h2>
          <p className="text-slate-400 mb-6">다시 계산해주시기 바랍니다.</p>
          <Link href="/calculator">
            <Button variant="saju">
              다시 계산하기
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const birthInfo = currentInput ? {
    date: `${currentInput.birth.year}-${currentInput.birth.month.toString().padStart(2, '0')}-${currentInput.birth.day.toString().padStart(2, '0')}`,
    time: `${currentInput.birth.hour.toString().padStart(2, '0')}:${currentInput.birth.minute.toString().padStart(2, '0')}`,
    isLunar: false, // 향후 음력 지원시 추가
    timezone: 'Asia/Seoul'
  } : {
    date: '1990-01-01',
    time: '12:00',
    isLunar: false,
    timezone: 'Asia/Seoul'
  };

  return (
    <div className="min-h-screen">
      {/* 상단 네비게이션 */}
      <div className="sticky top-0 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700/50 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/calculator" className="flex items-center gap-2 text-slate-400 hover:text-slate-300">
                <ArrowLeft className="w-4 h-4" />
                다시 계산하기
              </Link>
              {currentInput && (
                <div className="text-slate-300">
                  <span className="font-medium">{currentInput.name}</span>님의 사주 분석
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleShare}
                className="text-slate-400 hover:text-slate-200"
              >
                <Share2 className="w-4 h-4 mr-1" />
                공유
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleDownload}
                className="text-slate-400 hover:text-slate-200"
              >
                <Download className="w-4 h-4 mr-1" />
                저장
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* 메인 컨텐츠 */}
      <ModernSajuLayout 
        result={result} 
        birthInfo={birthInfo}
      />

      {/* 하단 액션 바 */}
      <div className="sticky bottom-0 bg-slate-900/95 backdrop-blur-sm border-t border-slate-700/50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-center gap-4">
            <Link href="/calculator">
              <Button variant="outline" className="px-6">
                새로 계산하기
              </Button>
            </Link>
            <Button onClick={handleShare} variant="saju" className="px-6">
              결과 공유하기
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ResultPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mx-auto mb-4 flex items-center justify-center animate-spin">
            <RefreshCw className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-xl font-medium text-slate-200 mb-2">사주 분석 로딩 중...</h2>
          <p className="text-slate-400">잠시만 기다려주세요.</p>
        </div>
      </div>
    }>
      <ResultContent />
    </Suspense>
  );
}