/**
 * 🔮 사주 관리자 탭별 목업 - 경량화 버전
 * 
 * 핵심 서비스 관리 기능:
 * - 1:1 문의, 회원관리, 사용자관리, 매거진관리
 * - 상품관리, 스토어관리, 사주관리설정
 * - 캐시/포인트 정책, 운영정책, 시스템설정
 * - 리뷰관리, 댓글관리
 * 
 * @author HEAL7 Admin Team
 * @version 2.0.0 - Service Management Complete (Modular)
 * @created 2025-09-04
 */

import React from 'react'
import {
  DashboardTab,
  SajuEngineTab,
  UserManagementTab,
  ContentManagementTab,
  AnalyticsTab,
  PointManagementTab,
  SystemManagementTab
} from './tabs'

// 🎯 경량화된 탭 컴포넌트 익스포트
export const DashboardTabMockup = DashboardTab
export const SajuEngineTabMockup = SajuEngineTab
export const UserManagementTabMockup = UserManagementTab
export const ContentManagementTabMockup = ContentManagementTab
export const AnalyticsTabMockup = AnalyticsTab
export const PointManagementTabMockup = PointManagementTab
export const SystemManagementTabMockup = SystemManagementTab