/**
 * 📝 콘텐츠관리 탭 - 매거진, 상품, 스토어 관리
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { Plus, Edit, Trash2 } from 'lucide-react'

export const ContentManagementTab = () => {
  const [contentType, setContentType] = useState('magazine')
  
  const contentTypes = [
    { key: 'magazine', label: '매거진 관리', count: 245 },
    { key: 'products', label: '상품 관리', count: 89 },
    { key: 'store', label: '스토어 관리', count: 12 }
  ]

  const mockContent = {
    magazine: [
      { id: 1, title: '2025년 신년운세 특집', author: '운세마스터', views: 15420, status: 'published', date: '2025-01-01' },
      { id: 2, title: '사주로 보는 연애운 가이드', author: '사주전문가', views: 8960, status: 'draft', date: '2025-01-15' }
    ],
    products: [
      { id: 1, name: '프리미엄 사주 풀이', price: 30000, sales: 156, status: 'active', category: '사주' },
      { id: 2, name: '궁합 분석 서비스', price: 25000, sales: 89, status: 'active', category: '궁합' }
    ],
    store: [
      { id: 1, name: '힐7 사주 본점', manager: '김관리자', revenue: 2450000, products: 15, status: 'active' },
      { id: 2, name: '프리미엄 사주샵', manager: '이관리자', revenue: 1890000, products: 8, status: 'active' }
    ]
  }

  return (
    <div className="space-y-6">
      {/* 콘텐츠 타입 선택 */}
      <div className="card-cosmic p-6">
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
        <div className="card-cosmic">
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

      {/* 상품 관리 */}
      {contentType === 'products' && (
        <div className="card-cosmic">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">상품 관리</h4>
              <button className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30">
                <Plus className="w-4 h-4 mr-2 inline" />
                새 상품 등록
              </button>
            </div>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {mockContent.products.map(product => (
                <div key={product.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h5 className="text-white font-semibold mb-1">{product.name}</h5>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span>가격: {product.price.toLocaleString()}원</span>
                        <span>판매량: {product.sales}건</span>
                        <span>카테고리: {product.category}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400">활성</span>
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

      {/* 스토어 관리 */}
      {contentType === 'store' && (
        <div className="card-cosmic">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">스토어 관리</h4>
              <button className="px-4 py-2 bg-green-600/20 border border-green-400/30 rounded-lg text-green-400 hover:bg-green-600/30">
                <Plus className="w-4 h-4 mr-2 inline" />
                새 스토어 등록
              </button>
            </div>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {mockContent.store.map(store => (
                <div key={store.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h5 className="text-white font-semibold mb-1">{store.name}</h5>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span>담당자: {store.manager}</span>
                        <span>매출: {store.revenue.toLocaleString()}원</span>
                        <span>상품 수: {store.products}개</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400">활성</span>
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
    </div>
  )
}