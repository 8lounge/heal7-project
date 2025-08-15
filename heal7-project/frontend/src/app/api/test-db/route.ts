import { NextRequest, NextResponse } from 'next/server'
import { initializeConnections, testDatabaseQueries } from '@/lib/database'

export async function GET(request: NextRequest) {
  try {
    // Initialize connections
    const initResult = await initializeConnections()
    if (!initResult.success) {
      return NextResponse.json({
        success: false,
        error: 'Failed to initialize connections',
        details: initResult.error
      }, { status: 500 })
    }

    // Test database queries
    const testResult = await testDatabaseQueries()
    
    return NextResponse.json({
      success: testResult.success,
      message: testResult.success ? 'Database connections working properly' : 'Database test failed',
      data: testResult.success ? {
        postgresql: testResult.postgresql,
        redis: testResult.redis
      } : null,
      error: testResult.success ? null : testResult.error,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json({
      success: false,
      error: 'Internal server error',
      details: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    }, { status: 500 })
  }
}