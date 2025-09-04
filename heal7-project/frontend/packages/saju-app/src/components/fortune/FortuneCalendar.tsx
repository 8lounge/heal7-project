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

  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic';

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
    
    let className = 'relative p-2 rounded-lg cursor-pointer transition-all hover:bg-white/20 ';
    
    if (isToday) {
      className += 'ring-2 ring-yellow-400 bg-yellow-400/20 ';
    }
    
    if (isSelected) {
      className += 'bg-purple-500/30 ring-2 ring-purple-400 ';
    }
    
    if (calendarDate.gilil) {
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
            <Calendar className="w-8 h-8 text-white" />
            <h1 className="text-4xl font-bold text-white">📅 운세 캘린더</h1>
            <Star className="w-8 h-8 text-yellow-300" />
          </div>
          <p className="text-white/80 text-lg">
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
                  className="p-2 rounded-lg bg-white/20 hover:bg-white/30 text-white transition-colors"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
                
                <div className="text-center">
                  <h2 className="text-2xl font-bold text-white">
                    {year}년 {month}월
                  </h2>
                  {monthlyFortune && (
                    <p className="text-white/80 text-sm mt-1">
                      {monthlyFortune.monthlyMessage}
                    </p>
                  )}
                </div>

                <button
                  onClick={() => navigateMonth('next')}
                  className="p-2 rounded-lg bg-white/20 hover:bg-white/30 text-white transition-colors"
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
                      index === 0 ? 'text-red-300' : index === 6 ? 'text-blue-300' : 'text-white'
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
                        'text-white'
                      }`}>
                        {calendarDate.date.getDate()}
                      </div>

                      {/* 갑자 */}
                      <div className="text-xs text-white/80 mb-1">
                        {calendarDate.gapja}
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
                        {calendarDate.절기 && (
                          <span className="text-xs" title={calendarDate.절기}>🌸</span>
                        )}
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
                    <div className="font-bold text-white text-lg">{todayFortune.gapja}</div>
                    <div className="text-white/80 text-sm">{todayFortune.zodiac}의 해</div>
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
                  
                  <div className="grid grid-cols-2 gap-3">
                    <div className="text-center">
                      <div className="text-white/80 text-xs">갑자</div>
                      <div className="text-white font-bold">{selectedDate.gapja}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-white/80 text-xs">띠</div>
                      <div className="text-white font-bold">{selectedDate.zodiac}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-white/80 text-xs">오행</div>
                      <div className="text-white font-bold">{selectedDate.element}</div>
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
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-yellow-400/20 rounded ring-2 ring-yellow-400"></div>
                  <span className="text-white/80">오늘</span>
                </div>
                <div className="mt-3 space-y-1">
                  <div className="text-white/80">★5: 매우 좋음</div>
                  <div className="text-white/80">★4: 좋음</div>
                  <div className="text-white/80">★3: 보통</div>
                  <div className="text-white/80">★2: 주의</div>
                  <div className="text-white/80">★1: 매우 주의</div>
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