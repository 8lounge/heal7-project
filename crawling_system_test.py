#!/usr/bin/env python3
"""
🔍 크롤링 시스템 종합 검수 스크립트
- Selenium을 활용한 실제 브라우저 테스트
- 모든 페이지 및 기능 자동 검증
- 실질 서비스 관점 검수
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CrawlingSystemTester:
    def __init__(self, base_url="https://crawling.heal7.com"):
        self.base_url = base_url
        self.api_base = "http://localhost:8003"
        self.driver = None
        self.test_results = []
        
    def setup_driver(self):
        """Chrome WebDriver 초기화"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # 헤드리스 모드 (서버 환경용)
        chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def log_test(self, test_name, status, details=""):
        """테스트 결과 기록"""
        result = {
            "test": test_name,
            "status": "✅" if status else "❌", 
            "details": details,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        print(f"{result['status']} [{result['timestamp']}] {test_name}")
        if details:
            print(f"   └─ {details}")
            
    def test_api_endpoints(self):
        """백엔드 API 엔드포인트 테스트"""
        print("\n🔧 API 엔드포인트 테스트")
        
        endpoints = [
            "/health",
            "/api/services", 
            "/api/stats",
            "/api/jobs",
            "/api/ai-stats", 
            "/api/data",
            "/api/settings"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.api_base}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"API {endpoint}", True, f"응답 크기: {len(str(data))} bytes")
                else:
                    self.log_test(f"API {endpoint}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"API {endpoint}", False, f"연결 오류: {str(e)}")
                
    def test_main_page_load(self):
        """메인 페이지 로딩 테스트"""
        print("\n📄 메인 페이지 로딩 테스트")
        
        try:
            start_time = time.time()
            self.driver.get(self.base_url)
            
            # 페이지 제목 확인
            WebDriverWait(self.driver, 10).until(
                lambda d: d.title != ""
            )
            load_time = round(time.time() - start_time, 2)
            
            self.log_test("메인 페이지 로딩", True, f"로딩 시간: {load_time}초")
            
            # React 앱 로딩 대기
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "text-3xl"))
                )
                self.log_test("React 앱 초기화", True, "컴포넌트 렌더링 완료")
            except TimeoutException:
                self.log_test("React 앱 초기화", False, "컴포넌트 로딩 타임아웃")
                
        except Exception as e:
            self.log_test("메인 페이지 로딩", False, f"오류: {str(e)}")
            
    def test_navigation_menu(self):
        """네비게이션 메뉴 테스트"""
        print("\n🧭 네비게이션 메뉴 테스트")
        
        menu_items = [
            ("대시보드", "dashboard"),
            ("크롤링", "crawling"), 
            ("AI 분석", "ai-analysis"),
            ("데이터 관리", "data-management"),
            ("설정", "settings")
        ]
        
        for menu_name, menu_id in menu_items:
            try:
                # 메뉴 클릭 시도
                time.sleep(1)  # 페이지 안정화
                
                # 다양한 방법으로 메뉴 찾기 시도
                menu_element = None
                selectors = [
                    f"//button[contains(text(), '{menu_name}')]",
                    f"//a[contains(text(), '{menu_name}')]", 
                    f"//div[contains(text(), '{menu_name}')]",
                    f"//span[contains(text(), '{menu_name}')]"
                ]
                
                for selector in selectors:
                    try:
                        menu_element = self.driver.find_element(By.XPATH, selector)
                        break
                    except:
                        continue
                        
                if menu_element:
                    self.driver.execute_script("arguments[0].click();", menu_element)
                    time.sleep(2)  # 페이지 전환 대기
                    
                    # 페이지 전환 확인
                    page_content = self.driver.page_source
                    if menu_name in page_content or len(page_content) > 1000:
                        self.log_test(f"네비게이션 - {menu_name}", True, "페이지 전환 성공")
                    else:
                        self.log_test(f"네비게이션 - {menu_name}", False, "페이지 내용 로딩 실패")
                else:
                    self.log_test(f"네비게이션 - {menu_name}", False, "메뉴 요소를 찾을 수 없음")
                    
            except Exception as e:
                self.log_test(f"네비게이션 - {menu_name}", False, f"오류: {str(e)}")
                
    def test_dashboard_features(self):
        """대시보드 기능 테스트"""
        print("\n📊 대시보드 기능 테스트")
        
        # 대시보드로 이동
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # KPI 카드 확인
            kpi_cards = self.driver.find_elements(By.CLASS_NAME, "text-2xl")
            self.log_test("KPI 카드 렌더링", len(kpi_cards) > 0, f"{len(kpi_cards)}개 카드 발견")
            
            # 연결 상태 확인
            connection_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '연결')]")
            self.log_test("연결 상태 표시", len(connection_elements) > 0, "연결 상태 정보 표시됨")
            
            # 서비스 목록 확인
            service_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '서비스') or contains(text(), 'API') or contains(text(), '정부')]")
            self.log_test("서비스 목록 표시", len(service_elements) > 0, f"{len(service_elements)}개 서비스 관련 요소")
            
        except Exception as e:
            self.log_test("대시보드 기능", False, f"오류: {str(e)}")
            
    def test_settings_page(self):
        """설정 페이지 테스트"""
        print("\n⚙️ 설정 페이지 테스트")
        
        try:
            # 설정 페이지로 이동
            settings_menu = self.driver.find_element(By.XPATH, "//button[contains(text(), '설정')] | //span[contains(text(), '설정')]")
            self.driver.execute_script("arguments[0].click();", settings_menu)
            time.sleep(3)
            
            # 설정 탭 확인
            tabs = ["시스템", "크롤러", "API 키", "보안"]
            for tab_name in tabs:
                try:
                    tab_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{tab_name}')]")
                    self.log_test(f"설정 탭 - {tab_name}", True, "탭 요소 발견됨")
                except NoSuchElementException:
                    self.log_test(f"설정 탭 - {tab_name}", False, "탭 요소를 찾을 수 없음")
                    
            # 설정 입력 필드 확인
            input_fields = self.driver.find_elements(By.TAG_NAME, "input")
            self.log_test("설정 입력 필드", len(input_fields) > 0, f"{len(input_fields)}개 입력 필드")
            
            # 저장 버튼 확인
            save_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), '저장')]")
            self.log_test("설정 저장 버튼", len(save_buttons) > 0, "저장 버튼 발견됨")
            
        except Exception as e:
            self.log_test("설정 페이지", False, f"오류: {str(e)}")
            
    def test_performance_metrics(self):
        """성능 메트릭 테스트"""
        print("\n⚡ 성능 메트릭 테스트")
        
        try:
            # JavaScript 실행으로 성능 데이터 수집
            navigation_timing = self.driver.execute_script("""
                var timing = window.performance.timing;
                return {
                    pageLoadTime: timing.loadEventEnd - timing.navigationStart,
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    resourceCount: performance.getEntriesByType('resource').length
                };
            """)
            
            load_time = navigation_timing.get('pageLoadTime', 0) / 1000
            dom_time = navigation_timing.get('domContentLoaded', 0) / 1000
            resource_count = navigation_timing.get('resourceCount', 0)
            
            self.log_test("페이지 로딩 시간", load_time < 5.0, f"{load_time:.2f}초")
            self.log_test("DOM 준비 시간", dom_time < 3.0, f"{dom_time:.2f}초") 
            self.log_test("리소스 로딩", resource_count > 0, f"{resource_count}개 리소스")
            
            # 메모리 사용량 (가능한 경우)
            try:
                memory_info = self.driver.execute_script("return window.performance.memory;")
                if memory_info:
                    used_mb = memory_info['usedJSHeapSize'] / 1024 / 1024
                    self.log_test("메모리 사용량", used_mb < 100, f"{used_mb:.1f} MB")
            except:
                self.log_test("메모리 사용량", False, "메모리 정보 수집 불가")
                
        except Exception as e:
            self.log_test("성능 메트릭", False, f"오류: {str(e)}")
            
    def test_error_handling(self):
        """오류 처리 테스트"""
        print("\n🚨 오류 처리 테스트")
        
        try:
            # JavaScript 에러 확인
            js_errors = self.driver.execute_script("""
                var errors = [];
                if (window.jsErrors) {
                    errors = window.jsErrors;
                }
                return errors;
            """)
            
            self.log_test("JavaScript 에러", len(js_errors) == 0, f"{len(js_errors)}개 에러")
            
            # 콘솔 로그 확인 (Chrome 전용)
            try:
                logs = self.driver.get_log('browser')
                error_logs = [log for log in logs if log['level'] == 'SEVERE']
                self.log_test("브라우저 콘솔 에러", len(error_logs) == 0, f"{len(error_logs)}개 심각한 에러")
            except:
                self.log_test("브라우저 콘솔 에러", False, "콘솔 로그 수집 불가")
                
        except Exception as e:
            self.log_test("오류 처리", False, f"오류: {str(e)}")
            
    def run_full_test(self):
        """전체 테스트 실행"""
        print("🔍 크롤링 시스템 종합 검수 시작")
        print("=" * 50)
        
        try:
            # 1. API 테스트
            self.test_api_endpoints()
            
            # 2. 브라우저 테스트
            self.setup_driver()
            
            self.test_main_page_load()
            self.test_navigation_menu() 
            self.test_dashboard_features()
            self.test_settings_page()
            self.test_performance_metrics()
            self.test_error_handling()
            
        except Exception as e:
            print(f"❌ 테스트 실행 중 치명적 오류: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
                
        # 결과 요약
        self.print_summary()
        
    def print_summary(self):
        """테스트 결과 요약 출력"""
        print("\n" + "=" * 50)
        print("📋 테스트 결과 요약")
        print("=" * 50)
        
        passed = len([r for r in self.test_results if r['status'] == '✅'])
        failed = len([r for r in self.test_results if r['status'] == '❌'])
        total = len(self.test_results)
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"총 테스트: {total}개")
        print(f"성공: {passed}개")
        print(f"실패: {failed}개") 
        print(f"성공률: {success_rate:.1f}%")
        
        if failed > 0:
            print(f"\n❌ 실패한 테스트:")
            for result in self.test_results:
                if result['status'] == '❌':
                    print(f"   • {result['test']}: {result['details']}")
                    
        # 검수 결과 판정
        if success_rate >= 90:
            print(f"\n🎉 검수 결과: 우수 (서비스 운영 가능)")
        elif success_rate >= 75:
            print(f"\n⚠️ 검수 결과: 양호 (일부 개선 필요)")
        else:
            print(f"\n❌ 검수 결과: 부족 (서비스 개선 필요)")

if __name__ == "__main__":
    tester = CrawlingSystemTester()
    tester.run_full_test()