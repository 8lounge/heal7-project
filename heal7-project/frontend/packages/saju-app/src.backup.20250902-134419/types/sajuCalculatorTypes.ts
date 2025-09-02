// 사주 계산기 관련 타입 정의

export type ViewMode = 'basic' | 'cyber_fantasy';

export interface SajuForm {
  year: string;
  month: string;
  day: string;
  hour: string;
  minute: string;
  gender: 'M' | 'F';
  location: string;
}

export interface SajuCalculatorProps {
  viewMode: ViewMode;
}

export interface LoadingStep {
  icon: string;
  message: string;
  emoji: string;
}

export type SajuTabType = 'personality' | 'career' | 'love' | 'fortune';