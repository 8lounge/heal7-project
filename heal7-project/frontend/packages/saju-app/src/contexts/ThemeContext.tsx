import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useWeatherTheme, ThemeMode } from '../hooks/useWeatherTheme';

// 테마 컨텍스트 타입 정의
interface ThemeContextType {
  theme: ThemeMode;
  isManualOverride: boolean;
  toggleTheme: () => void;
  resetToAuto: () => void;
  weatherData: any;
  isLoading: boolean;
  error: string | null;
}

// 테마 컨텍스트 생성
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// 테마 프로바이더 Props
interface ThemeProviderProps {
  children: ReactNode;
}

// 테마 프로바이더 컴포넌트
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const weatherTheme = useWeatherTheme();
  const [isManualOverride, setIsManualOverride] = useState(false);
  const [manualTheme, setManualTheme] = useState<ThemeMode>('dark');

  // 로컬 스토리지에서 수동 테마 설정 복원
  useEffect(() => {
    const savedManualOverride = localStorage.getItem('heal7_manual_theme_override');
    const savedTheme = localStorage.getItem('heal7_manual_theme') as ThemeMode;
    
    if (savedManualOverride === 'true' && savedTheme) {
      setIsManualOverride(true);
      setManualTheme(savedTheme);
    }
  }, []);

  // 수동 테마 토글 함수
  const toggleTheme = () => {
    const newTheme = isManualOverride 
      ? (manualTheme === 'dark' ? 'light' : 'dark')
      : (weatherTheme.theme === 'dark' ? 'light' : 'dark');
    
    setManualTheme(newTheme);
    setIsManualOverride(true);
    
    // 로컬 스토리지에 저장
    localStorage.setItem('heal7_manual_theme_override', 'true');
    localStorage.setItem('heal7_manual_theme', newTheme);
  };

  // 자동 테마로 리셋
  const resetToAuto = () => {
    setIsManualOverride(false);
    localStorage.removeItem('heal7_manual_theme_override');
    localStorage.removeItem('heal7_manual_theme');
  };

  // 최종 테마 결정
  const currentTheme = isManualOverride ? manualTheme : weatherTheme.theme;

  // CSS 변수로 테마 적용 (루트 엘리먼트에)
  useEffect(() => {
    const root = document.documentElement;
    
    if (currentTheme === 'dark') {
      // 🌙 macOS Dark - Premium Purple Universe Theme
      root.style.setProperty('--theme-text-primary', '#ffffff');
      root.style.setProperty('--theme-text-secondary', '#ffffff');
      root.style.setProperty('--theme-text-muted', '#ffffff');
      root.style.setProperty('--theme-text-inverse', '#000000');
      root.style.setProperty('--theme-bg-primary', 'linear-gradient(135deg, #1a0d2e 0%, #2d1b4e 30%, #4c1d95 70%, #1e0a37 100%)');
      root.style.setProperty('--theme-bg-surface', 'rgba(255, 255, 255, 0.09)');
      root.style.setProperty('--theme-bg-card', 'rgba(255, 255, 255, 0.09)');
      root.style.setProperty('--theme-bg-card-alt', 'rgba(255, 255, 255, 0.12)');
      root.style.setProperty('--theme-border', 'rgba(168, 85, 247, 0.25)');
      root.style.setProperty('--theme-accent', '#a855f7');
      root.className = 'theme-dark';
    } else {
      // ☀️ macOS Light - Clean White with System Blue
      root.style.setProperty('--theme-text-primary', '#000000');
      root.style.setProperty('--theme-text-secondary', '#000000');
      root.style.setProperty('--theme-text-muted', '#000000');
      root.style.setProperty('--theme-text-inverse', '#ffffff');
      root.style.setProperty('--theme-bg-primary', '#ffffff');
      root.style.setProperty('--theme-bg-surface', 'rgba(255, 255, 255, 0.75)');
      root.style.setProperty('--theme-bg-card', 'rgba(255, 255, 255, 0.75)');
      root.style.setProperty('--theme-bg-card-alt', 'rgba(255, 255, 255, 0.85)');
      root.style.setProperty('--theme-border', 'rgba(0, 122, 255, 0.2)');
      root.style.setProperty('--theme-accent', '#007aff');
      root.className = 'theme-light';
    }
  }, [currentTheme]);

  const value: ThemeContextType = {
    theme: currentTheme,
    isManualOverride,
    toggleTheme,
    resetToAuto,
    weatherData: weatherTheme.weatherData,
    isLoading: weatherTheme.isLoading,
    error: weatherTheme.error,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// 테마 컨텍스트 사용 훅
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export default ThemeProvider;