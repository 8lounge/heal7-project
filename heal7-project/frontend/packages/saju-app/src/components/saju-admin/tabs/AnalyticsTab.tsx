/**
 * 📊 통계분석 탭 - 리뷰/댓글 관리 및 분석
 * @author HEAL7 Admin Team
 * @version 2.0.0
 */

import React, { useState } from 'react'
import { Star, CheckCircle, XCircle } from 'lucide-react'

export const AnalyticsTab = () => {
  const [timeRange, setTimeRange] = useState('7days')
  const [activeTab, setActiveTab] = useState('reviews')
  
  const timeRanges = [
    { key: '7days', label: '최근 7일' },
    { key: '30days', label: '최근 30일' },
    { key: '3months', label: '최근 3개월' }
  ]

  const mockReviews = [
    { id: 1, user: '김○○', service: '사주 풀이', rating: 5, content: '정말 정확하고 상세한 해석이었습니다. 감사합니다!', date: '2025-09-03', status: 'approved' },
    { id: 2, user: '이○○', service: '궁합 분석', rating: 4, content: '도움이 많이 되었어요. 추천합니다.', date: '2025-09-02', status: 'pending' },
    { id: 3, user: '박○○', service: '꿈 해몽', rating: 5, content: '꿈해석이 너무 신기하게 맞았어요!', date: '2025-09-01', status: 'approved' }
  ]

  const mockComments = [
    { id: 1, user: '최○○', article: '2025년 신년운세', content: '좋은 정보 감사합니다!', date: '2025-09-03', status: 'approved' },
    { id: 2, user: '정○○', article: '사주 기초 가이드', content: '초보자도 이해하기 쉽네요', date: '2025-09-02', status: 'pending' }
  ]

  return (
    <div className="space-y-6">
      {/* 통계 개요 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { title: '총 리뷰', value: '1,247', change: '+12%', color: 'blue' },
          { title: '평균 평점', value: '4.6', change: '+0.2', color: 'green' },
          { title: '댓글 수', value: '3,456', change: '+18%', color: 'purple' },
          { title: '대기 검토', value: '23', change: '-5', color: 'yellow' }
        ].map((stat, idx) => (
          <div key={idx} className="bg-gray-900/80 backdrop-blur-sm rounded-lg p-4 border border-gray-600/40">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-200 text-sm">{stat.title}</p>
                <p className="text-white text-xl font-bold">{stat.value}</p>
                <p className={`text-xs text-${stat.color}-400`}>{stat.change}</p>
              </div>
              <Star className={`w-6 h-6 text-${stat.color}-400`} />
            </div>
          </div>
        ))}
      </div>

      {/* 기간 선택 */}
      <div className="card-base p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white text-lg font-semibold">리뷰 & 댓글 관리</h3>
          <div className="flex gap-2">
            {timeRanges.map(range => (
              <button
                key={range.key}
                onClick={() => setTimeRange(range.key)}
                className={`px-3 py-1 rounded text-sm ${
                  timeRange === range.key
                    ? 'bg-purple-500/30 text-purple-300'
                    : 'bg-gray-900/80 text-gray-200 hover:bg-white/20'
                }`}
              >
                {range.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-4 mb-6">
          {[
            { key: 'reviews', label: '리뷰 관리' },
            { key: 'comments', label: '댓글 관리' }
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 rounded-lg border ${
                activeTab === tab.key
                  ? 'bg-purple-500/30 border-purple-400 text-purple-300'
                  : 'bg-white/5 border-gray-600/40 text-gray-200 hover:bg-gray-900/80'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* 리뷰 관리 */}
      {activeTab === 'reviews' && (
        <div className="card-base">
          <div className="p-6 border-b border-gray-600/40">
            <div className="flex items-center justify-between">
              <h4 className="text-white font-semibold">리뷰 목록</h4>
              <div className="flex gap-2">
                <button className="px-3 py-1 bg-green-600/20 border border-green-400/30 rounded text-green-400 text-sm">
                  일괄 승인
                </button>
                <button className="px-3 py-1 bg-red-600/20 border border-red-400/30 rounded text-red-400 text-sm">
                  일괄 삭제
                </button>
              </div>
            </div>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {mockReviews.map(review => (
                <div key={review.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-white font-medium">{review.user}</span>
                        <span className="text-gray-400 text-sm">{review.service}</span>
                        <div className="flex">
                          {[...Array(review.rating)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                          ))}
                        </div>
                        <span className="text-gray-400 text-sm">{review.date}</span>
                      </div>
                      <p className="text-gray-200 text-sm">{review.content}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        review.status === 'approved' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {review.status === 'approved' ? '승인됨' : '대기 중'}
                      </span>
                      {review.status === 'pending' && (
                        <div className="flex gap-1">
                          <button className="text-green-400 hover:text-green-300 p-1">
                            <CheckCircle className="w-4 h-4" />
                          </button>
                          <button className="text-red-400 hover:text-red-300 p-1">
                            <XCircle className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 댓글 관리 */}
      {activeTab === 'comments' && (
        <div className="card-base">
          <div className="p-6 border-b border-gray-600/40">
            <h4 className="text-white font-semibold">댓글 목록</h4>
          </div>
          
          <div className="p-6">
            <div className="space-y-4">
              {mockComments.map(comment => (
                <div key={comment.id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-white font-medium">{comment.user}</span>
                        <span className="text-gray-400 text-sm">→ {comment.article}</span>
                        <span className="text-gray-400 text-sm">{comment.date}</span>
                      </div>
                      <p className="text-gray-200 text-sm">{comment.content}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        comment.status === 'approved' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {comment.status === 'approved' ? '승인됨' : '대기 중'}
                      </span>
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