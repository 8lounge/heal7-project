/**
 * 📝 콘텐츠관리 탭 - 매거진, 상품, 스토어 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, Package, ShoppingCart, TrendingUp, Wand2, Brain, FileText, CheckCircle } from 'lucide-react'

export const ContentManagementTab = () => {
  const [contentType, setContentType] = useState('magazine')
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [orders, setOrders] = useState([])
  const [storeStats, setStoreStats] = useState({})
  const [loading, setLoading] = useState(false)
  const [aiContent, setAiContent] = useState([])
  const [showAiGenerator, setShowAiGenerator] = useState(false)
  const [aiGenerationForm, setAiGenerationForm] = useState({
    content_type: 'magazine_article',
    topic: '',
    target_audience: 'general',
    length: 'medium',
    ai_model: 'auto',
    additional_requirements: ''
  })

  // 사주 해석 관리 상태
  const [sajuInterpretationType, setSajuInterpretationType] = useState('gapja')
  const [sajuInterpretations, setSajuInterpretations] = useState([])
  const [interpretationSummary, setInterpretationSummary] = useState(null)
  const [showInterpretationForm, setShowInterpretationForm] = useState(false)
  const [currentInterpretationForm, setCurrentInterpretationForm] = useState({
    type: 'gapja',
    data: {}
  })
  
  const contentTypes = [
    { key: 'magazine', label: '매거진 관리', count: 245 },
    { key: 'ai-content', label: 'AI 콘텐츠 생성', count: aiContent.length },
    { key: 'saju-interpretation', label: '사주 해석 등록', count: 0 },
    { key: 'products', label: '상품 관리', count: products.length },
    { key: 'store', label: '스토어 관리', count: storeStats?.categories?.total_categories || 12 }
  ]

  // AI 콘텐츠 관련 API 호출
  const fetchAiContent = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8002/api/admin/content/list', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setAiContent(data.data || [])
      }
    } catch (error) {
      console.error('AI 콘텐츠 로드 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateAiContent = async () => {
    if (!aiGenerationForm.topic.trim()) {
      alert('주제를 입력해주세요.')
      return
    }

    setLoading(true)
    try {
      const response = await fetch('http://localhost:8002/api/admin/content/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify(aiGenerationForm)
      })

      if (response.ok) {
        const data = await response.json()
        alert('AI 콘텐츠가 성공적으로 생성되었습니다!')
        setShowAiGenerator(false)
        setAiGenerationForm({
          content_type: 'magazine_article',
          topic: '',
          target_audience: 'general',
          length: 'medium',
          ai_model: 'auto',
          additional_requirements: ''
        })
        fetchAiContent() // 새로 생성된 콘텐츠 로드
      } else {
        alert('콘텐츠 생성 실패')
      }
    } catch (error) {
      console.error('AI 콘텐츠 생성 오류:', error)
      alert('콘텐츠 생성 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const reviewContent = async (contentId, action, notes = '') => {
    try {
      const response = await fetch('http://localhost:8002/api/admin/content/review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify({
          content_id: contentId,
          content_type: 'generated_content',
          review_action: action,
          review_notes: notes
        })
      })

      if (response.ok) {
        alert(`콘텐츠가 ${action === 'approve' ? '승인' : action === 'reject' ? '반려' : '수정요청'}되었습니다.`)
        fetchAiContent() // 상태 업데이트 반영
      }
    } catch (error) {
      console.error('콘텐츠 검토 오류:', error)
    }
  }

  // 사주 해석 관련 API 호출
  const fetchInterpretationSummary = async () => {
    try {
      const response = await fetch('http://localhost:8002/api/admin/saju/interpretation-summary', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setInterpretationSummary(data.data)
      }
    } catch (error) {
      console.error('해석 현황 로드 실패:', error)
    }
  }

  const fetchSajuInterpretations = async (type) => {
    setLoading(true)
    try {
      let endpoint = ''
      switch(type) {
        case 'gapja':
          endpoint = '/saju/gapja/interpretations'
          break
        case 'heavenly-stem':
          endpoint = '/saju/heavenly-stem/interpretations'
          break
        case 'earthly-branch':
          endpoint = '/saju/earthly-branch/interpretations'
          break
        case 'five-elements':
          endpoint = '/saju/five-elements/interpretations'
          break
        case 'pattern':
          endpoint = '/saju/pattern/interpretations'
          break
      }

      const response = await fetch(`http://localhost:8002/api/admin${endpoint}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setSajuInterpretations(data.data || [])
      }
    } catch (error) {
      console.error('해석 목록 로드 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const submitInterpretation = async (interpretationData) => {
    setLoading(true)
    try {
      let endpoint = ''
      switch(interpretationData.type) {
        case 'gapja':
          endpoint = '/saju/gapja/interpretation'
          break
        case 'heavenly-stem':
          endpoint = '/saju/heavenly-stem/interpretation'
          break
        case 'earthly-branch':
          endpoint = '/saju/earthly-branch/interpretation'
          break
        case 'five-elements':
          endpoint = '/saju/five-elements/interpretation'
          break
        case 'pattern':
          endpoint = '/saju/pattern/interpretation'
          break
      }

      const response = await fetch(`http://localhost:8002/api/admin${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify(interpretationData.data)
      })

      if (response.ok) {
        const result = await response.json()
        alert(result.message)
        setShowInterpretationForm(false)
        setCurrentInterpretationForm({ type: interpretationData.type, data: {} })
        fetchSajuInterpretations(interpretationData.type)
        fetchInterpretationSummary()
      } else {
        alert('해석 등록 실패')
      }
    } catch (error) {
      console.error('해석 등록 오류:', error)
      alert('해석 등록 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  // 3단계 스토어 시스템 API 호출
  const fetchStoreData = async () => {
    setLoading(true)
    try {
      // 상품 목록 조회
      const productsRes = await fetch('http://localhost:8002/api/store/products')
      if (productsRes.ok) {
        const productsData = await productsRes.json()
        setProducts(productsData)
      }
      
      // 카테고리 목록 조회
      const categoriesRes = await fetch('http://localhost:8002/api/store/categories')
      if (categoriesRes.ok) {
        const categoriesData = await categoriesRes.json()
        setCategories(categoriesData)
      }
      
      // 주문 목록 조회
      const ordersRes = await fetch('http://localhost:8002/api/store/orders')
      if (ordersRes.ok) {
        const ordersData = await ordersRes.json()
        setOrders(ordersData)
      }
      
      // 스토어 통계 조회
      const statsRes = await fetch('http://localhost:8002/api/store/stats')
      if (statsRes.ok) {
        const statsData = await statsRes.json()
        setStoreStats(statsData)
      }
    } catch (error) {
      console.error('스토어 데이터 로드 실패:', error)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    if (contentType === 'products' || contentType === 'store') {
      fetchStoreData()
    } else if (contentType === 'ai-content') {
      fetchAiContent()
    } else if (contentType === 'saju-interpretation') {
      fetchInterpretationSummary()
      fetchSajuInterpretations(sajuInterpretationType)
    }
  }, [contentType])

  useEffect(() => {
    if (contentType === 'saju-interpretation') {
      fetchSajuInterpretations(sajuInterpretationType)
    }
  }, [sajuInterpretationType])

  const mockContent = {
    magazine: [
      { id: 1, title: '2025년 신년운세 특집', author: '운세마스터', views: 15420, status: 'published', date: '2025-01-01' },
      { id: 2, title: '사주로 보는 연애운 가이드', author: '사주전문가', views: 8960, status: 'draft', date: '2025-01-15' }
    ]
  }

  return (
    <div className="space-y-6">
      {/* 콘텐츠 타입 선택 */}
      <div className="card-base p-6">
        <h3 className="text-white text-lg font-semibold mb-4">콘텐츠 관리</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {contentTypes.map(type => (
            <button
              key={type.key}
              onClick={() => setContentType(type.key)}
              className={`p-4 rounded-lg border transition-all text-left ${
                contentType === type.key
                  ? 'bg-purple-500/30 border-purple-400'
                  : 'bg-white/5 border-gray-600/40 hover:bg-gray-900/80'
              }`}
            >
              <div className="text-white font-semibold">{type.count}</div>
              <div className="text-gray-200 text-sm">{type.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* 매거진 관리 */}
      {contentType === 'magazine' && (
        <div className="card-base">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">매거진 관리</h4>
              <button className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30">
                <Plus className="w-4 h-4 mr-2 inline" />
                새 글 작성
              </button>
            </div>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {mockContent.magazine.map(article => (
                <div key={article.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h5 className="text-white font-semibold mb-1">{article.title}</h5>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span>작성자: {article.author}</span>
                        <span>조회수: {article.views.toLocaleString()}</span>
                        <span>작성일: {article.date}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        article.status === 'published' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {article.status === 'published' ? '발행됨' : '임시저장'}
                      </span>
                      <button className="text-blue-400 hover:text-blue-300 p-1">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="text-red-400 hover:text-red-300 p-1">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* AI 콘텐츠 생성 관리 */}
      {contentType === 'ai-content' && (
        <div className="space-y-6">
          {/* AI 콘텐츠 생성 섹션 */}
          <div className="card-base">
            <div className="p-6 border-b border-gray-600/40">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-semibold flex items-center gap-2">
                  <Brain className="w-5 h-5" />
                  AI 콘텐츠 생성
                </h4>
                <button
                  onClick={() => setShowAiGenerator(!showAiGenerator)}
                  className="px-4 py-2 bg-purple-600/20 border border-purple-400/30 rounded-lg text-purple-400 hover:bg-purple-600/30"
                >
                  <Wand2 className="w-4 h-4 mr-2 inline" />
                  새 콘텐츠 생성
                </button>
              </div>
            </div>

            {/* AI 생성 폼 */}
            {showAiGenerator && (
              <div className="p-6 border-b border-gray-600/40 bg-purple-900/10">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">콘텐츠 유형</label>
                    <select
                      value={aiGenerationForm.content_type}
                      onChange={(e) => setAiGenerationForm({...aiGenerationForm, content_type: e.target.value})}
                      className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                    >
                      <option value="magazine_article">매거진 아티클</option>
                      <option value="interpretation_template">해석 템플릿</option>
                      <option value="fortune_guide">운세 가이드</option>
                      <option value="compatibility_guide">궁합 가이드</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">AI 모델</label>
                    <select
                      value={aiGenerationForm.ai_model}
                      onChange={(e) => setAiGenerationForm({...aiGenerationForm, ai_model: e.target.value})}
                      className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                    >
                      <option value="auto">자동 선택</option>
                      <option value="gpt4o">GPT-4o</option>
                      <option value="gemini">Gemini 2.0</option>
                      <option value="claude">Claude</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">대상 독자</label>
                    <select
                      value={aiGenerationForm.target_audience}
                      onChange={(e) => setAiGenerationForm({...aiGenerationForm, target_audience: e.target.value})}
                      className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                    >
                      <option value="general">일반</option>
                      <option value="beginner">초심자</option>
                      <option value="advanced">고급자</option>
                      <option value="professional">전문가</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">길이</label>
                    <select
                      value={aiGenerationForm.length}
                      onChange={(e) => setAiGenerationForm({...aiGenerationForm, length: e.target.value})}
                      className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                    >
                      <option value="short">짧음 (500단어)</option>
                      <option value="medium">보통 (1000단어)</option>
                      <option value="long">길게 (2000단어)</option>
                    </select>
                  </div>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-300 mb-2">주제</label>
                  <input
                    type="text"
                    value={aiGenerationForm.topic}
                    onChange={(e) => setAiGenerationForm({...aiGenerationForm, topic: e.target.value})}
                    placeholder="예: 2025년 을사년 신년운세 전망"
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                  />
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-300 mb-2">추가 요구사항</label>
                  <textarea
                    value={aiGenerationForm.additional_requirements}
                    onChange={(e) => setAiGenerationForm({...aiGenerationForm, additional_requirements: e.target.value})}
                    placeholder="특별한 스타일이나 포함할 내용이 있다면 입력하세요"
                    rows="3"
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={generateAiContent}
                    disabled={loading}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
                  >
                    {loading ? '생성 중...' : 'AI 콘텐츠 생성'}
                  </button>
                  <button
                    onClick={() => setShowAiGenerator(false)}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                  >
                    취소
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* 생성된 AI 콘텐츠 목록 */}
          <div className="card-base">
            <div className="p-6 border-b border-gray-600/40">
              <h4 className="text-white font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5" />
                생성된 콘텐츠 ({aiContent.length})
              </h4>
            </div>

            <div className="p-6">
              {loading ? (
                <div className="text-center py-8 text-gray-400">로딩 중...</div>
              ) : aiContent.length > 0 ? (
                <div className="space-y-4">
                  {aiContent.map(content => (
                    <div key={content.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h5 className="text-white font-semibold mb-1">{content.topic}</h5>
                          <div className="flex items-center gap-4 text-sm text-gray-400 mb-2">
                            <span>유형: {content.content_type?.replace('_', ' ')}</span>
                            <span>모델: {content.ai_model}</span>
                            <span>단어수: {content.word_count}</span>
                            <span>작성일: {new Date(content.created_at).toLocaleDateString()}</span>
                          </div>
                          {content.content_text && (
                            <p className="text-gray-300 text-sm line-clamp-3 mb-2">
                              {content.content_text.substring(0, 200)}...
                            </p>
                          )}
                        </div>
                        <div className="flex items-center gap-2 ml-4">
                          <span className={`px-2 py-1 rounded text-xs ${
                            content.status === 'approved' ? 'bg-green-500/20 text-green-400' :
                            content.status === 'rejected' ? 'bg-red-500/20 text-red-400' :
                            content.status === 'revision_requested' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-gray-500/20 text-gray-400'
                          }`}>
                            {content.status === 'approved' ? '승인' :
                             content.status === 'rejected' ? '반려' :
                             content.status === 'revision_requested' ? '수정요청' : '검토대기'}
                          </span>
                          {content.status === 'draft' && (
                            <>
                              <button
                                onClick={() => reviewContent(content.id, 'approve')}
                                className="text-green-400 hover:text-green-300 p-1"
                                title="승인"
                              >
                                <CheckCircle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => reviewContent(content.id, 'reject')}
                                className="text-red-400 hover:text-red-300 p-1"
                                title="반려"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </>
                          )}
                          <button className="text-blue-400 hover:text-blue-300 p-1">
                            <Edit className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  생성된 AI 콘텐츠가 없습니다.
                  <br />
                  <button
                    onClick={() => setShowAiGenerator(true)}
                    className="mt-2 text-purple-400 hover:text-purple-300"
                  >
                    첫 콘텐츠를 생성해보세요
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* 사주 해석 등록 관리 */}
      {contentType === 'saju-interpretation' && (
        <div className="space-y-6">
          {/* 해석 등록 현황 요약 */}
          <div className="card-base p-6">
            <h3 className="text-white text-lg font-semibold mb-4">사주 해석 등록 현황</h3>
            {interpretationSummary ? (
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                {Object.entries(interpretationSummary).map(([key, data]) => (
                  <div key={key} className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="text-center">
                      <h4 className="text-white font-semibold mb-2">
                        {key === 'gapja' ? '60갑자' :
                         key === 'heavenly_stems' ? '천간' :
                         key === 'earthly_branches' ? '지지' :
                         key === 'five_elements' ? '오행' :
                         key === 'patterns' ? '격국' : key}
                      </h4>
                      <div className="mb-2">
                        <span className="text-2xl font-bold text-blue-400">{data.total}</span>
                        <span className="text-gray-400 text-sm">/{data.expected}</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${data.completion_rate}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-gray-400 mt-1">{data.completion_rate}% 완료</div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-4 text-gray-400">현황 정보를 불러오는 중...</div>
            )}
          </div>

          {/* 해석 유형 선택 및 관리 */}
          <div className="card-base">
            <div className="p-6 border-b border-gray-600/40">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-semibold">사주 해석 등록 관리</h4>
                <button
                  onClick={() => setShowInterpretationForm(!showInterpretationForm)}
                  className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30"
                >
                  <Plus className="w-4 h-4 mr-2 inline" />
                  새 해석 등록
                </button>
              </div>

              {/* 해석 유형 탭 */}
              <div className="flex flex-wrap gap-2 mt-4">
                {[
                  { key: 'gapja', label: '60갑자' },
                  { key: 'heavenly-stem', label: '천간' },
                  { key: 'earthly-branch', label: '지지' },
                  { key: 'five-elements', label: '오행' },
                  { key: 'pattern', label: '격국' }
                ].map(type => (
                  <button
                    key={type.key}
                    onClick={() => setSajuInterpretationType(type.key)}
                    className={`px-3 py-1 rounded-lg text-sm transition-all ${
                      sajuInterpretationType === type.key
                        ? 'bg-purple-500/30 border border-purple-400 text-purple-300'
                        : 'bg-gray-700/50 border border-gray-600 text-gray-300 hover:bg-gray-600/50'
                    }`}
                  >
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 해석 등록 폼 */}
            {showInterpretationForm && (
              <div className="p-6 border-b border-gray-600/40 bg-green-900/10">
                <SajuInterpretationForm
                  interpretationType={sajuInterpretationType}
                  onSubmit={submitInterpretation}
                  onCancel={() => setShowInterpretationForm(false)}
                  loading={loading}
                />
              </div>
            )}

            {/* 해석 목록 */}
            <div className="p-6">
              <h5 className="text-white font-semibold mb-4">
                {sajuInterpretationType === 'gapja' ? '60갑자' :
                 sajuInterpretationType === 'heavenly-stem' ? '천간' :
                 sajuInterpretationType === 'earthly-branch' ? '지지' :
                 sajuInterpretationType === 'five-elements' ? '오행' :
                 sajuInterpretationType === 'pattern' ? '격국' : ''} 해석 목록 ({sajuInterpretations.length})
              </h5>

              {loading ? (
                <div className="text-center py-8 text-gray-400">로딩 중...</div>
              ) : sajuInterpretations.length > 0 ? (
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {sajuInterpretations.map(interpretation => (
                    <div key={interpretation.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h6 className="text-white font-semibold mb-1">
                            {interpretation.gapja_code || interpretation.stem_code ||
                             interpretation.branch_code || interpretation.element ||
                             interpretation.pattern_name || 'Unknown'}
                            {interpretation.interpretation_title && ` - ${interpretation.interpretation_title}`}
                          </h6>
                          <p className="text-gray-300 text-sm line-clamp-2 mb-2">
                            {interpretation.basic_meaning || interpretation.basic_characteristics ||
                             interpretation.basic_interpretation || '기본 해석 없음'}
                          </p>
                          <div className="flex items-center gap-4 text-xs text-gray-400">
                            {interpretation.category && <span>카테고리: {interpretation.category}</span>}
                            {interpretation.element && <span>오행: {interpretation.element}</span>}
                            {interpretation.yin_yang && <span>음양: {interpretation.yin_yang}</span>}
                            <span>등록일: {new Date(interpretation.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 ml-4">
                          <button className="text-blue-400 hover:text-blue-300 p-1">
                            <Edit className="w-4 h-4" />
                          </button>
                          <button className="text-red-400 hover:text-red-300 p-1">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  등록된 해석이 없습니다.
                  <br />
                  <button
                    onClick={() => setShowInterpretationForm(true)}
                    className="mt-2 text-green-400 hover:text-green-300"
                  >
                    첫 해석을 등록해보세요
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* 상품 관리 */}
      {contentType === 'products' && (
        <div className="card-base">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold flex items-center gap-2">
                <Package className="w-5 h-5" />
                상품 관리 ({products.length}개)
              </h4>
              <button className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30">
                <Plus className="w-4 h-4 mr-2 inline" />
                새 상품 등록
              </button>
            </div>
          </div>
          
          <div className="p-6">
            {loading ? (
              <div className="text-center py-8 text-gray-400">로딩 중...</div>
            ) : products.length > 0 ? (
              <div className="space-y-4">
                {products.map(product => (
                  <div key={product.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h5 className="text-white font-semibold mb-1">{product.name}</h5>
                        <div className="flex items-center gap-4 text-sm text-gray-400">
                          <span>가격: {product.price?.toLocaleString()}원</span>
                          {product.sale_price && (
                            <span className="text-green-400">할인가: {product.sale_price.toLocaleString()}원</span>
                          )}
                          <span>재고: {product.stock_quantity}개</span>
                          <span>SKU: {product.sku || 'N/A'}</span>
                        </div>
                        {product.short_description && (
                          <p className="text-gray-300 text-sm mt-1">{product.short_description}</p>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          product.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                        }`}>
                          {product.is_active ? '활성' : '비활성'}
                        </span>
                        {product.is_digital && (
                          <span className="px-2 py-1 rounded text-xs bg-blue-500/20 text-blue-400">디지털</span>
                        )}
                        <button className="text-blue-400 hover:text-blue-300 p-1">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="text-red-400 hover:text-red-300 p-1">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-400">
                등록된 상품이 없습니다.
                <br />
                <button className="mt-2 text-green-400 hover:text-green-300">첫 상품을 등록해보세요</button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 스토어 관리 */}
      {contentType === 'store' && (
        <div className="space-y-6">
          {/* 스토어 통계 대시보드 */}
          <div className="card-base p-6">
            <h4 className="text-white font-semibold flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5" />
              스토어 통계
            </h4>
            
            {loading ? (
              <div className="text-center py-4 text-gray-400">통계 로딩 중...</div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center gap-3">
                    <Package className="w-8 h-8 text-blue-400" />
                    <div>
                      <div className="text-2xl font-bold text-white">{storeStats?.products?.total_products || 0}</div>
                      <div className="text-sm text-gray-400">전체 상품</div>
                      <div className="text-xs text-green-400">{storeStats?.products?.active_products || 0}개 활성</div>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center gap-3">
                    <ShoppingCart className="w-8 h-8 text-green-400" />
                    <div>
                      <div className="text-2xl font-bold text-white">{storeStats?.orders?.total_orders || 0}</div>
                      <div className="text-sm text-gray-400">전체 주문</div>
                      <div className="text-xs text-blue-400">{storeStats?.orders?.completed_orders || 0}건 완료</div>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center gap-3">
                    <TrendingUp className="w-8 h-8 text-purple-400" />
                    <div>
                      <div className="text-2xl font-bold text-white">{(storeStats?.orders?.total_revenue || 0).toLocaleString()}</div>
                      <div className="text-sm text-gray-400">총 매출 (원)</div>
                      <div className="text-xs text-purple-400">실시간 집계</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* 최근 주문 관리 */}
          <div className="card-base">
            <div className="p-6 border-b border-gray-600/40">
              <div className="flex items-center justify-between">
                <h4 className="text-white font-semibold flex items-center gap-2">
                  <ShoppingCart className="w-5 h-5" />
                  최근 주문 ({orders.length}건)
                </h4>
                <button className="px-4 py-2 bg-blue-600/20 border border-blue-400/30 rounded-lg text-blue-400 hover:bg-blue-600/30">
                  전체 주문 보기
                </button>
              </div>
            </div>
            
            <div className="p-6">
              {loading ? (
                <div className="text-center py-8 text-gray-400">주문 데이터 로딩 중...</div>
              ) : orders.length > 0 ? (
                <div className="space-y-4">
                  {orders.slice(0, 5).map(order => (
                    <div key={order.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h5 className="text-white font-semibold mb-1">주문번호: {order.order_number}</h5>
                          <div className="flex items-center gap-4 text-sm text-gray-400">
                            <span>금액: {order.total_amount?.toLocaleString()}원</span>
                            <span>결제: {order.payment_method}</span>
                            <span>상품: {order.items?.length || 0}개</span>
                            <span>주문일: {new Date(order.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 rounded text-xs ${
                            order.status === 'delivered' ? 'bg-green-500/20 text-green-400' :
                            order.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-blue-500/20 text-blue-400'
                          }`}>
                            {order.status === 'delivered' ? '배송완료' :
                             order.status === 'pending' ? '대기중' : order.status}
                          </span>
                          <button className="text-blue-400 hover:text-blue-300 p-1">
                            <Edit className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  아직 주문이 없습니다.
                  <br />
                  <span className="text-sm">상품이 등록되면 주문이 들어올 수 있습니다.</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// 사주 해석 등록 폼 컴포넌트
const SajuInterpretationForm = ({ interpretationType, onSubmit, onCancel, loading }) => {
  const [formData, setFormData] = useState({})

  // 해석 유형별 기본 폼 구조
  const getFormFields = () => {
    switch (interpretationType) {
      case 'gapja':
        return {
          gapja_code: '',
          gapja_index: 1,
          category: 'year',
          interpretation_title: '',
          basic_meaning: '',
          detailed_interpretation: '',
          personality_traits: '',
          career_fortune: '',
          health_fortune: '',
          relationship_fortune: '',
          wealth_fortune: ''
        }
      case 'heavenly-stem':
        return {
          stem_code: '',
          stem_index: 1,
          element: '목',
          yin_yang: '양',
          basic_meaning: '',
          personality_traits: '',
          strengths: '',
          weaknesses: '',
          compatible_stems: '',
          incompatible_stems: '',
          seasonal_influence: ''
        }
      case 'earthly-branch':
        return {
          branch_code: '',
          branch_index: 1,
          animal_sign: '',
          element: '목',
          season: '',
          direction: '',
          time_period: '',
          basic_meaning: '',
          personality_traits: '',
          hidden_stems: '',
          compatible_branches: '',
          incompatible_branches: ''
        }
      case 'five-elements':
        return {
          element: '목',
          element_index: 1,
          basic_characteristics: '',
          personality_traits: '',
          body_parts: '',
          emotions: '',
          colors: '',
          directions: '',
          seasons: '',
          organs: '',
          taste: '',
          generates_element: '',
          destroys_element: '',
          career_fields: '',
          fortune_analysis: ''
        }
      case 'pattern':
        return {
          pattern_name: '',
          pattern_type: '',
          pattern_code: '',
          formation_conditions: '',
          basic_interpretation: '',
          personality_analysis: '',
          career_fortune: '',
          wealth_fortune: '',
          relationship_fortune: '',
          health_fortune: '',
          life_phases: '',
          favorable_elements: '',
          unfavorable_elements: '',
          compatibility_patterns: ''
        }
      default:
        return {}
    }
  }

  useEffect(() => {
    setFormData(getFormFields())
  }, [interpretationType])

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.basic_meaning && !formData.basic_characteristics && !formData.basic_interpretation) {
      alert('기본 의미는 필수 항목입니다.')
      return
    }
    onSubmit({ type: interpretationType, data: formData })
  }

  const renderFormFields = () => {
    switch (interpretationType) {
      case 'gapja':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">갑자 코드 *</label>
                <input
                  type="text"
                  value={formData.gapja_code || ''}
                  onChange={(e) => handleChange('gapja_code', e.target.value)}
                  placeholder="예: 갑자"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">갑자 순서 (1-60) *</label>
                <input
                  type="number"
                  min="1"
                  max="60"
                  value={formData.gapja_index || 1}
                  onChange={(e) => handleChange('gapja_index', parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">카테고리 *</label>
                <select
                  value={formData.category || 'year'}
                  onChange={(e) => handleChange('category', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                >
                  <option value="year">년주</option>
                  <option value="month">월주</option>
                  <option value="day">일주</option>
                  <option value="hour">시주</option>
                </select>
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">해석 제목</label>
              <input
                type="text"
                value={formData.interpretation_title || ''}
                onChange={(e) => handleChange('interpretation_title', e.target.value)}
                placeholder="예: 갑자일주의 특성"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">기본 의미 *</label>
              <textarea
                value={formData.basic_meaning || ''}
                onChange={(e) => handleChange('basic_meaning', e.target.value)}
                placeholder="갑자의 기본적인 의미를 입력하세요"
                rows="3"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">성격 특성</label>
                <textarea
                  value={formData.personality_traits || ''}
                  onChange={(e) => handleChange('personality_traits', e.target.value)}
                  placeholder="성격적 특성을 입력하세요"
                  rows="3"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">직업운</label>
                <textarea
                  value={formData.career_fortune || ''}
                  onChange={(e) => handleChange('career_fortune', e.target.value)}
                  placeholder="직업운에 대한 해석을 입력하세요"
                  rows="3"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">건강운</label>
                <textarea
                  value={formData.health_fortune || ''}
                  onChange={(e) => handleChange('health_fortune', e.target.value)}
                  rows="2"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">인간관계운</label>
                <textarea
                  value={formData.relationship_fortune || ''}
                  onChange={(e) => handleChange('relationship_fortune', e.target.value)}
                  rows="2"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">재물운</label>
                <textarea
                  value={formData.wealth_fortune || ''}
                  onChange={(e) => handleChange('wealth_fortune', e.target.value)}
                  rows="2"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
            </div>
          </>
        )

      case 'heavenly-stem':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">천간 코드 *</label>
                <input
                  type="text"
                  value={formData.stem_code || ''}
                  onChange={(e) => handleChange('stem_code', e.target.value)}
                  placeholder="예: 갑"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">순서 (1-10) *</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.stem_index || 1}
                  onChange={(e) => handleChange('stem_index', parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">오행 *</label>
                <select
                  value={formData.element || '목'}
                  onChange={(e) => handleChange('element', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                >
                  <option value="목">목</option>
                  <option value="화">화</option>
                  <option value="토">토</option>
                  <option value="금">금</option>
                  <option value="수">수</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">음양 *</label>
                <select
                  value={formData.yin_yang || '양'}
                  onChange={(e) => handleChange('yin_yang', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                >
                  <option value="양">양</option>
                  <option value="음">음</option>
                </select>
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">기본 의미 *</label>
              <textarea
                value={formData.basic_meaning || ''}
                onChange={(e) => handleChange('basic_meaning', e.target.value)}
                placeholder="천간의 기본적인 의미를 입력하세요"
                rows="3"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">장점</label>
                <textarea
                  value={formData.strengths || ''}
                  onChange={(e) => handleChange('strengths', e.target.value)}
                  rows="3"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">약점</label>
                <textarea
                  value={formData.weaknesses || ''}
                  onChange={(e) => handleChange('weaknesses', e.target.value)}
                  rows="3"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
            </div>
          </>
        )

      case 'five-elements':
        return (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">오행 *</label>
                <select
                  value={formData.element || '목'}
                  onChange={(e) => handleChange('element', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                >
                  <option value="목">목</option>
                  <option value="화">화</option>
                  <option value="토">토</option>
                  <option value="금">금</option>
                  <option value="수">수</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">순서 (1-5) *</label>
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={formData.element_index || 1}
                  onChange={(e) => handleChange('element_index', parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">기본 특성 *</label>
              <textarea
                value={formData.basic_characteristics || ''}
                onChange={(e) => handleChange('basic_characteristics', e.target.value)}
                placeholder="오행의 기본적인 특성을 입력하세요"
                rows="3"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">관련 신체 부위</label>
                <input
                  type="text"
                  value={formData.body_parts || ''}
                  onChange={(e) => handleChange('body_parts', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">관련 감정</label>
                <input
                  type="text"
                  value={formData.emotions || ''}
                  onChange={(e) => handleChange('emotions', e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white"
                />
              </div>
            </div>
          </>
        )

      default:
        return <div className="text-gray-400">해당 해석 유형의 폼을 준비 중입니다.</div>
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h4 className="text-white font-semibold mb-4">
        {interpretationType === 'gapja' ? '60갑자' :
         interpretationType === 'heavenly-stem' ? '천간' :
         interpretationType === 'earthly-branch' ? '지지' :
         interpretationType === 'five-elements' ? '오행' :
         interpretationType === 'pattern' ? '격국' : ''} 해석 등록
      </h4>

      {renderFormFields()}

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {loading ? '등록 중...' : '해석 등록'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          취소
        </button>
      </div>
    </form>
  )
}