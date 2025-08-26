import React, { useState } from 'react';
import { Brain, TrendingUp, TrendingDown, Target, Users, Sparkles } from 'lucide-react';

interface PersonalityResult {
  mbti_type: string;
  saju_element: string;
  personality_summary: string;
  strengths: string[];
  weaknesses: string[];
  growth_directions: string[];
  famous_people: string[];
}

export const PersonalityProfile: React.FC = () => {
  const [formData, setFormData] = useState({
    birthDate: '',
    mbti: '',
    gender: 'male' as 'male' | 'female',
    name: ''
  });
  const [result, setResult] = useState<PersonalityResult | null>(null);
  const [loading, setLoading] = useState(false);

  const mbtiTypes = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP', 
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
  ];

  const elementColors: Record<string, string> = {
    '목': 'from-green-400 to-emerald-500',
    '화': 'from-red-400 to-pink-500', 
    '토': 'from-yellow-400 to-orange-500',
    '금': 'from-gray-300 to-slate-400',
    '수': 'from-blue-400 to-cyan-500'
  };

  const elementEmojis: Record<string, string> = {
    '목': '🌳', '화': '🔥', '토': '🏔️', '금': '⚡', '수': '🌊'
  };

  const handleAnalyze = async () => {
    if (!formData.birthDate || !formData.mbti) {
      alert('생년월일과 MBTI 유형을 선택해주세요.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`/api/fortune/personality-profile?mbti_type=${formData.mbti}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          birth_date: formData.birthDate,
          birth_time: '12:00',
          gender: formData.gender,
          name: formData.name,
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
      <div className="max-w-5xl mx-auto">
        
        {/* 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            🧠 통합 성격 프로파일
          </h1>
          <p className="text-gray-600 text-lg">
            MBTI × 사주 오행의 만남, 진짜 나를 발견하는 입체적 진단
          </p>
        </div>

        {/* 입력 폼 */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 mb-8">
          <div className="mb-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Brain className="w-5 h-5" />
              성격 분석을 위한 정보 입력
            </h3>
          </div>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2 text-white">생년월일</label>
                <input
                  type="date"
                  value={formData.birthDate}
                  onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-white">MBTI 유형</label>
                <select
                  value={formData.mbti}
                  onChange={(e) => setFormData({...formData, mbti: e.target.value})}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                >
                  <option value="">MBTI 유형을 선택하세요</option>
                  {mbtiTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  MBTI를 모르신다면 <a href="#" className="text-blue-500 underline">여기서 무료 테스트</a>
                </p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2 text-white">이름 (선택)</label>
                <input
                  type="text"
                  placeholder="이름을 입력하세요"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white placeholder-gray-400"
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
                      checked={formData.gender === 'male'}
                      onChange={(e) => setFormData({...formData, gender: e.target.value as 'male'})}
                      className="mr-2"
                    />
                    남성
                  </label>
                  <label className="flex items-center text-white">
                    <input
                      type="radio"
                      name="gender"
                      value="female"
                      checked={formData.gender === 'female'}
                      onChange={(e) => setFormData({...formData, gender: e.target.value as 'female'})}
                      className="mr-2"
                    />
                    여성
                  </label>
                </div>
              </div>
            </div>
            
            <div className="text-center">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="bg-gradient-to-r from-violet-500 to-indigo-500 hover:from-violet-600 hover:to-indigo-600 text-white px-8 py-3 text-lg rounded-lg font-medium transition-all duration-300 hover:scale-105 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2 inline-block"></div>
                    분석 중...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2 inline" />
                    통합 성격 분석하기
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* 결과 표시 */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            
            {/* 종합 결과 카드 */}
            <div className="border-2 border-violet-200/30 bg-white/10 backdrop-blur-md rounded-xl p-8">
                <div className="text-center mb-6">
                  <div className="flex justify-center items-center gap-4 mb-4">
                    <div className="text-4xl font-bold text-violet-600 bg-white rounded-full px-4 py-2 shadow-lg">
                      {result.mbti_type}
                    </div>
                    <div className="text-2xl">×</div>
                    <div className={`text-4xl rounded-full px-4 py-2 shadow-lg text-white bg-gradient-to-r ${elementColors[result.saju_element]}`}>
                      {elementEmojis[result.saju_element]} {result.saju_element}
                    </div>
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-4">
                    {formData.name || '회원님'}의 통합 성격 프로파일
                  </h2>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-semibold text-white mb-3 text-center">✨ 종합 분석</h3>
                  <p className="text-white text-lg leading-relaxed text-center">
                    {result.personality_summary}
                  </p>
                </div>
            </div>

            {/* 강점과 약점 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-md border border-green-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                    강점 & 장점
                  </h3>
                </div>
                <div>
                  <div className="space-y-2">
                    {result.strengths.map((strength, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-white">{strength}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md border border-orange-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <TrendingDown className="w-5 h-5 text-orange-400" />
                    보완점 & 주의사항
                  </h3>
                </div>
                <div>
                  <div className="space-y-2">
                    {result.weaknesses.map((weakness, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        <span className="text-white">{weakness}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* 성장 방향 */}
            <div className="bg-white/10 backdrop-blur-md border border-blue-200/30 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Target className="w-5 h-5 text-blue-400" />
                  성장 방향 & 개발 포인트
                </h3>
              </div>
              <div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {result.growth_directions.map((direction, index) => (
                    <div key={index} className="bg-white rounded-lg p-4 shadow-sm">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {index + 1}
                        </div>
                        <span className="font-medium text-white">{direction}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 유명인 */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Users className="w-5 h-5 text-purple-400" />
                  동일한 성격 유형의 유명인들
                </h3>
              </div>
              <div>
                <p className="text-white/80 mb-4">
                  회원님과 비슷한 성격 유형을 가진 유명인들을 만나보세요!
                </p>
                <div className="flex flex-wrap gap-3">
                  {result.famous_people.map((person, index) => (
                    <span key={index} className="inline-block border border-purple-400/50 text-purple-300 px-3 py-1 rounded-full text-sm bg-white/10 backdrop-blur-sm">
                      ⭐ {person}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* 추천 서비스 */}
            <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 backdrop-blur-md border border-purple-200/30 rounded-xl p-6">
                <div className="text-center">
                  <h3 className="text-xl font-bold text-white mb-3">
                    🔮 성격에 맞는 맞춤 운세는 어떠세요?
                  </h3>
                  <p className="text-white/80 mb-4">
                    회원님의 성격 유형에 최적화된 연애, 직업, 인간관계 운세를 확인해보세요!
                  </p>
                  <div className="flex flex-wrap justify-center gap-3">
                    <button className="border border-red-400/50 text-red-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                      💕 성격별 연애운
                    </button>
                    <button className="border border-blue-400/50 text-blue-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                      🚀 적성별 직업운
                    </button>
                    <button className="border border-green-400/50 text-green-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                      👥 관계별 궁합운
                    </button>
                  </div>
                </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default PersonalityProfile;