"""
📦 3단계 스토어 시스템 API
- 상품 카테고리, 상품, 주문 관리
- TossPayments 포인트 시스템 연동
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncpg
import uuid
import os
from decimal import Decimal

router = APIRouter(prefix="/api/store", tags=["Store System"])

# 데이터베이스 연결 설정
# Unix 소켓 사용 (암호 불필요)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ubuntu@/heal7_saju?host=/var/run/postgresql")

# ========================
# 📊 데이터 모델
# ========================

class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: int = 0

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    parent_id: Optional[str]
    sort_order: int
    is_active: bool
    created_at: datetime

class ProductCreate(BaseModel):
    category_id: str
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    price: int = Field(..., gt=0)
    sale_price: Optional[int] = Field(None, gt=0)
    sku: Optional[str] = Field(None, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)
    is_digital: bool = False
    images: Optional[List[str]] = None
    specifications: Optional[Dict[str, Any]] = None

class ProductResponse(BaseModel):
    id: str
    category_id: str
    name: str
    description: Optional[str]
    short_description: Optional[str]
    price: int
    sale_price: Optional[int]
    sku: Optional[str]
    stock_quantity: int
    is_digital: bool
    images: Optional[List[str]]
    specifications: Optional[Dict[str, Any]]
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

class OrderCreate(BaseModel):
    user_id: str
    items: List[Dict[str, Any]]  # [{"product_id": str, "quantity": int}]
    shipping_address: Optional[Dict[str, Any]] = None
    payment_method: str = "points"
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    user_id: str
    order_number: str
    status: str
    total_amount: int
    shipping_address: Optional[Dict[str, Any]]
    payment_method: str
    payment_status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[Dict[str, Any]]

# ========================
# 🗄️ 데이터베이스 연결
# ========================

async def get_db_connection():
    """비동기 PostgreSQL 연결"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 연결 실패: {str(e)}"
        )

# ========================
# 📂 카테고리 API
# ========================

@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    """상품 카테고리 목록 조회"""
    conn = await get_db_connection()
    try:
        query = """
            SELECT id, name, description, parent_id, sort_order, is_active, created_at
            FROM product_categories 
            WHERE is_active = true 
            ORDER BY sort_order, name
        """
        rows = await conn.fetch(query)
        # Convert UUID to string for JSON serialization
        result = []
        for row in rows:
            row_dict = dict(row)
            row_dict['id'] = str(row_dict['id'])
            if row_dict['parent_id']:
                row_dict['parent_id'] = str(row_dict['parent_id'])
            result.append(row_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 조회 실패: {str(e)}")
    finally:
        await conn.close()

@router.post("/categories", response_model=CategoryResponse)
async def create_category(category: CategoryCreate):
    """새 상품 카테고리 생성"""
    conn = await get_db_connection()
    try:
        category_id = str(uuid.uuid4())
        query = """
            INSERT INTO product_categories (id, name, description, parent_id, sort_order)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, name, description, parent_id, sort_order, is_active, created_at
        """
        row = await conn.fetchrow(
            query, category_id, category.name, category.description, 
            category.parent_id, category.sort_order
        )
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 생성 실패: {str(e)}")
    finally:
        await conn.close()

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: str, category: CategoryCreate):
    """상품 카테고리 수정"""
    conn = await get_db_connection()
    try:
        query = """
            UPDATE product_categories 
            SET name = $2, description = $3, parent_id = $4, sort_order = $5
            WHERE id = $1 AND is_active = true
            RETURNING id, name, description, parent_id, sort_order, is_active, created_at
        """
        row = await conn.fetchrow(
            query, category_id, category.name, category.description,
            category.parent_id, category.sort_order
        )
        if not row:
            raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 수정 실패: {str(e)}")
    finally:
        await conn.close()

@router.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    """상품 카테고리 삭제 (소프트 삭제)"""
    conn = await get_db_connection()
    try:
        query = "UPDATE product_categories SET is_active = false WHERE id = $1"
        result = await conn.execute(query, category_id)
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
        return {"message": "카테고리가 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 삭제 실패: {str(e)}")
    finally:
        await conn.close()

# ========================
# 📦 상품 API
# ========================

@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    category_id: Optional[str] = None,
    is_active: bool = True,
    limit: int = 50,
    offset: int = 0
):
    """상품 목록 조회"""
    conn = await get_db_connection()
    try:
        where_clause = "WHERE is_active = $1"
        params = [is_active]
        
        if category_id:
            where_clause += " AND category_id = $2"
            params.append(category_id)
            
        query = f"""
            SELECT id, category_id, name, description, short_description, 
                   price, sale_price, sku, stock_quantity, is_digital,
                   images, specifications, is_active, sort_order, 
                   created_at, updated_at
            FROM products 
            {where_clause}
            ORDER BY sort_order, name
            LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        params.extend([limit, offset])
        
        rows = await conn.fetch(query, *params)
        # Convert UUID to string for JSON serialization
        result = []
        for row in rows:
            row_dict = dict(row)
            row_dict['id'] = str(row_dict['id'])
            row_dict['category_id'] = str(row_dict['category_id'])
            result.append(row_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상품 조회 실패: {str(e)}")
    finally:
        await conn.close()

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """상품 상세 조회"""
    conn = await get_db_connection()
    try:
        query = """
            SELECT id, category_id, name, description, short_description, 
                   price, sale_price, sku, stock_quantity, is_digital,
                   images, specifications, is_active, sort_order, 
                   created_at, updated_at
            FROM products WHERE id = $1 AND is_active = true
        """
        row = await conn.fetchrow(query, product_id)
        if not row:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상품 조회 실패: {str(e)}")
    finally:
        await conn.close()

@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """새 상품 생성"""
    conn = await get_db_connection()
    try:
        product_id = str(uuid.uuid4())
        query = """
            INSERT INTO products (
                id, category_id, name, description, short_description,
                price, sale_price, sku, stock_quantity, is_digital,
                images, specifications
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id, category_id, name, description, short_description, 
                      price, sale_price, sku, stock_quantity, is_digital,
                      images, specifications, is_active, sort_order, 
                      created_at, updated_at
        """
        row = await conn.fetchrow(
            query, product_id, product.category_id, product.name,
            product.description, product.short_description, product.price,
            product.sale_price, product.sku, product.stock_quantity,
            product.is_digital, product.images, product.specifications
        )
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상품 생성 실패: {str(e)}")
    finally:
        await conn.close()

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductCreate):
    """상품 수정"""
    conn = await get_db_connection()
    try:
        query = """
            UPDATE products SET
                category_id = $2, name = $3, description = $4, short_description = $5,
                price = $6, sale_price = $7, sku = $8, stock_quantity = $9,
                is_digital = $10, images = $11, specifications = $12,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = $1 AND is_active = true
            RETURNING id, category_id, name, description, short_description, 
                      price, sale_price, sku, stock_quantity, is_digital,
                      images, specifications, is_active, sort_order, 
                      created_at, updated_at
        """
        row = await conn.fetchrow(
            query, product_id, product.category_id, product.name,
            product.description, product.short_description, product.price,
            product.sale_price, product.sku, product.stock_quantity,
            product.is_digital, product.images, product.specifications
        )
        if not row:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상품 수정 실패: {str(e)}")
    finally:
        await conn.close()

# ========================
# 🛒 주문 API
# ========================

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    """새 주문 생성"""
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            # 주문 번호 생성
            order_number = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
            order_id = str(uuid.uuid4())
            
            # 주문 상품 금액 계산
            total_amount = 0
            order_items_data = []
            
            for item in order.items:
                # 상품 정보 조회
                product_query = "SELECT price, sale_price, stock_quantity FROM products WHERE id = $1 AND is_active = true"
                product = await conn.fetchrow(product_query, item["product_id"])
                
                if not product:
                    raise HTTPException(status_code=404, detail=f"상품을 찾을 수 없습니다: {item['product_id']}")
                
                if product["stock_quantity"] < item["quantity"]:
                    raise HTTPException(status_code=400, detail="재고가 부족합니다")
                
                unit_price = product["sale_price"] if product["sale_price"] else product["price"]
                item_total = unit_price * item["quantity"]
                total_amount += item_total
                
                order_items_data.append({
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "unit_price": unit_price,
                    "total_price": item_total
                })
            
            # 주문 생성
            order_query = """
                INSERT INTO orders (id, user_id, order_number, total_amount, shipping_address, payment_method, notes)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id, user_id, order_number, status, total_amount, shipping_address, 
                         payment_method, payment_status, notes, created_at, updated_at
            """
            order_row = await conn.fetchrow(
                order_query, order_id, order.user_id, order_number, total_amount,
                order.shipping_address, order.payment_method, order.notes
            )
            
            # 주문 상품 생성
            for item_data in order_items_data:
                item_query = """
                    INSERT INTO order_items (id, order_id, product_id, quantity, unit_price, total_price)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """
                await conn.execute(
                    item_query, str(uuid.uuid4()), order_id, item_data["product_id"],
                    item_data["quantity"], item_data["unit_price"], item_data["total_price"]
                )
                
                # 재고 차감
                stock_query = "UPDATE products SET stock_quantity = stock_quantity - $1 WHERE id = $2"
                await conn.execute(stock_query, item_data["quantity"], item_data["product_id"])
            
            # 응답 데이터 구성
            result = dict(order_row)
            result["items"] = order_items_data
            
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주문 생성 실패: {str(e)}")
    finally:
        await conn.close()

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """주문 목록 조회"""
    conn = await get_db_connection()
    try:
        where_conditions = []
        params = []
        
        if user_id:
            where_conditions.append(f"user_id = ${len(params) + 1}")
            params.append(user_id)
            
        if status:
            where_conditions.append(f"status = ${len(params) + 1}")
            params.append(status)
            
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        query = f"""
            SELECT id, user_id, order_number, status, total_amount, shipping_address,
                   payment_method, payment_status, notes, created_at, updated_at
            FROM orders 
            {where_clause}
            ORDER BY created_at DESC
            LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        params.extend([limit, offset])
        
        rows = await conn.fetch(query, *params)
        
        # 각 주문의 상품 정보 조회
        result = []
        for row in rows:
            order_data = dict(row)
            
            items_query = """
                SELECT oi.product_id, oi.quantity, oi.unit_price, oi.total_price, p.name as product_name
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = $1
            """
            items = await conn.fetch(items_query, order_data["id"])
            order_data["items"] = [dict(item) for item in items]
            
            result.append(order_data)
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주문 조회 실패: {str(e)}")
    finally:
        await conn.close()

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """주문 상세 조회"""
    conn = await get_db_connection()
    try:
        order_query = """
            SELECT id, user_id, order_number, status, total_amount, shipping_address,
                   payment_method, payment_status, notes, created_at, updated_at
            FROM orders WHERE id = $1
        """
        order_row = await conn.fetchrow(order_query, order_id)
        
        if not order_row:
            raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
            
        # 주문 상품 조회
        items_query = """
            SELECT oi.product_id, oi.quantity, oi.unit_price, oi.total_price, p.name as product_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = $1
        """
        items = await conn.fetch(items_query, order_id)
        
        result = dict(order_row)
        result["items"] = [dict(item) for item in items]
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주문 조회 실패: {str(e)}")
    finally:
        await conn.close()

# ========================
# 📊 통계 API
# ========================

@router.get("/stats")
async def get_store_stats():
    """스토어 통계 조회"""
    conn = await get_db_connection()
    try:
        stats = {}
        
        # 상품 통계
        product_stats = await conn.fetchrow("""
            SELECT 
                COUNT(*) as total_products,
                COUNT(*) FILTER (WHERE is_active = true) as active_products,
                COUNT(*) FILTER (WHERE stock_quantity = 0) as out_of_stock
            FROM products
        """)
        stats["products"] = dict(product_stats)
        
        # 주문 통계
        order_stats = await conn.fetchrow("""
            SELECT 
                COUNT(*) as total_orders,
                COUNT(*) FILTER (WHERE status = 'delivered') as completed_orders,
                COALESCE(SUM(total_amount), 0) as total_revenue
            FROM orders
        """)
        stats["orders"] = dict(order_stats)
        
        # 카테고리 통계
        category_stats = await conn.fetchrow("""
            SELECT COUNT(*) as total_categories
            FROM product_categories WHERE is_active = true
        """)
        stats["categories"] = dict(category_stats)
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")
    finally:
        await conn.close()