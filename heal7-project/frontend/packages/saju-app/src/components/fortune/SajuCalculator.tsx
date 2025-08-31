import React, { useState } from 'react';
import { SajuCalculatorProps } from '../../types/sajuCalculatorTypes';
import SajuCalculatorPrimary from './SajuCalculatorPrimary';
import SajuCalculatorSecondary from './SajuCalculatorSecondary';

/**
 * 사주 계산기 - 리팩터링된 버전
 * 
 * 구조:
 * - Primary: 입력 폼 + 기본 결과 (일반 사용자용)
 * - Secondary: 상세 탭별 분석 (심화 해석용)
 * 
 * 리팩터링 효과:
 * - 기존: 761줄 단일 파일
 * - 개선: 기능별 분리 + 타입 모듈화
 * - 사용성: 단계별 정보 제공으로 UX 향상
 */

type ViewState = 'calculator' | 'detailed';

const SajuCalculator: React.FC<SajuCalculatorProps> = ({ viewMode }) => {
  const [currentView, setCurrentView] = useState<ViewState>('calculator');
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const handleDetailedAnalysis = (result: any) => {
    setAnalysisResult(result);
    setCurrentView('detailed');
  };

  const handleBackToCalculator = () => {
    setCurrentView('calculator');
  };

  return (
    <>
      {currentView === 'calculator' ? (
        <SajuCalculatorPrimary 
          viewMode={viewMode}
          onDetailedAnalysis={handleDetailedAnalysis}
        />
      ) : (
        <SajuCalculatorSecondary
          viewMode={viewMode}
          result={analysisResult}
          onBackToCalculator={handleBackToCalculator}
        />
      )}
    </>
  );
};

export default SajuCalculator;