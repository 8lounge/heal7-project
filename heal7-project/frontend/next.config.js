/** @type {import('next').NextConfig} */
const nextConfig = {
  // For production server mode (dynamic + static fallback)
  // output: 'export', // Disabled for server mode
  trailingSlash: true,
  // Image optimization
  images: {
    unoptimized: true,
    domains: ['images.unsplash.com', 'cdn.midjourney.com']
  },
  // ESLint configuration
  eslint: {
    ignoreDuringBuilds: true,
  },
  // TypeScript configuration
  typescript: {
    ignoreBuildErrors: true,
  },
  // Headers for CSP and external resources
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' 'unsafe-eval'", 
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              "font-src 'self' https://fonts.gstatic.com data:",
              "img-src 'self' data: https: blob:",
              "media-src 'self' https: data: blob:",
              "connect-src 'self' ws: wss: https:",
              "object-src 'none'",
              "base-uri 'self'"
            ].join('; ')
          }
        ]
      }
    ]
  }
}

module.exports = nextConfig