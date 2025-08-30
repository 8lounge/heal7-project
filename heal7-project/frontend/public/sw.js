// Service Worker for saju.heal7.com
// 사주 서비스용 간단한 PWA 지원

const CACHE_NAME = 'saju-v4'; // 버전 업데이트 - 최신 빌드 파일명 반영
const urlsToCache = [
  '/',
  '/index.html',
  '/crystal-ball.svg',
  '/manifest.json',
  // 실제 빌드된 파일들
  '/assets/index-kj6737nK.js',
  '/assets/index-BnOUI4Gb.css',
  '/assets/react-vendor-C8w-UNLI.js',
  '/assets/ui-vendor-CoQqhW55.js',
  '/assets/three-vendor-CdMAxR4E.js',
  '/assets/OptimizedCyberCrystal-XDdRvjI0.js',
  '/assets/OptimizedStars-4nEhQaFf.js'
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
  // 지원되지 않는 scheme 필터링
  const unsupportedSchemes = ['chrome-extension', 'moz-extension', 'ms-browser-extension'];
  const url = new URL(request.url);

  if (unsupportedSchemes.includes(url.protocol.replace(':', ''))) {
    return false;
  }

  // HTTP/HTTPS만 캐시 허용
  return url.protocol === 'http:' || url.protocol === 'https:';
}

// 요청 인터셉트
self.addEventListener('fetch', event => {
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
                  cache.put(event.request, responseToCache);
                }
              })
              .catch(error => {
                console.log('Cache put error:', error);
              });

            return response;
          });
      })
      .catch(error => {
        console.log('Fetch error:', error);
        return fetch(event.request);
      })
  );
});