'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Layout } from '@/components/layout/Layout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ShoppingBag, 
  Star, 
  Heart,
  BookOpen,
  Sparkles,
  Filter,
  Search,
  ArrowRight,
  ShoppingCart,
  Eye,
  Package
} from 'lucide-react'

const categories = [
  { id: 'all', name: '전체', count: 24 },
  { id: 'books', name: '도서', count: 12 },
  { id: 'wellness', name: '웰니스 용품', count: 8 },
  { id: 'meditation', name: '명상 도구', count: 4 }
]

const products = [
  {
    id: 1,
    name: '3D 성향분석 완벽 가이드북',
    description: '자신을 이해하는 첫 번째 단계, 3D 성향분석의 모든 것',
    price: 28000,
    originalPrice: 35000,
    image: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop',
    category: 'books',
    rating: 4.9,
    reviews: 156,
    badge: 'BEST',
    tags: ['성향분석', '자기계발', '심리학']
  },
  {
    id: 2,
    name: '명상용 아로마 디퓨저 세트',
    description: '마음의 평화를 찾는 힐링 아로마 디퓨저와 에센셜 오일',
    price: 89000,
    originalPrice: null,
    image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop',
    category: 'meditation',
    rating: 4.8,
    reviews: 89,
    badge: 'NEW',
    tags: ['명상', '아로마', '힐링']
  },
  {
    id: 3,
    name: 'AI 심리분석 워크북',
    description: 'AI 기반 심리분석 결과를 활용한 실전 워크북',
    price: 22000,
    originalPrice: null,
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop',
    category: 'books',
    rating: 4.7,
    reviews: 203,
    badge: 'HOT',
    tags: ['AI분석', '워크북', '실전']
  },
  {
    id: 4,
    name: '힐링 크리스탈 스타터 키트',
    description: '에너지 밸런싱을 위한 천연 크리스탈 7종 세트',
    price: 145000,
    originalPrice: 180000,
    image: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop',
    category: 'wellness',
    rating: 4.6,
    reviews: 67,
    badge: null,
    tags: ['크리스탈', '에너지', '밸런싱']
  },
  {
    id: 5,
    name: '명리학 기초 입문서',
    description: '전통 명리학부터 현대적 해석까지 체계적 학습서',
    price: 32000,
    originalPrice: null,
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
    category: 'books',
    rating: 4.9,
    reviews: 124,
    badge: null,
    tags: ['명리학', '전통', '입문서']
  },
  {
    id: 6,
    name: '요가 매트 & 소품 세트',
    description: '프리미엄 천연 요가매트와 명상용 소품 패키지',
    price: 78000,
    originalPrice: 95000,
    image: 'https://images.unsplash.com/photo-1506629905607-d13b4d00e3c5?w=400&h=300&fit=crop',
    category: 'wellness',
    rating: 4.8,
    reviews: 91,
    badge: null,
    tags: ['요가', '명상', '프리미엄']
  }
]

const ProductCard: React.FC<{ product: typeof products[0] }> = ({ product }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="group cursor-pointer border-0 shadow-lg hover:shadow-xl transition-all duration-300">
        <div className="relative overflow-hidden rounded-t-xl">
          <div
            className="aspect-[4/3] bg-cover bg-center group-hover:scale-105 transition-transform duration-300"
            style={{ backgroundImage: `url(${product.image})` }}
          />
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300" />
          
          {/* Badge */}
          {product.badge && (
            <Badge 
              variant={product.badge === 'BEST' ? 'healing' : product.badge === 'HOT' ? 'destructive' : 'secondary'}
              className="absolute top-3 left-3"
            >
              {product.badge}
            </Badge>
          )}
          
          {/* Quick Actions */}
          <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="flex flex-col gap-2">
              <Button size="icon" variant="secondary" className="w-8 h-8 rounded-full">
                <Heart className="w-4 h-4" />
              </Button>
              <Button size="icon" variant="secondary" className="w-8 h-8 rounded-full">
                <Eye className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
        
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="text-lg font-semibold line-clamp-2 group-hover:text-healing-600 transition-colors">
              {product.name}
            </CardTitle>
            <div className="flex items-center gap-1 text-sm text-yellow-500 shrink-0">
              <Star className="w-4 h-4 fill-current" />
              <span className="font-medium">{product.rating}</span>
            </div>
          </div>
          <CardDescription className="line-clamp-2">
            {product.description}
          </CardDescription>
        </CardHeader>
        
        <CardContent className="pt-0">
          <div className="flex flex-wrap gap-1 mb-4">
            {product.tags.slice(0, 2).map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
          
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-healing-600">
                {product.price.toLocaleString()}원
              </span>
              {product.originalPrice && (
                <span className="text-sm text-muted-foreground line-through">
                  {product.originalPrice.toLocaleString()}원
                </span>
              )}
            </div>
            <span className="text-sm text-muted-foreground">
              리뷰 {product.reviews}개
            </span>
          </div>
          
          <Button className="w-full bg-healing-600 hover:bg-healing-700">
            <ShoppingCart className="w-4 h-4 mr-2" />
            장바구니에 담기
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function StorePage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  return (
    <Layout>
      <div className="pt-20">
        {/* Header Section */}
        <section className="py-16 bg-gradient-to-br from-healing-50 via-sky-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-3xl mx-auto space-y-6"
            >
              <Badge variant="healing" className="mb-4">
                <ShoppingBag className="w-4 h-4 mr-2" />
                HEALING STORE
              </Badge>
              
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
                <span className="bg-gradient-to-r from-healing-600 to-sky-600 bg-clip-text text-transparent">
                  힐링 스토어
                </span>
              </h1>
              
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                마음의 평화와 성장을 위한 엄선된 상품들을 만나보세요.
                <br className="hidden sm:block" />
                전문가가 추천하는 힐링 도구와 지식을 한 곳에서 찾으실 수 있습니다.
              </p>

              {/* Search Bar */}
              <div className="relative max-w-md mx-auto mt-8">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <input
                  type="text"
                  placeholder="상품을 검색해보세요..."
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-healing-500 focus:border-transparent"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </motion.div>
          </div>
        </section>

        {/* Categories & Products */}
        <section className="py-16 bg-white dark:bg-gray-900">
          <div className="container mx-auto px-4">
            {/* Category Filter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-wrap justify-center gap-4 mb-12"
            >
              {categories.map((category) => (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? "healing" : "outline"}
                  size="lg"
                  onClick={() => setSelectedCategory(category.id)}
                  className="rounded-full"
                >
                  {category.name}
                  <Badge variant="secondary" className="ml-2 text-xs">
                    {category.count}
                  </Badge>
                </Button>
              ))}
            </motion.div>

            {/* Products Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {filteredProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>

            {filteredProducts.length === 0 && (
              <div className="text-center py-16">
                <Package className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">검색 결과가 없습니다</h3>
                <p className="text-muted-foreground">다른 검색어나 카테고리를 선택해보세요.</p>
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-healing-600 to-sky-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="max-w-3xl mx-auto space-y-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold">
                나만의 힐링 여정을 시작하세요
              </h2>
              <p className="text-xl text-healing-100">
                전문가가 엄선한 힐링 상품으로 더 나은 삶을 만들어가세요
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="xl" variant="secondary">
                  <Sparkles className="w-5 h-5 mr-2" />
                  3D 성향분석 받기
                </Button>
                <Button size="xl" variant="outline" className="border-white text-white hover:bg-white hover:text-healing-600">
                  <BookOpen className="w-5 h-5 mr-2" />
                  아카데미 둘러보기
                </Button>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </Layout>
  )
}