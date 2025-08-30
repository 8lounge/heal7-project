// Service Worker for saju.heal7.com
// 사주 서비스용 간단한 PWA 지원

const CACHE_NAME = 'saju-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/crystal-ball.svg',
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

// 요청 인터셉트
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 캐시에 있으면 캐시된 응답 반환, 없으면 네트워크 요청
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});