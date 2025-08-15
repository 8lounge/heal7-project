/** @type {import('next').NextConfig} */
const nextConfig = {
  // 실험적 기능
  experimental: {
    // App Router 완전 활용
    appDir: true,
    // 서버 컴포넌트 최적화
    serverComponentsExternalPackages: ['dayjs'],
    // 이미지 최적화
    optimizePackageImports: ['lucide-react', 'recharts'],
  },

  // 이미지 최적화 설정
  images: {
    domains: ['heal7.com', 'saju.heal7.com'],
    formats: ['image/webp', 'image/avif'],
  },

  // PWA 지원을 위한 설정
  reactStrictMode: true,
  swcMinify: true,

  // 빌드 최적화
  compiler: {
    // Emotion/styled-components 제거 (Tailwind 사용)
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // 성능 최적화
  compress: true,
  poweredByHeader: false,

  // 환경 변수 설정
  env: {
    CUSTOM_KEY: 'heal7-saju-frontend',
    VERSION: '2.0.0',
  },

  // 웹팩 설정 (사주 계산 최적화용)
  webpack: (config, { dev, isServer }) => {
    // Web Workers 지원
    config.module.rules.push({
      test: /\.worker\.(js|ts)$/,
      use: {
        loader: 'worker-loader',
        options: {
          name: 'static/[hash].worker.js',
          publicPath: '/_next/',
        },
      },
    });

    // 사주 계산 라이브러리 최적화
    if (!dev && !isServer) {
      config.optimization.splitChunks.cacheGroups = {
        ...config.optimization.splitChunks.cacheGroups,
        saju: {
          name: 'saju-engine',
          chunks: 'all',
          test: /[\\/]src[\\/]lib[\\/]saju[\\/]/,
          priority: 30,
          reuseExistingChunk: true,
        },
      };
    }

    return config;
  },

  // 헤더 설정 (보안 및 성능)
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate',
          },
        ],
      },
    ];
  },

  // 리다이렉트 설정
  async redirects() {
    return [
      {
        source: '/saju',
        destination: '/saju/calculate',
        permanent: false,
      },
    ];
  },
};

// Bundle Analyzer (개발용)
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer(nextConfig);