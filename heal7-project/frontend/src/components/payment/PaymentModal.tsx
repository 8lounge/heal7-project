import React, { useState, useEffect } from 'react';
import { loadTossPayments } from '@tosspayments/payment-sdk';
import { useAuth } from '@/contexts/AuthContext';

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  orderType: 'store' | 'academy';
  itemId: number;
  itemName: string;
  amount: number;
  quantity?: number;
}

interface CustomerInfo {
  name: string;
  email: string;
  phone: string;
}

const PaymentModal: React.FC<PaymentModalProps> = ({
  isOpen,
  onClose,
  orderType,
  itemId,
  itemName,
  amount,
  quantity = 1
}) => {
  const { user } = useAuth();
  const [customerInfo, setCustomerInfo] = useState<CustomerInfo>({
    name: '',
    email: '',
    phone: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [tossPayments, setTossPayments] = useState<any>(null);

  // 로그인된 사용자 정보 자동 설정
  useEffect(() => {
    if (user && isOpen) {
      setCustomerInfo({
        name: user.full_name || '',
        email: user.email || '',
        phone: user.phone || ''
      });
    }
  }, [user, isOpen]);

  useEffect(() => {
    if (isOpen) {
      const initTossPayments = async () => {
        try {
          const tossPaymentsInstance = await loadTossPayments('test_ck_D5GePWvyJnrK0W0k6q8gLzN97Eoq');
          setTossPayments(tossPaymentsInstance);
        } catch (error) {
          console.error('토스페이먼츠 초기화 실패:', error);
        }
      };
      initTossPayments();
    }
  }, [isOpen]);

  const handlePayment = async () => {
    if (!customerInfo.name || !customerInfo.email || !customerInfo.phone) {
      alert('모든 정보를 입력해주세요.');
      return;
    }

    if (!tossPayments) {
      alert('결제 시스템을 불러오는 중입니다. 잠시 후 다시 시도해주세요.');
      return;
    }

    setIsLoading(true);

    try {
      // 1. 주문 준비 API 호출
      const prepareResponse = await fetch(`/api/payment/prepare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          order_type: orderType,
          item_id: itemId,
          item_name: itemName,
          amount: amount,
          quantity: quantity,
          customer_name: customerInfo.name,
          customer_email: customerInfo.email,
          customer_phone: customerInfo.phone
        }),
      });

      const prepareData = await prepareResponse.json();

      if (!prepareData.success) {
        throw new Error(prepareData.message || '주문 준비 중 오류가 발생했습니다.');
      }

      // 2. 토스페이먼츠 결제 요청
      await tossPayments.requestPayment('카드', {
        amount: amount,
        orderId: prepareData.order_id,
        orderName: itemName,
        customerName: customerInfo.name,
        customerEmail: customerInfo.email,
        successUrl: `${window.location.origin}/payment/success`,
        failUrl: `${window.location.origin}/payment/fail`,
      });

    } catch (error: any) {
      console.error('결제 실행 중 오류:', error);
      alert(error.message || '결제 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900">결제하기</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            disabled={isLoading}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* 주문 정보 */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-900 mb-2">주문 상품</h3>
          <p className="text-gray-700">{itemName}</p>
          {quantity > 1 && <p className="text-sm text-gray-600">수량: {quantity}개</p>}
          <p className="text-lg font-bold text-blue-600 mt-2">
            {amount.toLocaleString()}원
          </p>
        </div>

        {/* 고객 정보 입력 */}
        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              이름 *
            </label>
            <input
              type="text"
              value={customerInfo.name}
              onChange={(e) => setCustomerInfo({...customerInfo, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="실명을 입력해주세요"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              이메일 *
            </label>
            <input
              type="email"
              value={customerInfo.email}
              onChange={(e) => setCustomerInfo({...customerInfo, email: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="example@email.com"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              휴대폰 번호 *
            </label>
            <input
              type="tel"
              value={customerInfo.phone}
              onChange={(e) => setCustomerInfo({...customerInfo, phone: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="010-0000-0000"
              disabled={isLoading}
            />
          </div>
        </div>

        {/* 결제 버튼 */}
        <div className="flex space-x-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50"
            disabled={isLoading}
          >
            취소
          </button>
          <button
            onClick={handlePayment}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? '처리 중...' : `${amount.toLocaleString()}원 결제하기`}
          </button>
        </div>

        {/* 결제 안내 */}
        <div className="mt-4 text-xs text-gray-500 text-center">
          <p>• 테스트 환경에서는 실제 결제가 발생하지 않습니다</p>
          <p>• 개인정보는 결제 처리 목적으로만 사용됩니다</p>
        </div>
      </div>
    </div>
  );
};

export default PaymentModal;