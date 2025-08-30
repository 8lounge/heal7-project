import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, Sparkles, Star, Heart, Briefcase, Gem, ArrowRight, Users } from 'lucide-react';
import { zodiacSigns, calculateZodiac, checkCompatibility, type ZodiacSign } from '../../data/zodiacData';

type ViewMode = 'basic' | 'cyber_fantasy';

interface ZodiacAnalysisProps {
  viewMode?: ViewMode;
}

export const ZodiacAnalysis: React.FC<ZodiacAnalysisProps> = ({ viewMode = 'basic' }) => {
  const [birthYear, setBirthYear] = useState('');
  const [selectedZodiac, setSelectedZodiac] = useState<ZodiacSign | null>(null);
  const [hoveredZodiac, setHoveredZodiac] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [compatibilityMode, setCompatibilityMode] = useState(false);
  const [, setPartnerZodiac] = useState<string | null>(null);

  // 출생년도 입력 시 자동으로 띠 계산
  useEffect(() => {
    if (birthYear && birthYear.length === 4) {
      const year = parseInt(birthYear);
      if (year >= 1900 && year <= 2030) {
        const zodiacId = calculateZodiac(year);
        const zodiac = zodiacSigns.find(sign => sign.id === zodiacId);
        if (zodiac) {
          setSelectedZodiac(zodiac);
          setShowDetails(true);
        }
      }
    }
  }, [birthYear]);

  const handleZodiacClick = (zodiac: ZodiacSign) => {
    setSelectedZodiac(zodiac);
    setShowDetails(true);
    
    // 해당 띠의 최근 년도를 찾아서 입력값에 설정
    const currentYear = new Date().getFullYear();
    const recentYear = zodiac.years.find(year => year <= currentYear) || zodiac.years[0];
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
          나의 띠를 통해 알아보는 성향, 직업 적성, 2025년 운세
        </p>
        
        {/* 모드 토글 */}
        <div className="flex items-center justify-center gap-4 mb-6">
          <button
            onClick={() => setCompatibilityMode(false)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
              !compatibilityMode
                ? viewMode === 'cyber_fantasy'
                  ? 'bg-gradient-to-r from-purple-500/80 to-pink-500/80'
                  : 'bg-gradient-to-r from-indigo-500/80 to-purple-500/80'
                : 'bg-white/10 hover:bg-white/20'
            } text-white`}
          >
            <Star className="w-4 h-4" />
            띠 운세
          </button>
          <button
            onClick={() => setCompatibilityMode(true)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
              compatibilityMode
                ? viewMode === 'cyber_fantasy'
                  ? 'bg-gradient-to-r from-purple-500/80 to-pink-500/80'
                  : 'bg-gradient-to-r from-indigo-500/80 to-purple-500/80'
                : 'bg-white/10 hover:bg-white/20'
            } text-white`}
          >
            <Heart className="w-4 h-4" />
            띠 궁합
          </button>
        </div>
      </div>

      {/* 출생년도 입력 */}
      <div className={`p-6 mb-8 rounded-xl ${
        viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic'
      }`}>
        <div className="flex items-center justify-center gap-4 mb-4">
          <Calendar className="w-5 h-5 text-white" />
          <span className="text-white font-medium">출생년도를 입력하거나 아래에서 띠를 선택하세요</span>
        </div>
        <div className="flex justify-center">
          <input
            type="number"
            placeholder="예: 1990"
            value={birthYear}
            onChange={(e) => setBirthYear(e.target.value)}
            min="1900"
            max="2030"
            className="bg-white/20 border border-white/30 rounded-lg px-4 py-2 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500 w-32 text-center"
          />
        </div>
        {birthYear && selectedZodiac && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mt-4"
          >
            <p className="text-white/80">
              {birthYear}년생은 <span className="text-purple-300 font-bold">{selectedZodiac.name}</span>입니다!
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
                <div className="text-4xl mb-2">{zodiac.emoji}</div>
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
                      {zodiac.element} · {zodiac.years.slice(-1)[0]}년
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
            {/* 기본 정보 카드 */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 text-center">
              <div className="text-8xl mb-4">{selectedZodiac.emoji}</div>
              <h2 className="text-3xl font-bold text-white mb-2">
                {selectedZodiac.name} ({selectedZodiac.chineseName})
              </h2>
              <div className="flex justify-center items-center gap-4 mb-4">
                <span className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm">
                  오행: {selectedZodiac.element}
                </span>
                <span className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm">
                  최근: {selectedZodiac.years.slice(-1)[0]}년
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

              {/* 2025년 운세 */}
              <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
                <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-orange-400" />
                  2025년 운세
                </h3>
                <div className="space-y-3">
                  <div>
                    <span className="text-orange-300 font-medium">종합운: </span>
                    <span className="text-white/80 text-sm">{selectedZodiac.fortune2025.overall}</span>
                  </div>
                  <div>
                    <span className="text-blue-300 font-medium">직업운: </span>
                    <span className="text-white/80 text-sm">{selectedZodiac.fortune2025.career}</span>
                  </div>
                  <div>
                    <span className="text-pink-300 font-medium">연애운: </span>
                    <span className="text-white/80 text-sm">{selectedZodiac.fortune2025.love}</span>
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

            {/* 궁합 정보 (궁합 모드일 때만) */}
            {compatibilityMode && (
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
                        onClick={() => setPartnerZodiac(otherZodiac.id)}
                      >
                        <div className="text-2xl mb-1">{otherZodiac.emoji}</div>
                        <div className="text-white text-xs font-medium">{otherZodiac.name}</div>
                        <div className={`text-xs mt-1 ${getCompatibilityColor(compatibility)}`}>
                          {compatibility}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
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