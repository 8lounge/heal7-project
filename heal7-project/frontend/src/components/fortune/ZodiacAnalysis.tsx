import React, { useState } from 'react';
import { Calendar, Sparkles, Star, Zap, Gift } from 'lucide-react';

interface ZodiacResult {
  zodiac_animal: string;
  animal_character: string;
  basic_traits: string[];
  hidden_potential: string[];
  career_luck: string;
  year_fortune: string;
  lucky_colors: string[];
  lucky_numbers: number[];
}

export const ZodiacAnalysis: React.FC = () => {
  const [birthDate, setBirthDate] = useState('');
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [name, setName] = useState('');
  const [result, setResult] = useState<ZodiacResult | null>(null);
  const [loading, setLoading] = useState(false);

  const zodiacEmojis: Record<string, string> = {
    '쥐': '🐭', '소': '🐂', '범': '🐅', '토끼': '🐰',
    '용': '🐉', '뱀': '🐍', '말': '🐎', '양': '🐑',
    '원숭이': '🐵', '닭': '🐓', '개': '🐕', '돼지': '🐷'
  };

  const handleAnalyze = async () => {
    if (!birthDate) {
      alert('생년월일을 입력해주세요.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/fortune/zodiac-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          birth_date: birthDate,
          birth_time: '12:00',
          gender,
          name,
          lunar_calendar: false
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        alert('분석 중 오류가 발생했습니다.');
      }
    } catch (error) {
      console.error('분석 오류:', error);
      alert('분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        
        {/* 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            🐉 십이지신 분석
          </h1>
          <p className="text-white/80 text-lg">
            나의 띠를 통해 알아보는 기본 성향과 숨겨진 잠재력
          </p>
        </div>

        {/* 입력 폼 */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 mb-8">
          <div className="mb-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Calendar className="w-5 h-5" />
              기본 정보 입력
            </h3>
          </div>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2 text-white">생년월일</label>
                <input
                  type="date"
                  value={birthDate}
                  onChange={(e) => setBirthDate(e.target.value)}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-white">성별</label>
                <div className="flex gap-4">
                  <label className="flex items-center text-white">
                    <input
                      type="radio"
                      name="gender"
                      value="male"
                      checked={gender === 'male'}
                      onChange={(e) => setGender(e.target.value as 'male')}
                      className="mr-2"
                    />
                    남성
                  </label>
                  <label className="flex items-center text-white">
                    <input
                      type="radio"
                      name="gender"
                      value="female"
                      checked={gender === 'female'}
                      onChange={(e) => setGender(e.target.value as 'female')}
                      className="mr-2"
                    />
                    여성
                  </label>
                </div>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2 text-white">이름 (선택)</label>
              <input
                type="text"
                placeholder="이름을 입력하세요"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white placeholder-gray-400"
              />
            </div>
            
            <div className="text-center">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white px-8 py-3 text-lg rounded-lg font-medium transition-all duration-300 hover:scale-105 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2 inline-block"></div>
                    분석 중...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2 inline" />
                    십이지신 분석하기
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* 결과 표시 */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            
            {/* 띠 소개 카드 */}
            <div className="border-2 border-orange-200/30 bg-white/10 backdrop-blur-md rounded-xl p-8 text-center">
              <div className="text-8xl mb-4">
                {zodiacEmojis[result.zodiac_animal] || '🐾'}
              </div>
              <h2 className="text-3xl font-bold text-white mb-2">
                {name || '회원님'}은 <span className="text-orange-400">{result.zodiac_animal}띠</span>입니다!
              </h2>
              <p className="text-white/80 text-lg leading-relaxed">
                {result.animal_character}
              </p>
            </div>

            {/* 기본 성향 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-md border border-blue-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Star className="w-5 h-5 text-blue-400" />
                    기본 성향
                  </h3>
                </div>
                <div>
                  <div className="flex flex-wrap gap-2">
                    {result.basic_traits.map((trait, index) => (
                      <span key={index} className="inline-block border border-blue-400/50 text-blue-300 px-3 py-1 rounded-full text-sm bg-white/10 backdrop-blur-sm">
                        {trait}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md border border-purple-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Zap className="w-5 h-5 text-purple-400" />
                    숨겨진 잠재력
                  </h3>
                </div>
                <div>
                  <div className="flex flex-wrap gap-2">
                    {result.hidden_potential.map((potential, index) => (
                      <span key={index} className="inline-block border border-purple-400/50 text-purple-300 px-3 py-1 rounded-full text-sm bg-white/10 backdrop-blur-sm">
                        {potential}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* 운세 정보 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-md border border-green-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-green-400">🚀 직업운</h3>
                </div>
                <div>
                  <p className="text-white leading-relaxed">
                    {result.career_luck}
                  </p>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md border border-orange-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-orange-400">✨ 2025년 총운</h3>
                </div>
                <div>
                  <p className="text-white leading-relaxed">
                    {result.year_fortune}
                  </p>
                </div>
              </div>
            </div>

            {/* 행운 정보 */}
            <div className="bg-white/10 backdrop-blur-md border border-pink-200/30 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Gift className="w-5 h-5 text-pink-400" />
                  행운의 요소들
                </h3>
              </div>
              <div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-white mb-3">🎨 행운의 색깔</h3>
                    <div className="flex flex-wrap gap-2">
                      {result.lucky_colors.map((color, index) => (
                        <span key={index} className="inline-block bg-pink-500/20 text-pink-300 px-3 py-1 rounded-full text-sm backdrop-blur-sm">
                          {color}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold text-white mb-3">🔢 행운의 숫자</h3>
                    <div className="flex flex-wrap gap-2">
                      {result.lucky_numbers.map((number, index) => (
                        <span key={index} className="inline-block bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm backdrop-blur-sm">
                          {number}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 추가 서비스 안내 */}
            <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 backdrop-blur-md border border-purple-200/30 rounded-xl p-6">
              <div className="text-center">
                <h3 className="text-xl font-bold text-white mb-3">
                  🔮 더 자세한 분석이 궁금하시다면?
                </h3>
                <p className="text-white/80 mb-4">
                  프리미엄 서비스로 연애운, 결혼운, 상세 궁합까지 확인해보세요!
                </p>
                <div className="flex flex-wrap justify-center gap-3">
                  <button className="border border-purple-400/50 text-purple-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                    💕 연애운 분석
                  </button>
                  <button className="border border-pink-400/50 text-pink-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                    👫 궁합 분석
                  </button>
                  <button className="border border-blue-400/50 text-blue-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                    📊 종합 운세
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 안내 정보 */}
        {!result && (
          <div className="text-center text-white/60 mt-8">
            <p className="text-sm">
              🔒 개인정보는 분석 목적으로만 사용되며 안전하게 보호됩니다.
            </p>
          </div>
        )}

      </div>
    </div>
  );
};

export default ZodiacAnalysis;