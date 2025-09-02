import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, Sparkles, Star, Briefcase, Gem, ArrowRight, Users } from 'lucide-react';
import { zodiacSigns, calculateZodiac, checkCompatibility, getMostRecentZodiacYear, calculateZodiacFromBirth, type ZodiacSign } from '../../data/zodiacData';

type ViewMode = 'basic' | 'cyber_fantasy';

// 최적화된 이미지 컴포넌트 (AVIF → WebP → PNG 폴백)
interface OptimizedImageProps {
  id: string;
  alt: string;
  className?: string;
  sizes?: string;
  loading?: 'lazy' | 'eager';
  isActive?: boolean;
  onClick?: () => void;
}

const OptimizedImage: React.FC<OptimizedImageProps> = ({ 
  id, alt, className = '', sizes, loading = 'lazy', isActive = false, onClick 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [imageSrc, setImageSrc] = useState(`/zodiac-images/${id}.webp`);

  const handleImageLoad = () => {
    setIsLoaded(true);
  };

  const handleImageError = () => {
    // WebP 실패 시 PNG로 폴백
    if (imageSrc.includes('.webp')) {
      setImageSrc(`/zodiac-images/${id}.png`);
    } else {
      console.error(`Failed to load both WebP and PNG images for: ${id}`);
    }
  };

  return (
    <div className={`relative overflow-hidden ${className}`} onClick={onClick}>
      <motion.img
        src={imageSrc}
        alt={alt}
        loading={loading}
        className={`w-full h-full object-contain transition-all duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        } ${
          isActive ? 'scale-105 brightness-110 saturate-110' : ''
        }`}
        onLoad={handleImageLoad}
        onError={handleImageError}
        whileHover={isActive ? { 
          scale: 1.08,
          rotate: [0, -1, 1, 0],
          transition: { duration: 0.3 }
        } : {}}
        animate={isActive ? {
          filter: ['brightness(1)', 'brightness(1.1)', 'brightness(1)'],
          transition: { 
            duration: 2,
            repeat: Infinity,
            repeatType: 'reverse'
          }
        } : {}}
      />
      
      {/* 로딩 스피너 */}
      {!isLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/5 backdrop-blur-sm">
          <div className="w-6 h-6 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
        </div>
      )}
      
      {/* 액티브 효과 - 글로우 */}
      {isActive && isLoaded && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-purple-500/20 via-transparent to-blue-500/20 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ 
            opacity: [0.3, 0.7, 0.3],
            scale: [1, 1.02, 1]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
      )}
    </div>
  );
};

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
  const [, setPartnerZodiac] = useState<string | null>(null);
  const [useDetailedBirth, setUseDetailedBirth] = useState(false);

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
          나의 띠를 통해 알아보는 성향, 직업 적성, 2025년 운세
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
                relative bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-4 cursor-pointer
                transition-all duration-300 hover:scale-105 hover:bg-white/20 overflow-hidden
                ${selectedZodiac?.id === zodiac.id ? 'ring-2 ring-purple-400 bg-purple-500/20 shadow-lg shadow-purple-500/25' : ''}
              `}
              onClick={() => handleZodiacClick(zodiac)}
              onMouseEnter={() => setHoveredZodiac(zodiac.id)}
              onMouseLeave={() => setHoveredZodiac(null)}
              whileHover={{ 
                scale: 1.05,
                rotateY: hoveredZodiac === zodiac.id ? 5 : 0,
                transition: { duration: 0.3 }
              }}
              whileTap={{ scale: 0.95 }}
            >
              {/* 선택된 카드 배경 글로우 효과 */}
              {selectedZodiac?.id === zodiac.id && (
                <motion.div
                  className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-transparent to-blue-500/20 rounded-xl"
                  initial={{ opacity: 0 }}
                  animate={{ 
                    opacity: [0.3, 0.6, 0.3],
                    scale: [1, 1.02, 1]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    repeatType: 'reverse'
                  }}
                />
              )}
              
              {/* 호버 시 반짝이는 효과 */}
              {hoveredZodiac === zodiac.id && (
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent rounded-xl"
                  initial={{ x: '-100%' }}
                  animate={{ x: '100%' }}
                  transition={{
                    duration: 0.6,
                    repeat: Infinity,
                    repeatDelay: 1
                  }}
                />
              )}
              <div className="text-center">
                {/* 선택 그리드는 항상 이모지 아이콘으로 표시 */}
                <div className="mb-2">
                  <motion.div 
                    className="text-4xl"
                    animate={hoveredZodiac === zodiac.id ? {
                      scale: [1, 1.2, 1],
                      rotate: [0, -10, 10, 0]
                    } : selectedZodiac?.id === zodiac.id ? {
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0]
                    } : {}}
                    transition={{ duration: 0.5 }}
                  >
                    {zodiac.emoji}
                  </motion.div>
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
              {/* 좌측 - 띠 결과 이미지/설명 */}
              <div className="lg:col-span-1">
                <motion.div 
                  className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 text-center h-full flex flex-col justify-center"
                  initial={{ 
                    opacity: 0, 
                    scale: 0.8, 
                    rotateY: -90 
                  }}
                  animate={{ 
                    opacity: 1, 
                    scale: 1, 
                    rotateY: 0 
                  }}
                  transition={{ 
                    duration: 0.8, 
                    delay: 0.2,
                    type: "spring",
                    stiffness: 100,
                    damping: 15
                  }}
                  style={{ perspective: 1000 }}
                >
                  {/* 메인 이미지 */}
                  <motion.div 
                    className="mb-6"
                    initial={{ 
                      opacity: 0, 
                      scale: 0.5, 
                      rotate: -180 
                    }}
                    animate={{ 
                      opacity: 1, 
                      scale: 1, 
                      rotate: 0 
                    }}
                    transition={{ 
                      duration: 1.2, 
                      delay: 0.5,
                      type: "spring",
                      stiffness: 80,
                      damping: 12
                    }}
                  >
                    <OptimizedImage
                      id={selectedZodiac.id}
                      alt={selectedZodiac.name}
                      className="w-32 h-48 md:w-40 md:h-60 lg:w-48 lg:h-72 mx-auto rounded-lg shadow-lg"
                      sizes="(min-width: 1024px) 192px, (min-width: 768px) 160px, 128px"
                      loading="eager"
                      isActive={true}
                    />
                  </motion.div>
                  
                  {/* 띠 정보 */}
                  <motion.div 
                    className="space-y-3"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                  >
                    <motion.h3 
                      className="text-2xl font-bold text-white"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.5, delay: 0.9 }}
                    >
                      {selectedZodiac.name}
                    </motion.h3>
                    <motion.p 
                      className="text-white/70 text-lg"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.4, delay: 1.0 }}
                    >
                      {selectedZodiac.chineseName}
                    </motion.p>
                    
                    {/* 기본 속성 */}
                    <motion.div 
                      className="space-y-2"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 1.1 }}
                    >
                      <div className="bg-purple-500/20 text-purple-300 px-3 py-2 rounded-lg text-sm">
                        <span className="font-medium">오행:</span> {selectedZodiac.element}
                      </div>
                      <div className="bg-blue-500/20 text-blue-300 px-3 py-2 rounded-lg text-sm">
                        <span className="font-medium">최근 해:</span> {getMostRecentZodiacYear(selectedZodiac.id)}년
                      </div>
                    </motion.div>
                    
                    {/* 대표 특징 */}
                    <motion.div 
                      className="mt-4 p-3 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-lg border border-yellow-500/20"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.4, delay: 1.2 }}
                    >
                      <p className="text-yellow-200 text-sm font-medium">
                        "{selectedZodiac.characteristics[0]}"
                      </p>
                    </motion.div>
                  </motion.div>
                </motion.div>
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

                {/* 적합한 직업 */}
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
                        onClick={() => setPartnerZodiac(otherZodiac.id)}
                      >
                        <div className="mb-1">
                          <motion.div 
                            className="text-2xl"
                            whileHover={{
                              scale: 1.3,
                              rotate: [0, -15, 15, 0],
                              transition: { duration: 0.4 }
                            }}
                          >
                            {otherZodiac.emoji}
                          </motion.div>
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