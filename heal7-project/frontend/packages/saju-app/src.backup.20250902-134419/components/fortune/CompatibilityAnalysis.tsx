import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Users, TrendingUp, AlertTriangle, Lightbulb, Target, Sparkles, Crown } from 'lucide-react';

type ViewMode = 'basic' | 'cyber_fantasy';

interface CompatibilityAnalysisProps {
  viewMode: ViewMode;
}

interface Person {
  birthDate: string;
  birthTime: string;
  gender: 'male' | 'female';
  name: string;
}

interface CompatibilityResult {
  compatibility_score: number;
  overall_assessment: string;
  strengths: string[];
  challenges: string[];
  improvement_tips: string[];
  long_term_outlook: string;
}

export const CompatibilityAnalysis: React.FC<CompatibilityAnalysisProps> = ({ viewMode }) => {
  const [person1, setPerson1] = useState<Person>({
    birthDate: '',
    birthTime: '12:00',
    gender: 'male',
    name: ''
  });
  
  const [person2, setPerson2] = useState<Person>({
    birthDate: '',
    birthTime: '12:00',
    gender: 'female',
    name: ''
  });
  
  const [relationshipType, setRelationshipType] = useState<'연인' | '부부' | '가족' | '친구' | '동료'>('연인');
  const [result, setResult] = useState<CompatibilityResult | null>(null);
  const [loading, setLoading] = useState(false);

  // 동적 스타일 클래스
  const cardClass = viewMode === 'cyber_fantasy' ? 'card-crystal backdrop-blur-md' : 'card-cosmic';
  const textClass = viewMode === 'cyber_fantasy' ? 'text-cyan-100' : 'text-white';
  const accentClass = viewMode === 'cyber_fantasy' ? 'text-pink-300' : 'text-white';
  const titleClass = viewMode === 'cyber_fantasy' ? 'text-mystic' : 'text-cosmic';

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'from-green-500 to-emerald-500';
    if (score >= 80) return 'from-blue-500 to-cyan-500';
    if (score >= 70) return 'from-yellow-500 to-orange-500';
    if (score >= 60) return 'from-orange-500 to-red-500';
    return 'from-red-500 to-pink-500';
  };

  const getScoreText = (score: number) => {
    if (score >= 90) return '환상의 궁합';
    if (score >= 80) return '매우 좋은 궁합';
    if (score >= 70) return '좋은 궁합';
    if (score >= 60) return '보통 궁합';
    return '노력이 필요한 궁합';
  };

  const handleAnalyze = async () => {
    if (!person1.birthDate || !person2.birthDate) {
      alert('두 분의 생년월일을 모두 입력해주세요.');
      return;
    }

    setLoading(true);
    try {
      // 샘플 데이터로 시연
      setTimeout(() => {
        const sampleResult: CompatibilityResult = {
          compatibility_score: Math.floor(Math.random() * 40) + 60, // 60-100점
          overall_assessment: "두 분은 서로를 보완해주는 훌륭한 관계입니다. 각자의 개성을 존중하면서도 공통된 가치관을 공유하여 안정적이고 따뜻한 관계를 유지할 수 있습니다.",
          strengths: [
            "서로의 장점을 인정하고 존중하는 관계",
            "의사소통이 원활하며 갈등 해결 능력이 뛰어남",
            "공통된 관심사와 취미를 통한 유대감 형성",
            "서로에게 정신적 안정감을 주는 관계"
          ],
          challenges: [
            "때로는 너무 완벽을 추구하려 하는 경향",
            "서로의 개인 시간을 존중하는 법 학습 필요",
            "의견 차이가 있을 때 감정적으로 반응하는 경향"
          ],
          improvement_tips: [
            "정기적인 대화 시간을 가져 서로의 마음을 확인하세요",
            "작은 관심과 배려를 일상에서 실천해보세요",
            "서로의 다름을 인정하고 존중하는 마음가짐을 가지세요",
            "함께 새로운 경험을 만들어가세요"
          ],
          long_term_outlook: "두 분의 관계는 시간이 지날수록 더욱 깊어지고 성숙해질 것입니다. 서로에 대한 이해와 신뢰를 바탕으로 어떤 어려움도 함께 극복해나가실 수 있을 것입니다."
        };
        setResult(sampleResult);
        setLoading(false);
      }, 2000);
    } catch (error) {
      console.error('분석 오류:', error);
      alert('궁합 분석 중 오류가 발생했습니다.');
      setLoading(false);
    }
  };

  return (
    <motion.div 
      className="max-w-6xl mx-auto px-4 py-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
        
      {/* 헤더 */}
      <motion.div 
        className="text-center mb-8"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className={`text-3xl md:text-4xl font-bold mb-4 ${titleClass}`}>
          👫 {viewMode === 'cyber_fantasy' ? '사이버 궁합 분석' : '사주 궁합 분석'}
        </h1>
        <p className={`${textClass} opacity-80`}>
          {viewMode === 'cyber_fantasy' 
            ? '3D 크리스탈이 밝혀내는 두 영혼의 연결고리'
            : '두 분의 사주를 정밀 분석하여 최적의 관계 가이드를 제시합니다'
          }
        </p>
      </motion.div>

      {/* 입력 폼 */}
      <motion.div 
        className={`p-6 rounded-xl ${cardClass} mb-8`}
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className={`text-xl font-bold mb-6 flex items-center ${textClass}`}>
          <Users className="w-5 h-5 mr-2" />
          궁합 분석 정보 입력
        </h2>
        <div className="space-y-8">
          
          {/* 관계 유형 선택 */}
          <div>
            <label className={`block text-sm font-medium mb-3 ${textClass}`}>관계 유형</label>
            <div className="flex flex-wrap gap-3">
              {(['연인', '부부', '가족', '친구', '동료'] as const).map((type) => (
                <motion.button
                  key={type}
                  onClick={() => setRelationshipType(type)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                    relationshipType === type
                      ? viewMode === 'cyber_fantasy'
                        ? 'bg-gradient-to-r from-purple-500/80 to-pink-500/80 text-white shadow-lg'
                        : 'bg-gradient-to-r from-indigo-500/80 to-purple-500/80 text-white shadow-lg'
                      : 'bg-white/10 text-white/80 hover:bg-white/20 backdrop-blur-sm border border-white/20'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {type}
                </motion.button>
              ))}
            </div>
          </div>

          {/* 두 사람 정보 입력 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* 첫 번째 사람 */}
            <div className="bg-black/20 border border-white/20 rounded-xl p-6 backdrop-blur-sm">
              <h3 className={`text-lg font-bold mb-4 ${accentClass}`}>👤 첫 번째 분</h3>
              <div className="space-y-4">
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>이름</label>
                  <input
                    type="text"
                    placeholder="이름을 입력하세요"
                    value={person1.name}
                    onChange={(e) => setPerson1({...person1, name: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>생년월일</label>
                  <input
                    type="date"
                    value={person1.birthDate}
                    onChange={(e) => setPerson1({...person1, birthDate: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>출생시간 (선택)</label>
                  <input
                    type="time"
                    value={person1.birthTime}
                    onChange={(e) => setPerson1({...person1, birthTime: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>성별</label>
                  <div className="flex gap-4">
                    <label className={`flex items-center ${textClass}`}>
                      <input
                        type="radio"
                        name="gender1"
                        value="male"
                        checked={person1.gender === 'male'}
                        onChange={(e) => setPerson1({...person1, gender: e.target.value as 'male'})}
                        className="mr-2 text-white focus:ring-purple-500"
                      />
                      남성
                    </label>
                    <label className={`flex items-center ${textClass}`}>
                      <input
                        type="radio"
                        name="gender1"
                        value="female"
                        checked={person1.gender === 'female'}
                        onChange={(e) => setPerson1({...person1, gender: e.target.value as 'female'})}
                        className="mr-2 text-white focus:ring-purple-500"
                      />
                      여성
                    </label>
                  </div>
                </div>
              </div>
            </div>

            {/* 두 번째 사람 */}
            <div className="bg-black/20 border border-white/20 rounded-xl p-6 backdrop-blur-sm">
              <h3 className={`text-lg font-bold mb-4 ${accentClass}`}>👤 두 번째 분</h3>
              <div className="space-y-4">
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>이름</label>
                  <input
                    type="text"
                    placeholder="이름을 입력하세요"
                    value={person2.name}
                    onChange={(e) => setPerson2({...person2, name: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>생년월일</label>
                  <input
                    type="date"
                    value={person2.birthDate}
                    onChange={(e) => setPerson2({...person2, birthDate: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>출생시간 (선택)</label>
                  <input
                    type="time"
                    value={person2.birthTime}
                    onChange={(e) => setPerson2({...person2, birthTime: e.target.value})}
                    className="w-full px-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${textClass}`}>성별</label>
                  <div className="flex gap-4">
                    <label className={`flex items-center ${textClass}`}>
                      <input
                        type="radio"
                        name="gender2"
                        value="male"
                        checked={person2.gender === 'male'}
                        onChange={(e) => setPerson2({...person2, gender: e.target.value as 'male'})}
                        className="mr-2 text-white focus:ring-purple-500"
                      />
                      남성
                    </label>
                    <label className={`flex items-center ${textClass}`}>
                      <input
                        type="radio"
                        name="gender2"
                        value="female"
                        checked={person2.gender === 'female'}
                        onChange={(e) => setPerson2({...person2, gender: e.target.value as 'female'})}
                        className="mr-2 text-white focus:ring-purple-500"
                      />
                      여성
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <motion.button
              onClick={handleAnalyze}
              disabled={loading}
              className={`px-8 py-3 text-lg rounded-xl font-bold transition-all duration-300 ${
                viewMode === 'cyber_fantasy'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg'
                  : 'bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white shadow-lg'
              } disabled:opacity-50`}
              whileHover={{ scale: loading ? 1 : 1.05 }}
              whileTap={{ scale: loading ? 1 : 0.95 }}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2 inline-block"></div>
                  궁합 분석 중...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2 inline" />
                  궁합 분석하기
                </>
              )}
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* 결과 표시 */}
      <AnimatePresence>
        {result && (
          <motion.div 
            className="space-y-6 mt-8"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            transition={{ duration: 0.5 }}
          >
          
            {/* 궁합 점수 */}
            <div className={`p-8 rounded-xl ${cardClass} text-center border-2 border-white/30`}>
              <div className="mb-6">
                <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-r ${getScoreColor(result.compatibility_score)} text-white text-4xl font-bold shadow-lg mb-4`}>
                  {result.compatibility_score}
                </div>
                <h2 className={`text-2xl font-bold mb-2 ${textClass}`}>
                  {getScoreText(result.compatibility_score)}
                </h2>
                <div className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-medium ${accentClass} bg-white/10 backdrop-blur-sm border border-white/20`}>
                  <Crown className="w-4 h-4 mr-1" />
                  {relationshipType} 궁합
                </div>
              </div>
              
              <div className="bg-black/20 border border-white/20 rounded-lg p-6 backdrop-blur-sm">
                <h3 className={`font-semibold mb-3 ${textClass}`}>종합 평가</h3>
                <p className={`${textClass} opacity-90 text-lg leading-relaxed`}>
                  {result.overall_assessment}
                </p>
              </div>
            </div>

            {/* 강점과 도전 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className={`p-6 rounded-xl ${cardClass}`}>
                <h3 className={`text-lg font-bold mb-4 flex items-center ${textClass}`}>
                  <TrendingUp className="w-5 h-5 mr-2" />
                  관계의 강점
                </h3>
                <div className="space-y-3">
                  {result.strengths.map((strength, index) => (
                    <div key={index} className="flex items-start gap-3 bg-black/20 border border-white/20 rounded-lg p-3 backdrop-blur-sm">
                      <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p className={`${textClass} opacity-90`}>{strength}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className={`p-6 rounded-xl ${cardClass}`}>
                <h3 className={`text-lg font-bold mb-4 flex items-center ${textClass}`}>
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  주의할 점
                </h3>
                <div className="space-y-3">
                  {result.challenges.map((challenge, index) => (
                    <div key={index} className="flex items-start gap-3 bg-black/20 border border-white/20 rounded-lg p-3 backdrop-blur-sm">
                      <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p className={`${textClass} opacity-90`}>{challenge}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 관계 개선 방법 */}
            <div className={`p-6 rounded-xl ${cardClass}`}>
              <h3 className={`text-lg font-bold mb-4 flex items-center ${textClass}`}>
                <Lightbulb className="w-5 h-5 mr-2" />
                관계 개선을 위한 구체적 방법
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.improvement_tips.map((tip, index) => (
                  <div key={index} className="bg-black/20 border border-white/20 rounded-lg p-4 backdrop-blur-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <div className={`w-6 h-6 ${viewMode === 'cyber_fantasy' ? 'bg-purple-500' : 'bg-indigo-500'} text-white rounded-full flex items-center justify-center text-sm font-bold`}>
                        {index + 1}
                      </div>
                      <span className={`font-medium ${textClass}`}>개선 포인트</span>
                    </div>
                    <p className={`${textClass} opacity-90 text-sm`}>{tip}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* 장기적 전망 */}
            <div className={`p-6 rounded-xl ${cardClass}`}>
              <h3 className={`text-lg font-bold mb-4 flex items-center ${textClass}`}>
                <Target className="w-5 h-5 mr-2" />
                장기적 관계 전망
              </h3>
              <div className="bg-black/20 border border-white/20 rounded-lg p-6 backdrop-blur-sm">
                <p className={`${textClass} opacity-90 text-lg leading-relaxed`}>
                  {result.long_term_outlook}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 하단 안내 */}
      <div className={`mt-8 text-center ${textClass} opacity-60 text-sm`}>
        <p>💫 모든 관계는 서로의 이해와 노력으로 더 아름다워집니다</p>
        <p className="mt-1">🔐 두 분의 정보는 분석 후 즉시 삭제되며 절대 보관되지 않습니다</p>
      </div>

    </motion.div>
  );
};

export default CompatibilityAnalysis;