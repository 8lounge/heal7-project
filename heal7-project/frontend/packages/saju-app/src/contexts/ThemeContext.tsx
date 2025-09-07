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
      root.style.setProperty('--theme-text-primary', '#ffffff');
      root.style.setProperty('--theme-text-secondary', '#e5e7eb');
      root.style.setProperty('--theme-text-muted', '#9ca3af');
      root.style.setProperty('--theme-bg-primary', '#000000');
      root.style.setProperty('--theme-bg-surface', 'rgba(255, 255, 255, 0.1)');
      root.style.setProperty('--theme-bg-card', 'rgba(255, 255, 255, 0.1)');
      root.style.setProperty('--theme-bg-card-alt', 'rgba(168, 85, 247, 0.1)');
      root.style.setProperty('--theme-border', 'rgba(255, 255, 255, 0.1)');
      root.style.setProperty('--theme-accent', '#a855f7');
      root.className = 'theme-dark';
    } else {
      root.style.setProperty('--theme-text-primary', '#1a202c');
      root.style.setProperty('--theme-text-secondary', '#2d3748');
      root.style.setProperty('--theme-text-muted', '#4a5568');
      root.style.setProperty('--theme-bg-primary', '#fdf2f8');
      root.style.setProperty('--theme-bg-surface', 'rgba(236, 72, 153, 0.15)');
      root.style.setProperty('--theme-bg-card', 'linear-gradient(135deg, rgba(240, 147, 251, 0.4) 0%, rgba(245, 87, 108, 0.4) 100%)');
      root.style.setProperty('--theme-bg-card-alt', 'linear-gradient(135deg, rgba(255, 154, 158, 0.3) 0%, rgba(254, 207, 239, 0.3) 50%, rgba(255, 236, 210, 0.3) 100%)');
      root.style.setProperty('--theme-border', 'rgba(251, 146, 60, 0.3)');
      root.style.setProperty('--theme-accent', '#ec4899');
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