/**
 * 🔮 사주엔진 탭 - 사주 해석 데이터 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Plus, Edit, Trash2 } from 'lucide-react'

export const SajuEngineTab = () => {
  const [selectedCategory, setSelectedCategory] = useState('60갑자')
  const [searchTerm, setSearchTerm] = useState('')
  
  const categories = ['60갑자', '천간(10개)', '지지(12개)', '지장간', '오행', '격국', '궁합']
  
  const mockData = {
    '60갑자': [
      { id: 1, name: '갑자', traditional: '재물운 상승, 새로운 시작', modern: '창업이나 투자에 좋은 시기', quality: 95 },
      { id: 2, name: '을축', traditional: '인내와 끈기로 성과', modern: '꾸준한 노력이 결실을 맺는 해', quality: 92 },
      { id: 3, name: '병인', traditional: '역동적 변화의 해', modern: '적극적인 도전으로 성공', quality: 88 }
    ],
    '천간(10개)': [
      { id: 1, name: '갑(甲)', element: '목', meaning: '큰 나무, 리더십', personality: '당당하고 의지가 강함' },
      { id: 2, name: '을(乙)', element: '목', meaning: '작은 나무, 유연성', personality: '섬세하고 적응력이 뛰어남' }
    ]
  }

  return (
    <div className="space-y-6">
      {/* 카테고리 선택 */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
        <h3 className="text-white text-lg font-semibold mb-4">사주 해석 데이터 관리</h3>
        <div className="flex flex-wrap gap-2 mb-4">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg border transition-all ${
                selectedCategory === category
                  ? 'bg-purple-500/30 border-purple-400 text-purple-300'
                  : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* 검색 및 필터 */}
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="해석 데이터 검색..."
              className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
            />
          </div>
          <button className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30 flex items-center gap-2">
            <Plus className="w-4 h-4" />
            새 해석 추가
          </button>
        </div>
      </div>

      {/* 데이터 표시 영역 */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20">
        <div className="p-6 border-b border-white/20">
          <h4 className="text-white font-semibold">{selectedCategory} 해석 데이터</h4>
          <p className="text-gray-300 text-sm mt-1">총 {mockData[selectedCategory]?.length || 0}개의 해석 데이터</p>
        </div>
        
        <div className="p-6">
          <div className="space-y-4">
            {mockData[selectedCategory]?.map(item => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="p-4 bg-white/5 rounded-lg border border-white/10"
              >
                <div className="flex items-center justify-between mb-3">
                  <h5 className="text-white font-semibold">{item.name}</h5>
                  <div className="flex items-center gap-2">
                    {item.quality && (
                      <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                        품질: {item.quality}점
                      </span>
                    )}
                    <button className="text-blue-400 hover:text-blue-300 p-1">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button className="text-red-400 hover:text-red-300 p-1">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {item.traditional && (
                  <div className="mb-2">
                    <span className="text-yellow-400 text-sm font-medium">전통적 해석:</span>
                    <p className="text-gray-300 text-sm mt-1">{item.traditional}</p>
                  </div>
                )}
                
                {item.modern && (
                  <div className="mb-2">
                    <span className="text-cyan-400 text-sm font-medium">현대적 해석:</span>
                    <p className="text-gray-300 text-sm mt-1">{item.modern}</p>
                  </div>
                )}
                
                {item.element && (
                  <div className="text-sm text-gray-400">
                    오행: {item.element} | 의미: {item.meaning}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}