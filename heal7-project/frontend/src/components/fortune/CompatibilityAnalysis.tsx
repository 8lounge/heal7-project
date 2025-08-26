import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Users, TrendingUp, AlertTriangle, Lightbulb, Target, Sparkles, Crown } from 'lucide-react';

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

export const CompatibilityAnalysis: React.FC = () => {
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
      const response = await fetch(`/api/fortune/compatibility?relationship_type=${relationshipType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          person1: {
            birth_date: person1.birthDate,
            birth_time: person1.birthTime,
            gender: person1.gender,
            name: person1.name,
            lunar_calendar: false
          },
          person2: {
            birth_date: person2.birthDate,
            birth_time: person2.birthTime,
            gender: person2.gender,
            name: person2.name,
            lunar_calendar: false
          }
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        alert('궁합 분석 중 오류가 발생했습니다.');
      }
    } catch (error) {
      console.error('분석 오류:', error);
      alert('궁합 분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        
        {/* 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            👫 궁합 분석
          </h1>
          <p className="text-gray-600 text-lg">
            두 분의 사주를 정밀 분석하여 최적의 관계 가이드를 제시합니다
          </p>
        </div>

        {/* 입력 폼 */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              궁합 분석 정보 입력
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-8">
            
            {/* 관계 유형 선택 */}
            <div>
              <label className="block text-sm font-medium mb-3">관계 유형</label>
              <div className="flex flex-wrap gap-3">
                {(['연인', '부부', '가족', '친구', '동료'] as const).map((type) => (
                  <button
                    key={type}
                    onClick={() => setRelationshipType(type)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      relationshipType === type
                        ? 'bg-purple-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            {/* 두 사람 정보 입력 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              
              {/* 첫 번째 사람 */}
              <Card className="border-blue-200 bg-blue-50">
                <CardHeader>
                  <CardTitle className="text-blue-600">👤 첫 번째 분</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">이름</label>
                    <Input
                      type="text"
                      placeholder="이름을 입력하세요"
                      value={person1.name}
                      onChange={(e) => setPerson1({...person1, name: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">생년월일</label>
                    <Input
                      type="date"
                      value={person1.birthDate}
                      onChange={(e) => setPerson1({...person1, birthDate: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">출생시간 (선택)</label>
                    <Input
                      type="time"
                      value={person1.birthTime}
                      onChange={(e) => setPerson1({...person1, birthTime: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">성별</label>
                    <div className="flex gap-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="gender1"
                          value="male"
                          checked={person1.gender === 'male'}
                          onChange={(e) => setPerson1({...person1, gender: e.target.value as 'male'})}
                          className="mr-2"
                        />
                        남성
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="gender1"
                          value="female"
                          checked={person1.gender === 'female'}
                          onChange={(e) => setPerson1({...person1, gender: e.target.value as 'female'})}
                          className="mr-2"
                        />
                        여성
                      </label>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* 두 번째 사람 */}
              <Card className="border-pink-200 bg-pink-50">
                <CardHeader>
                  <CardTitle className="text-pink-600">👤 두 번째 분</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">이름</label>
                    <Input
                      type="text"
                      placeholder="이름을 입력하세요"
                      value={person2.name}
                      onChange={(e) => setPerson2({...person2, name: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">생년월일</label>
                    <Input
                      type="date"
                      value={person2.birthDate}
                      onChange={(e) => setPerson2({...person2, birthDate: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">출생시간 (선택)</label>
                    <Input
                      type="time"
                      value={person2.birthTime}
                      onChange={(e) => setPerson2({...person2, birthTime: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">성별</label>
                    <div className="flex gap-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="gender2"
                          value="male"
                          checked={person2.gender === 'male'}
                          onChange={(e) => setPerson2({...person2, gender: e.target.value as 'male'})}
                          className="mr-2"
                        />
                        남성
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="gender2"
                          value="female"
                          checked={person2.gender === 'female'}
                          onChange={(e) => setPerson2({...person2, gender: e.target.value as 'female'})}
                          className="mr-2"
                        />
                        여성
                      </label>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
            
            <div className="text-center">
              <Button
                onClick={handleAnalyze}
                disabled={loading}
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-8 py-3 text-lg"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                    궁합 분석 중...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    궁합 분석하기
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* 결과 표시 */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            
            {/* 궁합 점수 */}
            <Card className="border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-pink-50">
              <CardContent className="p-8 text-center">
                <div className="mb-6">
                  <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-r ${getScoreColor(result.compatibility_score)} text-white text-4xl font-bold shadow-lg mb-4`}>
                    {result.compatibility_score}
                  </div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-2">
                    {getScoreText(result.compatibility_score)}
                  </h2>
                  <Badge 
                    variant="outline" 
                    className={`text-lg px-4 py-2 border-purple-400 text-purple-600`}
                  >
                    <Crown className="w-4 h-4 mr-1" />
                    {relationshipType} 궁합
                  </Badge>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-semibold text-gray-800 mb-3">종합 평가</h3>
                  <p className="text-gray-700 text-lg leading-relaxed">
                    {result.overall_assessment}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* 강점과 도전 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="border-green-200 bg-green-50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-700">
                    <TrendingUp className="w-5 h-5" />
                    관계의 강점
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {result.strengths.map((strength, index) => (
                      <div key={index} className="flex items-start gap-3 bg-white rounded-lg p-3 shadow-sm">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        <p className="text-gray-700">{strength}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-orange-200 bg-orange-50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-orange-700">
                    <AlertTriangle className="w-5 h-5" />
                    주의할 점
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {result.challenges.map((challenge, index) => (
                      <div key={index} className="flex items-start gap-3 bg-white rounded-lg p-3 shadow-sm">
                        <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                        <p className="text-gray-700">{challenge}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 관계 개선 방법 */}
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-700">
                  <Lightbulb className="w-5 h-5" />
                  관계 개선을 위한 구체적 방법
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.improvement_tips.map((tip, index) => (
                    <div key={index} className="bg-white rounded-lg p-4 shadow-sm">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {index + 1}
                        </div>
                        <span className="font-medium text-gray-800">개선 포인트</span>
                      </div>
                      <p className="text-gray-700 text-sm">{tip}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* 장기적 전망 */}
            <Card className="border-purple-200 bg-purple-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-purple-700">
                  <Target className="w-5 h-5" />
                  장기적 관계 전망
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <p className="text-gray-700 text-lg leading-relaxed">
                    {result.long_term_outlook}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* 맞춤 서비스 추천 */}
            <Card className="bg-gradient-to-r from-purple-100 to-pink-100 border-purple-200">
              <CardContent className="p-6">
                <div className="text-center">
                  <h3 className="text-xl font-bold text-gray-800 mb-3">
                    🎯 두 분만을 위한 맞춤 서비스
                  </h3>
                  <p className="text-gray-600 mb-4">
                    더 깊이 있는 관계 분석과 개인별 맞춤 상담을 받아보세요
                  </p>
                  <div className="flex flex-wrap justify-center gap-3">
                    <Button className="bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white">
                      💕 연애 코칭 (₩25,000)
                    </Button>
                    <Button variant="outline" className="border-purple-400 text-purple-600">
                      👨‍👩‍👧‍👦 가족 궁합 (₩15,000)
                    </Button>
                    <Button variant="outline" className="border-blue-400 text-blue-600">
                      💒 결혼 상담 (₩30,000)
                    </Button>
                  </div>
                  
                  <div className="mt-4 p-3 bg-yellow-100 rounded-lg">
                    <p className="text-sm text-yellow-800">
                      💎 <strong>커플 패키지 특가!</strong> 3개 서비스 동시 신청 시 40% 할인
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* 하단 안내 */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>💫 모든 관계는 서로의 이해와 노력으로 더 아름다워집니다</p>
          <p className="mt-1">🔐 두 분의 정보는 분석 후 즉시 삭제되며 절대 보관되지 않습니다</p>
        </div>

      </div>
    </div>
  );
};

export default CompatibilityAnalysis;