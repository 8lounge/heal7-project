export interface Product {
  id: number
  name: string
  description: string
  price: number
  category: string
  image_url: string | null
  stock_quantity: number
  is_active: boolean
  shipping_info: string
  created_at: string
  updated_at: string
  featured_badge?: string
  originalPrice?: number
}

export interface ProductsResponse {
  success: boolean
  products: Product[]
  total: number
  limit: number
  offset: number
  category: string
}

export interface OrderRequest {
  product_id: number
  quantity: number
  customer_name: string
  customer_email: string
  customer_phone: string
  shipping_address: string
}