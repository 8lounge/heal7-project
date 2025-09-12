import { useState, useEffect } from 'react';
import { getKoreaHour, isNightTimeInKorea } from '../utils/timeUtils';

export type ThemeMode = 'dark' | 'light';

interface WeatherData {
  weather: string;
  temperature: number;
  city: string;
  country: string;
}

// 백엔드 날씨 API 응답 구조
interface WeatherApiResponse {
  weather: string;
  temperature: number;
  city: string;
  success: boolean;
  message?: string;
}

export const useWeatherTheme = () => {
  const [theme, setTheme] = useState<ThemeMode>('dark');
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 사용자의 위치를 가져오는 함수
  const getUserLocation = (): Promise<{ lat: number; lon: number }> => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          });
        },
        (error) => {
          // 위치 접근 실패 시 서울 좌표 사용
          resolve({ lat: 37.5665, lon: 126.9780 });
        },
        {
          timeout: 10000,
          enableHighAccuracy: false,
          maximumAge: 300000 // 5분간 캐시 사용
        }
      );
    });
  };

  // 백엔드를 통해 KMA API 날씨 데이터를 가져오는 함수
  const fetchWeatherData = async (): Promise<WeatherData> => {
    try {
      const { lat, lon } = await getUserLocation();
      
      // 백엔드 API를 통해 기상청 데이터 요청
      const response = await fetch('/api/weather/current', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: lat,
          longitude: lon
        })
      });
      
      if (!response.ok) {
        throw new Error(`날씨 API 응답 오류: ${response.status}`);
      }
      
      const data = await response.json();
      
      return {
        weather: data.weather || 'clear',
        temperature: data.temperature || 20,
        city: data.city || '서울',
        country: 'KR'
      };
      
    } catch (error) {
      console.warn('백엔드 날씨 API 호출 실패, 기본값 사용:', error);
      // API 실패 시 기본값 반환
      return {
        weather: 'clear',
        temperature: 20,
        city: '서울',
        country: 'KR'
      };
    }
  };

  // 테마를 결정하는 함수
  const determineTheme = (weather: string): ThemeMode => {
    // 한국 시간대 기준 밤/낮 판단 (글로벌 상수 사용)
    const isNightTime = isNightTimeInKorea();
    
    // 비/눈/구름 많음/황사 등의 날씨 조건 (어두운 테마 적용 대상)
    const isDarkWeather = [
      'rain', 'drizzle', 'thunderstorm',  // 비 관련
      'snow', 'sleet',                    // 눈 관련
      'mist', 'fog', 'haze',             // 안개 관련
      'clouds', 'overcast',              // 구름 관련
      'dust', 'sand', 'ash'              // 황사/미세먼지 관련
    ].includes(weather.toLowerCase());
    
    // 밤 시간이거나 어두운 날씨일 때 어두운 테마
    if (isNightTime || isDarkWeather) {
      return 'dark';
    }
    
    // 그 외는 밝은 테마
    return 'light';
  };

  // 날씨 데이터를 가져오고 테마 설정
  const updateWeatherTheme = async () => {
    try {
      setError(null);
      
      const weather = await fetchWeatherData();
      setWeatherData(weather);
      
      const newTheme = determineTheme(weather.weather);
      setTheme(newTheme);
      
    } catch (error) {
      setError(error instanceof Error ? error.message : '날씨 데이터 로드 실패');
      // 오류 시 한국 시간 기준으로만 테마 결정 (글로벌 상수 사용)
      const fallbackTheme: ThemeMode = isNightTimeInKorea() ? 'dark' : 'light';
      setTheme(fallbackTheme);
    } finally {
      setIsLoading(false);
    }
  };

  // 수동으로 테마 전환 (토글 기능)
  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  // 초기 로드 및 1시간마다 업데이트
  useEffect(() => {
    // 즉시 로딩 완료하고 한국 시간 기준 기본 테마 설정 (글로벌 상수 사용)
    const initialTheme: ThemeMode = isNightTimeInKorea() ? 'dark' : 'light';
    setTheme(initialTheme);
    setIsLoading(false);
    
    // 백그라운드에서 날씨 데이터 업데이트 (비동기)
    updateWeatherTheme();
    
    // 1시간마다 날씨 데이터 업데이트
    const interval = setInterval(updateWeatherTheme, 60 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  return {
    theme,
    weatherData,
    isLoading,
    error,
    toggleTheme,
    updateWeatherTheme
  };
};