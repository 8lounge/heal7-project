"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

export interface TabItem {
  id: string
  label: string
  content: React.ReactNode
  disabled?: boolean
  icon?: React.ReactNode
}

export interface TabsProps {
  items: TabItem[]
  defaultActiveId?: string
  activeId?: string
  onTabChange?: (id: string) => void
  variant?: "default" | "pills" | "underline"
  size?: "sm" | "md" | "lg"
  className?: string
  orientation?: "horizontal" | "vertical"
}

const Tabs: React.FC<TabsProps> = ({
  items,
  defaultActiveId,
  activeId: controlledActiveId,
  onTabChange,
  variant = "default",
  size = "md",
  className,
  orientation = "horizontal"
}) => {
  const [internalActiveId, setInternalActiveId] = React.useState(
    controlledActiveId || defaultActiveId || items[0]?.id || ""
  )

  const activeId = controlledActiveId !== undefined ? controlledActiveId : internalActiveId
  const activeItem = items.find(item => item.id === activeId)

  const handleTabClick = (id: string, disabled?: boolean) => {
    if (disabled) return
    
    if (controlledActiveId === undefined) {
      setInternalActiveId(id)
    }
    onTabChange?.(id)
  }

  const sizeStyles = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg"
  }

  const variantStyles = {
    default: {
      list: "bg-muted p-1 rounded-lg",
      tab: "rounded-md transition-all duration-200 font-medium",
      active: "bg-background text-foreground shadow-sm",
      inactive: "text-muted-foreground hover:text-foreground hover:bg-background/50"
    },
    pills: {
      list: "gap-2",
      tab: "rounded-full transition-all duration-200 font-medium",
      active: "bg-primary text-primary-foreground",
      inactive: "text-muted-foreground hover:text-foreground hover:bg-muted"
    },
    underline: {
      list: "border-b border-border gap-6",
      tab: "relative pb-2 border-b-2 border-transparent transition-all duration-200 font-medium",
      active: "text-foreground border-primary",
      inactive: "text-muted-foreground hover:text-foreground hover:border-muted-foreground"
    }
  }

  const isVertical = orientation === "vertical"

  return (
    <div className={cn(
      "w-full",
      isVertical && "flex gap-4",
      className
    )}>
      {/* Tab List */}
      <div className={cn(
        "flex",
        isVertical ? "flex-col min-w-[200px]" : "flex-row",
        variantStyles[variant].list
      )}>
        {items.map((item) => {
          const isActive = item.id === activeId
          const isDisabled = item.disabled
          
          return (
            <button
              key={item.id}
              onClick={() => handleTabClick(item.id, item.disabled)}
              disabled={isDisabled}
              className={cn(
                "flex items-center justify-center gap-2 whitespace-nowrap transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                sizeStyles[size],
                variantStyles[variant].tab,
                isActive
                  ? variantStyles[variant].active
                  : variantStyles[variant].inactive,
                isDisabled && "opacity-50 cursor-not-allowed",
                isVertical && "w-full justify-start"
              )}
            >
              {item.icon && (
                <span className="text-current">{item.icon}</span>
              )}
              <span className="hangul-modern">{item.label}</span>
            </button>
          )
        })}
      </div>

      {/* Tab Content */}
      <div className={cn(
        "flex-1",
        isVertical ? "" : "mt-6"
      )}>
        {activeItem && (
          <div className="w-full">
            {activeItem.content}
          </div>
        )}
      </div>
    </div>
  )
}

export { Tabs }

// 사주 전용 탭 컴포넌트
export interface SajuTabsProps {
  children: React.ReactNode
  defaultTab?: string
  className?: string
}

export const SajuTabs: React.FC<SajuTabsProps> = ({
  children,
  defaultTab,
  className
}) => {
  const defaultItems: TabItem[] = [
    {
      id: "basic",
      label: "기본정보",
      content: children,
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      )
    },
    {
      id: "saju",
      label: "사주팔자",
      content: <div className="text-center p-8 text-muted-foreground">사주 계산 결과가 여기에 표시됩니다</div>,
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      )
    },
    {
      id: "analysis",
      label: "상세분석",
      content: <div className="text-center p-8 text-muted-foreground">상세 분석 결과가 여기에 표시됩니다</div>,
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      )
    }
  ]

  return (
    <Tabs
      items={defaultItems}
      defaultActiveId={defaultTab || "basic"}
      variant="underline"
      className={className}
    />
  )
}