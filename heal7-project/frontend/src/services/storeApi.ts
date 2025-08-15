import axios from 'axios'
import { ProductsResponse, OrderRequest } from '../types/store'
import { API_BASE_URL } from './config'

export const storeApi = {
  async getProducts(category?: string): Promise<ProductsResponse> {
    const url = category 
      ? `${API_BASE_URL}/api/store/products?category=${category}`
      : `${API_BASE_URL}/api/store/products`
    
    const response = await axios.get<ProductsResponse>(url)
    return response.data
  },

  async getProduct(id: number) {
    const response = await axios.get(`${API_BASE_URL}/api/store/products/${id}`)
    return response.data
  },

  async createOrder(orderData: OrderRequest) {
    const response = await axios.post(`${API_BASE_URL}/api/store/orders`, orderData)
    return response.data
  },

  async getFeaturedProducts(): Promise<ProductsResponse> {
    const response = await axios.get<ProductsResponse>(`${API_BASE_URL}/api/store/products/featured`)
    return response.data
  },

  async toggleFeaturedProduct(productId: number, isFeatured: boolean, badge?: string) {
    const params = new URLSearchParams()
    params.append('is_featured', isFeatured.toString())
    if (badge) params.append('badge', badge)
    
    const response = await axios.put(`${API_BASE_URL}/api/store/products/${productId}/set-featured?${params}`)
    return response.data
  }
}