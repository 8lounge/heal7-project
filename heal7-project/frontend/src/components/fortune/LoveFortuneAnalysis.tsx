import React, { useState } from 'react';
import { Heart, Calendar, Sparkles, Users, MessageCircle, Gift, Crown } from 'lucide-react';

interface LoveFortuneResult {
  love_tendency: string;
  ideal_partner_type: string;
  meeting_period: string;
  love_advice: string[];
  compatibility_tips: string[];
}

export const LoveFortuneAnalysis: React.FC = () => {
  const [formData, setFormData] = useState({
    birthDate: '',
    birthTime: '12:00',
    gender: 'male' as 'male' | 'female',
    name: '',
    relationshipStatus: 'single' as 'single' | 'dating' | 'married'
  });
  const [result, setResult] = useState<LoveFortuneResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!formData.birthDate) {
      alert('생년월일을 입력해주세요.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/fortune/love-fortune', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          birth_date: formData.birthDate,
          birth_time: formData.birthTime,
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
          <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-red-600 bg-clip-text text-transparent mb-4">
            💕 연애운 분석
          </h1>
          <p className="text-gray-600 text-lg">
            나의 연애 성향과 올해의 사랑운을 자세히 알아보세요
          </p>
        </div>

        {/* 입력 폼 */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 mb-8">
          <div className="mb-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Heart className="w-5 h-5 text-pink-400" />
              연애운 분석을 위한 정보
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
                <label className="block text-sm font-medium mb-2 text-white">출생시간 (선택)</label>
                <input
                  type="time"
                  value={formData.birthTime}
                  onChange={(e) => setFormData({...formData, birthTime: e.target.value})}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                />
                <p className="text-xs text-white/60 mt-1">정확한 시간을 모르면 12:00으로 설정됩니다</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
              
              <div>
                <label className="block text-sm font-medium mb-2 text-white">현재 연애 상태</label>
                <select
                  value={formData.relationshipStatus}
                  onChange={(e) => setFormData({...formData, relationshipStatus: e.target.value as any})}
                  className="w-full p-2 bg-white/20 border border-white/30 rounded-md text-white"
                >
                  <option value="single">솔로</option>
                  <option value="dating">연애 중</option>
                  <option value="married">기혼</option>
                </select>
              </div>
            </div>
            
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
            
            <div className="text-center">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white px-8 py-3 text-lg rounded-lg font-medium transition-all duration-300 hover:scale-105 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2 inline-block"></div>
                    분석 중...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2 inline" />
                    연애운 분석하기
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* 결과 표시 */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            
            {/* 연애 성향 */}
            <div className="border-2 border-pink-200/30 bg-white/10 backdrop-blur-md rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <Heart className="w-6 h-6 text-pink-400" />
                  {formData.name || '회원님'}의 연애 성향
                </h3>
              </div>
              <div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                  <p className="text-white text-lg leading-relaxed">
                    {result.love_tendency}
                  </p>
                </div>
              </div>
            </div>

            {/* 이상형과 인연 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white/10 backdrop-blur-md border border-purple-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Crown className="w-5 h-5 text-purple-400" />
                    이상적인 파트너 유형
                  </h3>
                </div>
                <div>
                  <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                    <p className="text-white leading-relaxed">
                      {result.ideal_partner_type}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md border border-orange-200/30 rounded-xl p-6">
                <div className="mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-orange-400" />
                    새로운 인연을 만날 시기
                  </h3>
                </div>
                <div>
                  <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                    <p className="text-white leading-relaxed font-medium">
                      {result.meeting_period}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* 연애 조언 */}
            <div className="bg-white/10 backdrop-blur-md border border-blue-200/30 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <MessageCircle className="w-5 h-5 text-blue-400" />
                  연애 성공을 위한 조언
                </h3>
              </div>
              <div>
                <div className="space-y-3">
                  {result.love_advice.map((advice, index) => (
                    <div key={index} className="flex items-start gap-3 bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                      <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 mt-0.5">
                        {index + 1}
                      </div>
                      <p className="text-white">{advice}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 궁합 팁 */}
            <div className="bg-white/10 backdrop-blur-md border border-green-200/30 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Users className="w-5 h-5 text-green-400" />
                  좋은 관계를 위한 궁합 팁
                </h3>
              </div>
              <div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.compatibility_tips.map((tip, index) => (
                    <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                      <div className="flex items-center gap-2 mb-2">
                        <Gift className="w-4 h-4 text-green-400" />
                        <span className="font-medium text-white">팁 {index + 1}</span>
                      </div>
                      <p className="text-white text-sm">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 월별 연애운 (간단 버전) */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6">
              <div className="mb-4">
                <h3 className="text-lg font-bold text-white text-center">📅 2025년 월별 연애운 흐름</h3>
              </div>
              <div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { month: '1-3월', score: 75, desc: '새로운 시작' },
                    { month: '4-6월', score: 90, desc: '최고의 시기' },
                    { month: '7-9월', score: 65, desc: '안정기' },
                    { month: '10-12월', score: 80, desc: '성숙한 사랑' }
                  ].map((period, index) => (
                    <div key={index} className="text-center p-4 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20">
                      <div className="text-sm font-medium text-white/80 mb-1">{period.month}</div>
                      <div className="text-2xl font-bold text-pink-400 mb-1">{period.score}점</div>
                      <div className="text-xs text-white/60">{period.desc}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 프리미엄 서비스 안내 */}
            <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 backdrop-blur-md border border-purple-200/30 rounded-xl p-6">
                <div className="text-center">
                  <h3 className="text-xl font-bold text-white mb-3">
                    💎 더 정확한 분석을 원하신다면?
                  </h3>
                  <p className="text-white/80 mb-4">
                    프리미엄 서비스로 상대방과의 1:1 궁합, 결혼 시기, 상세 연애 가이드를 확인해보세요!
                  </p>
                  <div className="flex flex-wrap justify-center gap-3">
                    <button className="bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white px-4 py-2 rounded-lg font-medium transition-all duration-300">
                      💕 1:1 커플 궁합 (₩15,000)
                    </button>
                    <button className="border border-purple-400/50 text-purple-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                      💒 결혼운 분석 (₩12,000)
                    </button>
                    <button className="border border-pink-400/50 text-pink-300 px-4 py-2 rounded-lg bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
                      📱 연애 코칭 (₩20,000)
                    </button>
                  </div>
                  
                  <div className="mt-4 p-3 bg-yellow-500/20 backdrop-blur-sm rounded-lg border border-yellow-400/30">
                    <p className="text-sm text-yellow-200">
                      🎁 <strong>런칭 기념 특가!</strong> 지금 결제하면 30% 할인 + 무료 후속 상담 1회
                    </p>
                  </div>
                </div>
            </div>
          </div>
        )}

        {/* 하단 안내 */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>💝 연애에 관한 모든 고민, HEAL7에서 해결하세요</p>
          <p className="mt-1">🔒 개인정보는 분석 목적으로만 사용되며 절대 공개되지 않습니다</p>
        </div>

      </div>
    </div>
  );
};

export default LoveFortuneAnalysis;