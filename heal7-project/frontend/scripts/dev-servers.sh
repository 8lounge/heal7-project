#!/bin/bash

# 개발 서버 관리 스크립트

start_all() {
  echo "🚀 Starting all development servers..."
  echo "📡 Services will run on:"
  echo "- Saju App:        http://localhost:5173"
  echo "- Crawling App:    http://localhost:5174" 
  echo "- Admin App:       http://localhost:5175"
  echo "- Cube Module App: http://localhost:5176"
  echo ""
  
  pnpm dev
}

start_service() {
  case $1 in
    "saju")
      echo "🔮 Starting Saju App on http://localhost:5173..."
      pnpm dev:saju
      ;;
    "crawling")
      echo "🕷️ Starting Crawling App on http://localhost:5174..."
      pnpm dev:crawling
      ;;
    "admin")
      echo "🛠️ Starting Admin App on http://localhost:5175..."
      pnpm dev:admin
      ;;
    "cube")
      echo "🎼 Starting Cube Module App on http://localhost:5176..."
      pnpm dev:cube
      ;;
    *)
      echo "❌ Unknown service: $1"
      echo "Available: saju, crawling, admin, cube"
      exit 1
      ;;
  esac
}

usage() {
  echo "Usage: $0 [all|saju|crawling|admin|cube]"
  echo ""
  echo "Examples:"
  echo "  $0 all      # Start all services"
  echo "  $0 saju     # Start only saju app"
  echo "  $0 crawling # Start only crawling app"
  echo "  $0 admin    # Start only admin app"
  echo "  $0 cube     # Start only cube module app"
}

case ${1:-"help"} in
  "all")
    start_all
    ;;
  "saju"|"crawling"|"admin"|"cube")
    start_service $1
    ;;
  *)
    usage
    ;;
esac