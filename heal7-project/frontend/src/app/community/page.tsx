'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  MessageSquare,
  Bell,
  HelpCircle,
  Star,
  TrendingUp,
  Calendar,
  User,
  Clock,
  Eye,
  Heart,
  ArrowRight,
  Search,
  Filter,
  Pin,
  ThumbsUp,
  Reply,
  Send,
  UserPlus,
  Shield
} from 'lucide-react'

const categories = [
  { id: 'all', name: '전체', count: 156, icon: Users },
  { id: 'notice', name: '공지사항', count: 12, icon: Bell },
  { id: 'qna', name: '1:1 문의', count: 89, icon: HelpCircle },
  { id: 'community', name: '자유게시판', count: 34, icon: MessageSquare },
  { id: 'review', name: '후기', count: 21, icon: Star }
]

const posts = [
  {
    id: 1,
    category: 'notice',
    title: '[공지] 3D 성향분석 v2.0 업데이트 안내',
    content: '더욱 정확하고 상세한 분석을 위해 3D 성향분석 시스템을 업데이트했습니다. 새로운 기능과 개선사항을...',
    author: 'Heal7 운영팀',
    avatar: '🏢',
    createdAt: '2025-08-10',
    views: 1245,
    likes: 89,
    replies: 15,
    isPinned: true,
    isOfficial: true,
    tags: ['업데이트', '공지사항', '3D분석']
  },
  {
    id: 2,
    category: 'review',
    title: 'AI 심리분석 받고 인생이 바뀌었어요!',
    content: '정말 놀라웠습니다. 제가 평소에 느끼던 막연한 불안감의 원인을 정확히 짚어주더라고요. 특히 맞춤 솔루션이...',
    author: '김민지',
    avatar: '👩‍💼',
    createdAt: '2025-08-09',
    views: 892,
    likes: 156,
    replies: 23,
    isPinned: false,
    isOfficial: false,
    tags: ['AI분석', '후기', '변화', '추천'],
    rating: 5
  },
  {
    id: 3,
    category: 'qna',
    title: '3D 성향분석 결과 해석 문의',
    content: '안녕하세요. 어제 3D 성향분석을 받았는데, 일부 결과에 대해 궁금한 점이 있어서 문의드립니다...',
    author: '박준호',
    avatar: '👨‍🎓',
    createdAt: '2025-08-09',
    views: 234,
    likes: 12,
    replies: 3,
    isPinned: false,
    isOfficial: false,
    tags: ['질문', '3D분석', '해석'],
    status: '답변완료'
  },
  {
    id: 4,
    category: 'community',
    title: '명상 초보자를 위한 팁 공유해요',
    content: '명상을 시작한지 3개월 된 초보입니다. 그동안 경험하면서 도움이 되었던 팁들을 공유하고 싶어요...',
    author: '이수연',
    avatar: '👩‍💻',
    createdAt: '2025-08-08',
    views: 567,
    likes: 78,
    replies: 19,
    isPinned: false,
    isOfficial: false,
    tags: ['명상', '팁', '초보자', '경험공유']
  },
  {
    id: 5,
    category: 'notice',
    title: '[이벤트] 여름 힐링 챌린지 참여하세요!',
    content: '8월 한 달간 진행되는 여름 힐링 챌린지에 참여해보세요. 매일 작은 힐링 실천으로 건강한 습관을...',
    author: 'Heal7 운영팀',
    avatar: '🏢',
    createdAt: '2025-08-07',
    views: 2134,
    likes: 234,
    replies: 67,
    isPinned: true,
    isOfficial: true,
    tags: ['이벤트', '챌린지', '여름', '힐링']
  },
  {
    id: 6,
    category: 'review',
    title: '명리학 v5.0 정말 신기해요!',
    content: '전통 명리학을 현대적으로 해석한 점이 정말 인상적이었어요. 특히 직업 적합성 분석 부분이...',
    author: '최영수',
    avatar: '👨‍💼',
    createdAt: '2025-08-07',
    views: 445,
    likes: 67,
    replies: 8,
    isPinned: false,
    isOfficial: false,
    tags: ['명리학', '후기', '정확도'],
    rating: 4
  }
]

const stats = [
  { label: '총 회원수', value: '12,890', icon: Users, color: 'text-healing-600' },
  { label: '오늘 방문자', value: '1,234', icon: Eye, color: 'text-sky-600' },
  { label: '전체 게시물', value: '2,567', icon: MessageSquare, color: 'text-purple-600' },
  { label: '해결된 문의', value: '987', icon: HelpCircle, color: 'text-green-600' }
]

const PostCard: React.FC<{ post: typeof posts[0] }> = ({ post }) => {
  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'notice': return 'bg-blue-100 text-blue-800'
      case 'qna': return 'bg-green-100 text-green-800'
      case 'review': return 'bg-yellow-100 text-yellow-800'
      case 'community': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'notice': return '공지사항'
      case 'qna': return '1:1 문의'
      case 'review': return '후기'
      case 'community': return '자유게시판'
      default: return '기타'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="group cursor-pointer border-0 shadow-md hover:shadow-lg transition-all duration-300">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-2 flex-wrap">
                {post.isPinned && <Pin className="w-4 h-4 text-healing-600" />}
                <Badge className={getCategoryColor(post.category)}>
                  {getCategoryName(post.category)}
                </Badge>
                {post.isOfficial && (
                  <Badge variant="healing">공식</Badge>
                )}
                {post.status && (
                  <Badge variant="secondary">{post.status}</Badge>
                )}
                {post.rating && (
                  <div className="flex items-center gap-1">
                    {[...Array(post.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                )}
              </div>
              
              <CardTitle className="text-lg font-semibold line-clamp-2 group-hover:text-healing-600 transition-colors">
                {post.title}
              </CardTitle>
              
              <CardDescription className="line-clamp-2">
                {post.content}
              </CardDescription>
            </div>
          </div>

          {/* Tags */}
          {post.tags && (
            <div className="flex flex-wrap gap-1 pt-2">
              {post.tags.slice(0, 3).map((tag) => (
                <Badge key={tag} variant="outline" className="text-xs">
                  #{tag}
                </Badge>
              ))}
              {post.tags.length > 3 && (
                <Badge variant="outline" className="text-xs">
                  +{post.tags.length - 3}
                </Badge>
              )}
            </div>
          )}
        </CardHeader>

        <CardContent className="pt-0">
          {/* Author & Stats */}
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <span className="text-lg">{post.avatar}</span>
              <span className="font-medium">{post.author}</span>
              <span>•</span>
              <span>{post.createdAt}</span>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                <Eye className="w-4 h-4" />
                <span>{post.views.toLocaleString()}</span>
              </div>
              <div className="flex items-center gap-1">
                <ThumbsUp className="w-4 h-4" />
                <span>{post.likes}</span>
              </div>
              <div className="flex items-center gap-1">
                <Reply className="w-4 h-4" />
                <span>{post.replies}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function CommunityPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const filteredPosts = posts.filter(post => {
    const matchesCategory = selectedCategory === 'all' || post.category === selectedCategory
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         post.content.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  return (
    <Layout>
      <div className="pt-20">
        {/* Header Section */}
        <section className="py-16 bg-gradient-to-br from-purple-50 via-healing-50 to-sky-50 dark:from-gray-900 dark:via-purple-900 dark:to-sky-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto space-y-8"
            >
              <Badge variant="healing" className="mb-4 text-base px-6 py-2">
                <Users className="w-5 h-5 mr-2" />
                HEALING COMMUNITY
              </Badge>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-8">
                <span className="bg-gradient-to-r from-purple-600 via-healing-600 to-sky-600 bg-clip-text text-transparent">
                  함께 성장하는
                </span>
                <br />
                <span className="text-gray-900 dark:text-white">
                  힐링 커뮤니티
                </span>
              </h1>
              
              <p className="text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                같은 목표를 가진 사람들과 함께 소통하고 성장하세요.
                <br className="hidden sm:block" />
                <strong className="text-healing-600">경험과 지혜</strong>를 나누며 <strong className="text-purple-600">더 나은 내일</strong>을 만들어가요
              </p>

              {/* Search Bar */}
              <div className="relative max-w-lg mx-auto mt-12">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
                <input
                  type="text"
                  placeholder="궁금한 내용을 검색해보세요..."
                  className="w-full pl-12 pr-4 py-4 text-lg border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-healing-500 focus:border-transparent bg-white shadow-md"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </motion.div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-12 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.1 * index }}
                  className="text-center"
                >
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 dark:bg-gray-800 mb-3`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Categories & Posts */}
        <section className="py-16 bg-gray-50 dark:bg-gray-800">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              {/* Categories */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="flex flex-wrap justify-center gap-4 mb-12"
              >
                {categories.map((category) => {
                  const Icon = category.icon
                  return (
                    <Button
                      key={category.id}
                      variant={selectedCategory === category.id ? "healing" : "outline"}
                      size="lg"
                      onClick={() => setSelectedCategory(category.id)}
                      className="rounded-full"
                    >
                      <Icon className="w-4 h-4 mr-2" />
                      {category.name}
                      <Badge variant="secondary" className="ml-2 text-xs">
                        {category.count}
                      </Badge>
                    </Button>
                  )
                })}
              </motion.div>

              {/* Posts */}
              <div className="space-y-6">
                {/* Pinned Posts */}
                {filteredPosts.filter(post => post.isPinned).length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                      <Pin className="w-5 h-5 text-healing-600" />
                      고정된 게시물
                    </h3>
                    <div className="space-y-4">
                      {filteredPosts
                        .filter(post => post.isPinned)
                        .map((post) => (
                          <PostCard key={`pinned-${post.id}`} post={post} />
                        ))}
                    </div>
                  </div>
                )}

                {/* Regular Posts */}
                <div className="space-y-4">
                  {filteredPosts.filter(post => post.isPinned).length > 0 && (
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      일반 게시물
                    </h3>
                  )}
                  <div className="space-y-4">
                    {filteredPosts
                      .filter(post => !post.isPinned)
                      .map((post) => (
                        <PostCard key={post.id} post={post} />
                      ))}
                  </div>
                </div>

                {filteredPosts.length === 0 && (
                  <div className="text-center py-16">
                    <MessageSquare className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-2">게시물이 없습니다</h3>
                    <p className="text-muted-foreground">다른 카테고리를 선택하거나 검색어를 변경해보세요.</p>
                  </div>
                )}
              </div>

              {/* Quick Actions */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
                <Button size="lg" className="bg-healing-600 hover:bg-healing-700">
                  <Send className="w-5 h-5 mr-2" />
                  1:1 문의하기
                </Button>
                <Button size="lg" variant="outline">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  자유 게시판 글쓰기
                </Button>
                <Button size="lg" variant="outline">
                  <Star className="w-5 h-5 mr-2" />
                  후기 작성하기
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Community Guidelines */}
        <section className="py-16 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="space-y-8"
              >
                <h2 className="text-3xl md:text-4xl font-bold">
                  건전한 커뮤니티 문화를 위해
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <Card className="text-center p-6">
                    <Heart className="w-12 h-12 text-healing-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-3">존중과 배려</h3>
                    <p className="text-muted-foreground">
                      다른 회원들의 의견을 존중하고 배려하는 마음으로 소통해주세요
                    </p>
                  </Card>
                  
                  <Card className="text-center p-6">
                    <Shield className="w-12 h-12 text-sky-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-3">개인정보 보호</h3>
                    <p className="text-muted-foreground">
                      본인과 타인의 개인정보를 보호하며 안전한 소통을 지향합니다
                    </p>
                  </Card>
                  
                  <Card className="text-center p-6">
                    <UserPlus className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-3">함께 성장</h3>
                    <p className="text-muted-foreground">
                      경험과 지혜를 나누며 함께 성장하는 공동체를 만들어가요
                    </p>
                  </Card>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-purple-600 via-healing-600 to-sky-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-3xl mx-auto space-y-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold">
                지금 바로 커뮤니티에 참여하세요!
              </h2>
              <p className="text-xl text-white/90">
                같은 목표를 가진 사람들과 함께 성장하는 여정을 시작해보세요
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="xl" variant="secondary">
                  <Users className="w-5 h-5 mr-2" />
                  회원가입하기
                </Button>
                <Button size="xl" variant="outline" className="border-white text-white hover:bg-white hover:text-healing-600">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  커뮤니티 둘러보기
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}