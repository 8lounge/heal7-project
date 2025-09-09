import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  ChevronLeft, 
  ChevronRight, 
  Star, 
  Sparkles,
  Info,
  TrendingUp,
  Sun
} from 'lucide-react';
import { 
  generateCalendarMonth, 
  getMonthlyFortune, 
  getTodayFortune,
  getKasiApiErrorSummary,
  get절기상세정보,
  is절기날,
  get갑자표시,
  type CalendarDate,
  type MonthlyFortune 
} from '../../data/calendarData';

type ViewMode = 'basic' | 'cyber_fantasy'

interface FortuneCalendarProps {
  onClose?: () => void;
  viewMode: ViewMode;
}

export const FortuneCalendar: React.FC<FortuneCalendarProps> = ({ onClose: _, viewMode }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<CalendarDate | null>(null);
  const [monthlyData, setMonthlyData] = useState<CalendarDate[]>([]);
  const [monthlyFortune, setMonthlyFortune] = useState<MonthlyFortune | null>(null);
  const [todayFortune, setTodayFortune] = useState<CalendarDate | null>(null);

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-featured' : 'card-base';

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth() + 1;

  useEffect(() => {
    const loadCalendarData = async () => {
      try {
        console.log(`🔮 캘린더 데이터 로딩 시작: ${year}년 ${month}월`);
        
        // KASI API를 사용한 비동기 데이터 로딩
        const [data, fortune, today] = await Promise.all([
          generateCalendarMonth(year, month),
          getMonthlyFortune(year, month), // 이제 비동기 함수
          getTodayFortune() // 이제 비동기 함수
        ]);
        
        setMonthlyData(data);
        setMonthlyFortune(fortune);
        setTodayFortune(today);
        
        console.log(`✅ 캘린더 데이터 로딩 완료: ${data.length}개 날짜`);
        
        // KASI API 오류 요약 로그
        const errorSummary = getKasiApiErrorSummary();
        if (errorSummary.total > 0) {
          console.warn(`⚠️  KASI API 오류 요약: 총 ${errorSummary.total}건`, errorSummary.byType);
        }
        
      } catch (error) {
        console.error('캘린더 데이터 로딩 실패:', error);
        // 오류 발생 시 빈 데이터로 설정
        setMonthlyData([]);
        setMonthlyFortune(null);
        setTodayFortune(null);
      }
    };
    
    loadCalendarData();
  }, [year, month]);

  const navigateMonth = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    if (direction === 'prev') {
      newDate.setMonth(currentDate.getMonth() - 1);
    } else {
      newDate.setMonth(currentDate.getMonth() + 1);
    }
    setCurrentDate(newDate);
    setSelectedDate(null);
  };

  const getDayClass = (calendarDate: CalendarDate) => {
    const isToday = calendarDate.date.toDateString() === new Date().toDateString();
    const isSelected = selectedDate?.date.toDateString() === calendarDate.date.toDateString();
    const is절기 = is절기날(calendarDate.date);
    
    let className = 'relative p-2 rounded-lg cursor-pointer card-nav ';
    
    if (isToday) {
      className += 'ring-2 ring-yellow-400 bg-yellow-400/20 ';
    }
    
    if (isSelected) {
      className += 'bg-[var(--theme-primary)]/30 ring-2 ring-[var(--theme-primary)] ';
    }
    
    // 🔥 윤달 날짜 특별 강조 (절기보다 우선)
    if (calendarDate.isLeapMonth && !isToday && !isSelected) {
      className += 'bg-indigo-400/20 ring-2 ring-indigo-400/60 shadow-lg shadow-indigo-400/25 ';
    }
    // 🔥 절기 날짜 특별 강조 (윤달 다음 우선순위)
    else if (is절기 && !isToday && !isSelected) {
      const 절기정보 = get절기상세정보(calendarDate.date);
      if (절기정보) {
        // 계절별 배경색
        const 계절배경색: Record<string, string> = {
          '봄': 'bg-green-400/15 ring-1 ring-green-400/40 ',
          '여름': 'bg-orange-400/15 ring-1 ring-orange-400/40 ',
          '가을': 'bg-red-400/15 ring-1 ring-red-400/40 ',
          '겨울': 'bg-blue-400/15 ring-1 ring-blue-400/40 '
        };
        className += 계절배경색[절기정보.season] || 'bg-yellow-400/10 ring-1 ring-yellow-400/30 ';
      }
    } else if (calendarDate.gilil) {
      className += 'bg-green-500/20 ';
    } else if (calendarDate.흉일) {
      className += 'bg-red-500/20 ';
    } else if (calendarDate.sonEobNeunNal) {
      className += 'bg-gray-500/20 ';
    }
    
    return className;
  };

  const getScoreColor = (score: number) => {
    if (score >= 4) return 'text-green-400';
    if (score >= 3) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBg = (score: number) => {
    if (score >= 4) return 'bg-green-500/20';
    if (score >= 3) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  // 캘린더 그리드 생성 (첫째 주 공백 포함)
  const firstDayOfMonth = new Date(year, month - 1, 1).getDay();
  const daysInPrevMonth = new Date(year, month - 1, 0).getDate();
  const calendarGrid: (CalendarDate | null)[] = [];

  // 이전 달 마지막 주 날짜들 (회색 처리)
  for (let i = firstDayOfMonth - 1; i >= 0; i--) {
    const prevDate = new Date(year, month - 2, daysInPrevMonth - i);
    // 이전/다음 달 데이터는 기본 데이터로 표시 (비동기 호출 제거)
    calendarGrid.push(null);
  }

  // 현재 달 날짜들
  calendarGrid.push(...monthlyData);

  // 다음 달 첫째 주 날짜들 (42개 셀 채우기)
  const remainingCells = 42 - calendarGrid.length;
  for (let i = 1; i <= remainingCells; i++) {
    const nextDate = new Date(year, month, i);
    // 이전/다음 달 데이터는 기본 데이터로 표시 (비동기 호출 제거)
    calendarGrid.push(null);
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Calendar className="w-8 h-8 theme-text-primary" />
            <h1 className="text-4xl font-bold theme-text-heading">📅 운세 캘린더</h1>
            <Star className="w-8 h-8 text-yellow-300" />
          </div>
          <p className="theme-text-secondary text-lg">
            12지신, 60갑자, 손없는날을 한눈에 확인하세요
          </p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          {/* 메인 캘린더 */}
          <div className="xl:col-span-3">
            <div className={`${cardClass} p-6 rounded-xl`}>
              {/* 캘린더 헤더 */}
              <div className="flex items-center justify-between mb-6">
                <button
                  onClick={() => navigateMonth('prev')}
                  className="btn-ghost !p-2"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
                
                <div className="text-center">
                  <h2 className="text-2xl font-bold theme-text-heading">
                    {year}년 {month}월
                  </h2>
                  {monthlyFortune && (
                    <p className="theme-text-secondary text-sm mt-1">
                      {monthlyFortune.monthlyMessage}
                    </p>
                  )}
                </div>

                <button
                  onClick={() => navigateMonth('next')}
                  className="btn-ghost !p-2"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>

              {/* 요일 헤더 */}
              <div className="grid grid-cols-7 gap-2 mb-4">
                {['일', '월', '화', '수', '목', '금', '토'].map((day, index) => (
                  <div 
                    key={day} 
                    className={`text-center py-2 font-medium ${
                      index === 0 ? 'text-red-300' : index === 6 ? 'text-blue-300' : 'theme-text-primary'
                    }`}
                  >
                    {day}
                  </div>
                ))}
              </div>

              {/* 캘린더 그리드 */}
              <div className="grid grid-cols-7 gap-2">
                {calendarGrid.map((calendarDate, index) => {
                  if (!calendarDate) return <div key={index} className="p-2"></div>;
                  
                  const isCurrentMonth = calendarDate.date.getMonth() === currentDate.getMonth();
                  const dayOfWeek = calendarDate.date.getDay();
                  
                  return (
                    <div
                      key={`${calendarDate.date.getTime()}`}
                      className={`${getDayClass(calendarDate)} ${!isCurrentMonth ? 'opacity-50' : ''}`}
                      onClick={() => setSelectedDate(calendarDate)}
                    >
                      {/* 날짜 */}
                      <div className={`text-sm font-bold mb-1 ${
                        dayOfWeek === 0 ? 'text-red-300' : 
                        dayOfWeek === 6 ? 'text-blue-300' : 
                        'theme-text-primary'
                      }`}>
                        {calendarDate.date.getDate()}
                      </div>

                      {/* 갑자 (한자 포함) */}
                      <div className="text-xs text-white/80 mb-1 leading-tight">
                        {get갑자표시(calendarDate.gapja)}
                      </div>

                      {/* 🔥 음력 날짜 표시 개선 */}
                      <div className="text-xs text-white/60 mb-1 flex items-center justify-center gap-1">
                        {calendarDate.lunarMonth === 0 || calendarDate.lunarDay === 0 ? (
                          <span className="text-red-300 text-xs">음력 X</span>
                        ) : (
                          <>
                            <span>{calendarDate.lunarMonth}/{calendarDate.lunarDay}</span>
                            {calendarDate.isLeapMonth && (
                              <span 
                                className="text-indigo-300 animate-pulse" 
                                title="윤달 (음력 특별한 달)"
                              >
                                🌙+
                              </span>
                            )}
                          </>
                        )}
                      </div>

                      {/* 운세 점수 */}
                      <div className={`text-xs px-1 py-0.5 rounded ${getScoreBg(calendarDate.운세점수)} ${getScoreColor(calendarDate.운세점수)}`}>
                        ★{calendarDate.운세점수}
                      </div>

                      {/* 특이사항 아이콘 */}
                      <div className="flex justify-center mt-1 space-x-1">
                        {calendarDate.sonEobNeunNal && (
                          <span className="text-xs" title="손없는날">👻</span>
                        )}
                        {calendarDate.gilil && (
                          <span className="text-xs" title="길일">✨</span>
                        )}
                        {calendarDate.흉일 && (
                          <span className="text-xs" title="흉일">⚠️</span>
                        )}
                        {/* 🔥 24절기 아이콘 강조 시스템 */}
                        {(() => {
                          const 절기정보 = get절기상세정보(calendarDate.date);
                          if (절기정보) {
                            return (
                              <div className="flex flex-col items-center">
                                <span 
                                  className={`text-sm ${절기정보.color} drop-shadow-lg`} 
                                  title={`${절기정보.name}: ${절기정보.description}`}
                                >
                                  {절기정보.icon}
                                </span>
                                {/* 절기 강조 링 */}
                                <div className="w-1 h-1 bg-yellow-400 rounded-full opacity-75 animate-pulse"></div>
                              </div>
                            );
                          }
                          return null;
                        })()}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* 사이드바 */}
          <div className="xl:col-span-1 space-y-6">
            {/* 오늘의 운세 */}
            {todayFortune && (
              <div className={`${cardClass} p-6 rounded-xl`}>
                <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                  <Sun className="w-5 h-5" />
                  오늘의 운세
                </h3>
                <div className="space-y-3">
                  <div className="text-center">
                    <div className="text-3xl mb-2">{todayFortune.zodiac === '쥐' ? '🐭' : todayFortune.zodiac === '소' ? '🐂' : todayFortune.zodiac === '호랑이' ? '🐅' : todayFortune.zodiac === '토끼' ? '🐰' : todayFortune.zodiac === '용' ? '🐉' : todayFortune.zodiac === '뱀' ? '🐍' : todayFortune.zodiac === '말' ? '🐴' : todayFortune.zodiac === '양' ? '🐑' : todayFortune.zodiac === '원숭이' ? '🐒' : todayFortune.zodiac === '닭' ? '🐓' : todayFortune.zodiac === '개' ? '🐕' : '🐷'}</div>
                    <div className="font-bold text-white text-lg">{get갑자표시(todayFortune.yearPillar)}</div>
                    <div className="text-white/80 text-sm">{todayFortune.zodiac}의 해</div>
                    <div className="text-white/60 text-xs mt-1">오늘 일주: {get갑자표시(todayFortune.gapja)}</div>
                  </div>
                  <div className="text-center">
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${getScoreBg(todayFortune.운세점수)} ${getScoreColor(todayFortune.운세점수)}`}>
                      <Star className="w-4 h-4 mr-1" />
                      운세 {todayFortune.운세점수}/5
                    </div>
                  </div>
                  {todayFortune.특이사항.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-white/80 text-sm font-medium">특이사항</h4>
                      {todayFortune.특이사항.map((item, index) => (
                        <div key={index} className="text-xs bg-white/20 text-white px-2 py-1 rounded">
                          {item}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* 선택된 날짜 정보 */}
            {selectedDate && (
              <div className={`${cardClass} p-6 rounded-xl`}>
                <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                  <Info className="w-5 h-5" />
                  선택된 날짜
                </h3>
                <div className="space-y-3">
                  <div className="text-center">
                    <div className="text-white font-bold text-lg">
                      {selectedDate.date.getMonth() + 1}월 {selectedDate.date.getDate()}일
                    </div>
                    <div className="text-white/80 text-sm">{selectedDate.lunarDate}</div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div className="text-center">
                        <div className="text-white/80 text-xs">연주(년)</div>
                        <div className="text-white font-bold text-sm leading-tight">{get갑자표시(selectedDate.yearPillar)}</div>
                      </div>
                      <div className="text-center">
                        <div className="text-white/80 text-xs">일주(일)</div>
                        <div className="text-white font-bold text-sm leading-tight">{get갑자표시(selectedDate.gapja)}</div>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div className="text-center">
                        <div className="text-white/80 text-xs">띠</div>
                        <div className="text-white font-bold">{selectedDate.zodiac}</div>
                      </div>
                      <div className="text-center">
                        <div className="text-white/80 text-xs">오행</div>
                        <div className="text-white font-bold">{selectedDate.element}</div>
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-white/80 text-xs">운세</div>
                      <div className={`font-bold ${getScoreColor(selectedDate.운세점수)}`}>
                        {selectedDate.운세점수}/5
                      </div>
                    </div>
                  </div>

                  {selectedDate.특이사항.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-white/80 text-sm font-medium">특이사항</h4>
                      <div className="space-y-1">
                        {selectedDate.특이사항.map((item, index) => (
                          <div key={index} className="text-xs bg-white/20 text-white px-2 py-1 rounded">
                            {item}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* 월간 운세 요약 */}
            {monthlyFortune && (
              <div className={`${cardClass} p-6 rounded-xl`}>
                <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  이달의 운세
                </h3>
                <div className="space-y-4">
                  <p className="text-white/80 text-sm">
                    {monthlyFortune.monthlyMessage}
                  </p>
                  
                  {monthlyFortune.bestDates.length > 0 && (
                    <div>
                      <h4 className="text-green-300 text-sm font-medium mb-2">좋은 날들</h4>
                      <div className="flex flex-wrap gap-1">
                        {monthlyFortune.bestDates.slice(0, 3).map((date) => (
                          <span
                            key={date.date.getTime()}
                            className="text-xs bg-green-500/20 text-green-200 px-2 py-1 rounded cursor-pointer hover:bg-green-500/30"
                            onClick={() => setSelectedDate(date)}
                          >
                            {date.date.getDate()}일
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {monthlyFortune.importantDates.length > 0 && (
                    <div>
                      <h4 className="text-yellow-300 text-sm font-medium mb-2">주요 일정</h4>
                      <div className="space-y-1">
                        {monthlyFortune.importantDates.slice(0, 3).map((date) => (
                          <div
                            key={date.date.getTime()}
                            className="text-xs text-white/80 cursor-pointer hover:text-white"
                            onClick={() => setSelectedDate(date)}
                          >
                            {date.date.getDate()}일: {date.절기 || date.특이사항[0]}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* 범례 */}
            <div className={`${cardClass} p-6 rounded-xl`}>
              <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5" />
                범례
              </h3>
              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-500/20 rounded"></div>
                  <span className="text-white/80">길일</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-500/20 rounded"></div>
                  <span className="text-white/80">흉일</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-gray-500/20 rounded"></div>
                  <span className="text-white/80">손없는날</span>
                </div>
                {/* 🔥 윤달 범례 추가 */}
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-indigo-400/20 rounded ring-2 ring-indigo-400/60 shadow-sm shadow-indigo-400/25"></div>
                  <span className="text-white/80 flex items-center gap-1">
                    윤달 <span className="text-indigo-300">🌙+</span>
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-yellow-400/20 rounded ring-2 ring-yellow-400"></div>
                  <span className="text-white/80">오늘</span>
                </div>
                {/* 절기 범례 추가 */}
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-gradient-to-r from-green-400/15 via-orange-400/15 to-blue-400/15 rounded ring-1 ring-yellow-400/40"></div>
                  <span className="text-white/80">24절기</span>
                </div>
                <div className="mt-3 space-y-1">
                  <div className="theme-text-secondary">★5: 매우 좋음</div>
                  <div className="theme-text-secondary">★4: 좋음</div>
                  <div className="theme-text-secondary">★3: 보통</div>
                  <div className="theme-text-secondary">★2: 주의</div>
                  <div className="theme-text-secondary">★1: 매우 주의</div>
                </div>
                <div className="mt-3 pt-3 border-t border-pink-200/20">
                  <div className="theme-text-muted text-xs">
                    📅 M/D: 음력 월/일<br/>
                    🌙+: 윤달 (특별한 음력 달)<br/>
                    🌸: 24절기 (계절 변화)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FortuneCalendar;