// Service Worker for saju.heal7.com
// 사주 서비스용 간단한 PWA 지원

const CACHE_NAME = 'saju-v5'; // 강화된 chrome-extension 필터링
const urlsToCache = [
  '/',
  '/index.html',
  '/crystal-ball.svg',
  '/manifest.json',
  // 최신 빌드 파일들로 업데이트 (실제 빌드 후 생성되는 파일명으로 교체 필요)
  '/assets/index-DmWc4CBu.js',
  '/assets/index-Za-sZ4XS.css',
  '/assets/react-vendor-C8w-UNLI.js',
  '/assets/ui-vendor-DFRbeLvN.js',
  '/assets/three-vendor-Bkv47SOs.js'
];

// 설치 이벤트
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// 활성화 이벤트
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 캐시 가능한 요청인지 확인하는 함수 추가
function isValidCacheRequest(request) {
  try {
    // 지원되지 않는 scheme 필터링
    const unsupportedSchemes = ['chrome-extension', 'moz-extension', 'ms-browser-extension', 'chrome', 'moz', 'ms-browser'];
    const url = new URL(request.url);

    // 프로토콜 체크
    const protocol = url.protocol.replace(':', '');
    if (unsupportedSchemes.includes(protocol)) {
      console.log(`[SW] Skipping unsupported scheme: ${protocol}`);
      return false;
    }

    // HTTP/HTTPS만 캐시 허용
    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
      console.log(`[SW] Skipping non-HTTP(S) protocol: ${url.protocol}`);
      return false;
    }

    // extension 관련 URL 패턴 체크
    if (url.href.includes('extension') || url.href.includes('chrome-extension')) {
      console.log(`[SW] Skipping extension URL: ${url.href}`);
      return false;
    }

    return true;
  } catch (error) {
    console.error('[SW] Error checking request validity:', error);
    return false;
  }
}

// 요청 인터셉트
self.addEventListener('fetch', event => {
  // 빠른 프로토콜 체크
  if (event.request.url.startsWith('chrome-extension:') ||
    event.request.url.startsWith('moz-extension:') ||
    event.request.url.startsWith('ms-browser-extension:')) {
    console.log(`[SW] Ignoring extension request: ${event.request.url}`);
    return; // 완전히 무시하고 처리하지 않음
  }

  // 캐시 가능한 요청인지 확인
  if (!isValidCacheRequest(event.request)) {
    return; // 캐시하지 않고 그냥 넘어감
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 캐시에 있으면 캐시된 응답 반환, 없으면 네트워크 요청
        if (response) {
          return response;
        }

        return fetch(event.request)
          .then(response => {
            // 응답이 유효한지 확인
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                // 다시 한 번 캐시 가능한 요청인지 확인
                if (isValidCacheRequest(event.request)) {
                  cache.put(event.request, responseToCache).catch(error => {
                    console.error('[SW] Cache put error:', error, 'URL:', event.request.url);
                  });
                }
              })
              .catch(error => {
                console.error('[SW] Cache open error:', error);
              });

            return response;
          });
      })
      .catch(error => {
        console.log('[SW] Fetch error:', error);
        return fetch(event.request);
      })
  );
});