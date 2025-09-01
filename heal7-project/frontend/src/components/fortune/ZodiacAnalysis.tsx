import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, Sparkles, Star, Briefcase, Gem, ArrowRight, Users } from 'lucide-react';
import { zodiacSigns, calculateZodiac, checkCompatibility, getMostRecentZodiacYear, calculateZodiacFromBirth, type ZodiacSign } from '../../data/zodiacData';

type ViewMode = 'basic' | 'cyber_fantasy';

interface ZodiacAnalysisProps {
  viewMode?: ViewMode;
}

export const ZodiacAnalysis: React.FC<ZodiacAnalysisProps> = ({ viewMode = 'basic' }) => {
  const [birthYear, setBirthYear] = useState('');
  const [birthMonth, setBirthMonth] = useState('');
  const [birthDay, setBirthDay] = useState('');
  const [selectedZodiac, setSelectedZodiac] = useState<ZodiacSign | null>(null);
  const [hoveredZodiac, setHoveredZodiac] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [partnerZodiac, setPartnerZodiac] = useState<string | null>(null);
  const [showCompatibility, setShowCompatibility] = useState(false);
  const [useDetailedBirth, setUseDetailedBirth] = useState(false);
  
  // 현재 연도 계산
  const currentYear = new Date().getFullYear();

  // 출생년도/생년월일 입력 시 자동으로 띠 계산
  useEffect(() => {
    if (birthYear && birthYear.length === 4) {
      const year = parseInt(birthYear);
      if (year >= 1900 && year <= 2030) {
        let zodiacId: string;
        
        // 상세 생년월일 입력이 있으면 입춘 기준으로 계산
        if (useDetailedBirth && birthMonth && birthDay) {
          const month = parseInt(birthMonth);
          const day = parseInt(birthDay);
          zodiacId = calculateZodiacFromBirth(year, month, day);
        } else {
          zodiacId = calculateZodiac(year);
        }
        
        const zodiac = zodiacSigns.find(sign => sign.id === zodiacId);
        if (zodiac) {
          setSelectedZodiac(zodiac);
          setShowDetails(true);
        }
      }
    }
  }, [birthYear, birthMonth, birthDay, useDetailedBirth]);

  const handleZodiacClick = (zodiac: ZodiacSign) => {
    setSelectedZodiac(zodiac);
    setShowDetails(true);
    
    // 해당 띠의 가장 최근 년도를 설정
    const recentYear = getMostRecentZodiacYear(zodiac.id);
    setBirthYear(recentYear.toString());
  };

  const getCompatibilityColor = (compatibility: string) => {
    switch (compatibility) {
      case '매우 좋음': return 'text-green-400';
      case '좋음': return 'text-blue-400';
      case '주의 필요': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const getCompatibilityBg = (compatibility: string) => {
    switch (compatibility) {
      case '매우 좋음': return 'bg-green-500/10';
      case '좋음': return 'bg-blue-500/10';
      case '주의 필요': return 'bg-yellow-500/10';
      default: return 'bg-gray-500/10';
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* 헤더 */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Star className="w-8 h-8 text-white" />
          <h1 className="text-4xl font-bold text-white">🐭 12띠 운세 센터</h1>
          <Gem className="w-8 h-8 text-purple-300" />
        </div>
        <p className="text-white/80 text-lg mb-6">
          나의 띠를 통해 알아보는 성향, 직업 적성, {currentYear}년 운세
        </p>
        
      </div>

      {/* 출생년도/생년월일 입력 */}
      <div className={`p-6 mb-8 rounded-xl ${
        viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
      }`}>
        <div className="flex items-center justify-center gap-4 mb-4">
          <Calendar className="w-5 h-5 text-white" />
          <span className="text-white font-medium">생년월일을 입력하거나 아래에서 띠를 선택하세요</span>
        </div>
        
        {/* 입력 모드 토글 */}
        <div className="flex justify-center mb-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setUseDetailedBirth(false)}
              className={`px-3 py-1 text-sm rounded-lg transition-all ${
                !useDetailedBirth 
                  ? 'bg-purple-500/80 text-white' 
                  : 'bg-white/10 text-white/60 hover:bg-white/20'
              }`}
            >
              년도만
            </button>
            <button
              onClick={() => setUseDetailedBirth(true)}
              className={`px-3 py-1 text-sm rounded-lg transition-all ${
                useDetailedBirth 
                  ? 'bg-purple-500/80 text-white' 
                  : 'bg-white/10 text-white/60 hover:bg-white/20'
              }`}
            >
              정확한 생년월일
            </button>
          </div>
        </div>

        <div className="flex justify-center gap-2">
          <input
            type="number"
            placeholder="년도"
            value={birthYear}
            onChange={(e) => setBirthYear(e.target.value)}
            min="1900"
            max="2030"
            className="bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500 w-24 text-center"
          />
          {useDetailedBirth && (
            <>
              <select
                value={birthMonth}
                onChange={(e) => setBirthMonth(e.target.value)}
                className="bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">월</option>
                {Array.from({length: 12}, (_, i) => (
                  <option key={i+1} value={i+1} className="bg-gray-800">
                    {i+1}월
                  </option>
                ))}
              </select>
              <select
                value={birthDay}
                onChange={(e) => setBirthDay(e.target.value)}
                className="bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">일</option>
                {Array.from({length: 31}, (_, i) => (
                  <option key={i+1} value={i+1} className="bg-gray-800">
                    {i+1}일
                  </option>
                ))}
              </select>
            </>
          )}
        </div>

        {useDetailedBirth && (
          <div className="text-center mt-2 text-xs text-white/60">
            💡 1~2월 초 출생은 입춘(2/4) 기준으로 정확한 띠를 계산합니다
          </div>
        )}

        {birthYear && selectedZodiac && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mt-4"
          >
            <p className="text-white/80">
              {useDetailedBirth && birthMonth && birthDay 
                ? `${birthYear}년 ${birthMonth}월 ${birthDay}일생은`
                : `${birthYear}년생은`
              } <span className="text-purple-300 font-bold">{selectedZodiac.name}</span>입니다!
            </p>
          </motion.div>
        )}
      </div>

      {/* 12지신 카드 그리드 */}
      <div className="mb-8">
        <h2 className="text-white text-xl font-bold mb-6 text-center">
          🎯 12지신 선택하기
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {zodiacSigns.map((zodiac, index) => (
            <motion.div
              key={zodiac.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className={`
                bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 cursor-pointer
                transition-all duration-300 hover:scale-105 hover:bg-white/20
                ${selectedZodiac?.id === zodiac.id ? 'ring-2 ring-purple-400 bg-purple-500/20' : ''}
              `}
              onClick={() => handleZodiacClick(zodiac)}
              onMouseEnter={() => setHoveredZodiac(zodiac.id)}
              onMouseLeave={() => setHoveredZodiac(null)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="text-center">
                <div className="mb-2">
                  <div className="text-4xl">
                    {zodiac.emoji}
                  </div>
                </div>
                <h3 className="text-white font-medium text-sm">{zodiac.name}</h3>
                <p className="text-white/60 text-xs mt-1">{zodiac.chineseName}</p>
                
                {/* 호버 시 추가 정보 */}
                <AnimatePresence>
                  {hoveredZodiac === zodiac.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-2 text-xs text-white/80"
                    >
                      {zodiac.element} · {getMostRecentZodiacYear(zodiac.id)}년
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* 상세 정보 패널 */}
      <AnimatePresence>
        {showDetails && selectedZodiac && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="space-y-6"
          >
            {/* 기본 정보 카드 - 카드 이미지 제거 */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 text-center">
              <h2 className="text-3xl font-bold text-white mb-2">
                {selectedZodiac.name} ({selectedZodiac.chineseName})
              </h2>
              <div className="flex justify-center items-center gap-4 mb-4">
                <span className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm">
                  오행: {selectedZodiac.element}
                </span>
                <span className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm">
                  최근: {getMostRecentZodiacYear(selectedZodiac.id)}년
                </span>
              </div>
            </div>

            {/* 메인 콘텐츠 - 좌측 카드 이미지, 우측 정보 섹터들 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* 좌측 - 세로형 카드 이미지 섹터 */}
              <div className="lg:col-span-1">
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 text-center h-full flex flex-col justify-center">
                  <div className="mb-4">
                    <img 
                      src={selectedZodiac.image} 
                      alt={selectedZodiac.name}
                      className="w-32 h-48 md:w-40 md:h-60 lg:w-48 lg:h-72 mx-auto object-contain rounded-lg shadow-lg"
                    />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    {selectedZodiac.name}
                  </h3>
                  <p className="text-white/70 text-sm">
                    {selectedZodiac.chineseName}
                  </p>
                </div>
              </div>

              {/* 우측 - 정보 섹터들 */}
              <div className="lg:col-span-2 space-y-6">
                {/* 성격 특성 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                  <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                    <Star className="w-5 h-5 text-yellow-400" />
                    주요 성격
                  </h3>
                  <div className="space-y-2">
                    {selectedZodiac.characteristics.map((trait, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="text-white/80 text-sm flex items-start gap-2"
                      >
                        <ArrowRight className="w-3 h-3 text-purple-400 mt-1 flex-shrink-0" />
                        {trait}
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* 직업 적성 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                  <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                    <Briefcase className="w-5 h-5 text-green-400" />
                    적합한 직업
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedZodiac.suitableJobs.map((job, index) => (
                      <motion.span
                        key={index}
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.05 }}
                        className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm"
                      >
                        {job}
                      </motion.span>
                    ))}
                  </div>
                </div>

                {/* 현재 연도 운세 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                  <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-orange-400" />
                    {currentYear}년 운세
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <span className="text-orange-300 font-medium">종합운: </span>
                      <span className="text-white/80 text-sm">{selectedZodiac.currentFortune?.overall || '운세 정보를 불러오는 중입니다.'}</span>
                    </div>
                    <div>
                      <span className="text-blue-300 font-medium">직업운: </span>
                      <span className="text-white/80 text-sm">{selectedZodiac.currentFortune?.career || '운세 정보를 불러오는 중입니다.'}</span>
                    </div>
                    <div>
                      <span className="text-pink-300 font-medium">연애운: </span>
                      <span className="text-white/80 text-sm">{selectedZodiac.currentFortune?.love || '운세 정보를 불러오는 중입니다.'}</span>
                    </div>
                  </div>
                </div>

                {/* 행운 요소 */}
                <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                  <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                    <Gem className="w-5 h-5 text-purple-400" />
                    행운 요소
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <span className="text-purple-300 font-medium">행운의 숫자: </span>
                      <div className="flex gap-2 mt-1">
                        {selectedZodiac.luckyNumbers.map((num) => (
                          <span
                            key={num}
                            className="bg-purple-500/20 text-purple-300 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                          >
                            {num}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-cyan-300 font-medium">행운의 색깔: </span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {selectedZodiac.luckyColors.map((color) => (
                          <span
                            key={color}
                            className="bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded-full text-xs"
                          >
                            {color}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 궁합 정보 */}
              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                  <Users className="w-5 h-5 text-pink-400" />
                  띠 궁합
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {zodiacSigns.map((otherZodiac) => {
                    if (otherZodiac.id === selectedZodiac.id) return null;
                    
                    const compatibility = checkCompatibility(selectedZodiac.id, otherZodiac.id);
                    
                    return (
                      <div
                        key={otherZodiac.id}
                        className={`p-3 rounded-lg border text-center cursor-pointer transition-all hover:scale-105 ${
                          getCompatibilityBg(compatibility)
                        } border-white/20`}
                        onClick={() => {
                          setPartnerZodiac(otherZodiac.id);
                          setShowCompatibility(true);
                        }}
                      >
                        <div className="mb-1">
                          <div className="text-2xl">
                            {otherZodiac.emoji}
                          </div>
                        </div>
                        <div className="text-white text-xs font-medium">{otherZodiac.name}</div>
                        <div className={`text-xs mt-1 ${getCompatibilityColor(compatibility)}`}>
                          {compatibility}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 띠별 궁합 상세 결과 */}
      <AnimatePresence>
        {showCompatibility && selectedZodiac && partnerZodiac && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-purple-900/40 to-blue-900/40 border border-white/20 backdrop-blur-sm"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Users className="w-5 h-5" />
                띠별 궁합 상세
              </h3>
              <button
                onClick={() => setShowCompatibility(false)}
                className="text-white/60 hover:text-white transition-colors text-sm"
              >
                닫기
              </button>
            </div>
            
            {(() => {
              const partnerSign = zodiacSigns.find(sign => sign.id === partnerZodiac);
              const compatibility = checkCompatibility(selectedZodiac.id, partnerZodiac);
              const compatibilityColor = getCompatibilityColor(compatibility);
              
              return (
                <div className="space-y-4">
                  {/* 궁합 대상 */}
                  <div className="flex items-center justify-center gap-8 mb-6">
                    <div className="text-center">
                      <div className="text-4xl mb-2">{selectedZodiac.emoji}</div>
                      <div className="text-white font-medium">{selectedZodiac.name}</div>
                    </div>
                    <div className="text-2xl text-white/60">×</div>
                    <div className="text-center">
                      <div className="text-4xl mb-2">{partnerSign?.emoji}</div>
                      <div className="text-white font-medium">{partnerSign?.name}</div>
                    </div>
                  </div>
                  
                  {/* 궁합 결과 */}
                  <div className="text-center mb-4">
                    <div className={`text-2xl font-bold ${compatibilityColor} mb-2`}>
                      {compatibility}
                    </div>
                  </div>
                  
                  {/* 궁합 설명 */}
                  <div className="bg-white/10 rounded-lg p-4">
                    <div className="text-white text-sm leading-relaxed">
                      {compatibility === '매우 좋음' && (
                        <p><strong>{selectedZodiac.name}</strong>와 <strong>{partnerSign?.name}</strong>은 천생연분의 궁합입니다. 서로의 장점을 부각시키고 부족한 부분을 보완해주는 관계로, 함께할 때 더욱 성장할 수 있습니다.</p>
                      )}
                      {compatibility === '좋음' && (
                        <p><strong>{selectedZodiac.name}</strong>와 <strong>{partnerSign?.name}</strong>은 좋은 궁합을 가지고 있습니다. 서로를 이해하고 배려하면 안정적이고 조화로운 관계를 유지할 수 있습니다.</p>
                      )}
                      {compatibility === '주의 필요' && (
                        <p><strong>{selectedZodiac.name}</strong>와 <strong>{partnerSign?.name}</strong>은 주의가 필요한 궁합입니다. 서로 다른 성향으로 인해 오해가 생길 수 있지만, 충분한 소통과 이해를 통해 좋은 관계를 만들어갈 수 있습니다.</p>
                      )}
                      {compatibility === '보통' && (
                        <p><strong>{selectedZodiac.name}</strong>와 <strong>{partnerSign?.name}</strong>은 평범한 궁합입니다. 특별한 갈등은 없지만 서로에 대한 깊은 이해와 노력이 필요한 관계입니다.</p>
                      )}
                    </div>
                  </div>
                  
                  {/* 다른 궁합 확인 버튼 */}
                  <div className="text-center pt-4">
                    <button
                      onClick={() => {
                        setShowCompatibility(false);
                        setPartnerZodiac(null);
                      }}
                      className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg text-sm font-medium hover:opacity-80 transition-opacity"
                    >
                      다른 띠와 궁합 보기
                    </button>
                  </div>
                </div>
              );
            })()}
          </motion.div>
        )}
      </AnimatePresence>

      {/* 안내 메시지 */}
      {!showDetails && (
        <div className="text-center text-white/60 mt-8">
          <p>출생년도를 입력하거나 위의 띠 카드를 선택해주세요</p>
        </div>
      )}
    </div>
  );
};

export default ZodiacAnalysis;