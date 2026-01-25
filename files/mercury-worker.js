// ============================================================================
// Mercury AI Chatbot - Cloudflare Worker Proxy
// ============================================================================
// 
// This Worker securely proxies requests from your Mercury chatbot to the
// Anthropic API while keeping your API key hidden server-side.
//
// Features:
// - API key hidden on server (secure)
// - IP-based rate limiting (10 requests/minute per IP)
// - Domain validation (only your domain can use it)
// - Request logging for monitoring
// - CORS enabled for your domain
//
// Deploy to: Cloudflare Workers (workers.cloudflare.com)
// Cost: FREE (100,000 requests/day)
// ============================================================================

// ============================================================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================================================

const CONFIG = {
  // Your Anthropic API key (HIDDEN on server-side)
  ANTHROPIC_API_KEY: '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',
  
  // Your allowed domain(s) - requests from other domains will be rejected
  ALLOWED_ORIGINS: [
    'https://quicktick.ai',
    'https://www.quicktick.ai',
    'http://localhost:8000', // For local testing (remove in production)
  ],
  
  // Rate limiting
  RATE_LIMIT_REQUESTS: 10,    // Max requests per window
  RATE_LIMIT_WINDOW: 60000,   // Window in milliseconds (60 seconds)
  
  // Anthropic API endpoint
  ANTHROPIC_API_URL: 'https://api.anthropic.com/v1/messages',
  ANTHROPIC_VERSION: '2023-06-01',
};

// ============================================================================
// RATE LIMITING STORAGE (In-memory, resets on worker restart)
// ============================================================================

// Map to track requests per IP: { ip: [timestamp1, timestamp2, ...] }
const rateLimitStore = new Map();

function checkRateLimit(ip) {
  const now = Date.now();
  
  // Get existing requests for this IP
  let requests = rateLimitStore.get(ip) || [];
  
  // Remove requests older than the window
  requests = requests.filter(timestamp => now - timestamp < CONFIG.RATE_LIMIT_WINDOW);
  
  // Check if limit exceeded
  if (requests.length >= CONFIG.RATE_LIMIT_REQUESTS) {
    const oldestRequest = Math.min(...requests);
    const resetTime = new Date(oldestRequest + CONFIG.RATE_LIMIT_WINDOW);
    
    return {
      allowed: false,
      resetTime: resetTime.toISOString(),
      remaining: 0,
    };
  }
  
  // Add current request
  requests.push(now);
  rateLimitStore.set(ip, requests);
  
  return {
    allowed: true,
    remaining: CONFIG.RATE_LIMIT_REQUESTS - requests.length,
  };
}

// ============================================================================
// CORS HEADERS
// ============================================================================

function getCorsHeaders(origin) {
  // Check if origin is allowed
  const isAllowed = CONFIG.ALLOWED_ORIGINS.includes(origin);
  
  if (!isAllowed) {
    return null; // Will reject the request
  }
  
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400', // 24 hours
  };
}

// ============================================================================
// MAIN WORKER HANDLER
// ============================================================================

export default {
  async fetch(request, env, ctx) {
    const startTime = Date.now();
    const origin = request.headers.get('Origin');
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    
    // ========================================================================
    // 1. HANDLE CORS PREFLIGHT
    // ========================================================================
    
    if (request.method === 'OPTIONS') {
      const corsHeaders = getCorsHeaders(origin);
      
      if (!corsHeaders) {
        return new Response('Origin not allowed', { status: 403 });
      }
      
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }
    
    // ========================================================================
    // 2. VALIDATE REQUEST
    // ========================================================================
    
    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response(
        JSON.stringify({ error: 'Method not allowed. Use POST.' }),
        { 
          status: 405,
          headers: { 'Content-Type': 'application/json' },
        }
      );
    }
    
    // Validate origin
    const corsHeaders = getCorsHeaders(origin);
    if (!corsHeaders) {
      console.log(`❌ Rejected request from unauthorized origin: ${origin}`);
      return new Response(
        JSON.stringify({ error: 'Origin not allowed' }),
        { 
          status: 403,
          headers: { 'Content-Type': 'application/json' },
        }
      );
    }
    
    // ========================================================================
    // 3. CHECK RATE LIMIT
    // ========================================================================
    
    const rateLimitCheck = checkRateLimit(clientIP);
    
    if (!rateLimitCheck.allowed) {
      console.log(`⚠️  Rate limit exceeded for IP: ${clientIP}`);
      
      return new Response(
        JSON.stringify({
          error: 'Rate limit exceeded',
          message: `Too many requests. Please try again after ${rateLimitCheck.resetTime}`,
          resetTime: rateLimitCheck.resetTime,
        }),
        {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'X-RateLimit-Limit': CONFIG.RATE_LIMIT_REQUESTS.toString(),
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset': rateLimitCheck.resetTime,
            ...corsHeaders,
          },
        }
      );
    }
    
    // ========================================================================
    // 4. PARSE AND VALIDATE REQUEST BODY
    // ========================================================================
    
    let requestBody;
    
    try {
      requestBody = await request.json();
    } catch (error) {
      console.log(`❌ Invalid JSON in request body: ${error.message}`);
      
      return new Response(
        JSON.stringify({ error: 'Invalid JSON in request body' }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
          },
        }
      );
    }
    
    // Validate required fields
    if (!requestBody.model || !requestBody.messages) {
      console.log('❌ Missing required fields (model or messages)');
      
      return new Response(
        JSON.stringify({ 
          error: 'Missing required fields',
          required: ['model', 'messages'],
        }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
          },
        }
      );
    }
    
    // ========================================================================
    // 5. FORWARD REQUEST TO ANTHROPIC API
    // ========================================================================
    
    console.log(`✅ Forwarding request from IP: ${clientIP}, Model: ${requestBody.model}`);
    
    try {
      const anthropicResponse = await fetch(CONFIG.ANTHROPIC_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': CONFIG.ANTHROPIC_API_KEY,
          'anthropic-version': CONFIG.ANTHROPIC_VERSION,
        },
        body: JSON.stringify(requestBody),
      });
      
      // Get response body
      const responseBody = await anthropicResponse.text();
      
      // Log request details
      const processingTime = Date.now() - startTime;
      console.log(`📊 Request completed: ${anthropicResponse.status}, Time: ${processingTime}ms`);
      
      // Return response with CORS headers
      return new Response(responseBody, {
        status: anthropicResponse.status,
        headers: {
          'Content-Type': 'application/json',
          'X-Request-ID': anthropicResponse.headers.get('request-id') || 'unknown',
          'X-Processing-Time': `${processingTime}ms`,
          'X-RateLimit-Remaining': rateLimitCheck.remaining.toString(),
          ...corsHeaders,
        },
      });
      
    } catch (error) {
      console.error(`❌ Error forwarding to Anthropic: ${error.message}`);
      
      return new Response(
        JSON.stringify({
          error: 'Failed to reach Anthropic API',
          message: error.message,
        }),
        {
          status: 502,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders,
          },
        }
      );
    }
  },
};

// ============================================================================
// USAGE NOTES
// ============================================================================
//
// 1. Deploy this worker to Cloudflare Workers
// 2. Your worker URL will be: https://mercury-proxy.YOUR-SUBDOMAIN.workers.dev
// 3. Update your company.html to use this URL instead of Anthropic's API
// 4. Monitor usage at: https://dash.cloudflare.com
//
// Rate Limits:
// - 10 requests per minute per IP address
// - Resets automatically after 60 seconds
// - Applies to each user independently
//
// Security:
// - API key is NEVER sent to the browser
// - Only your domain can use this worker
// - All requests are logged for monitoring
// - Invalid requests are rejected immediately
//
// Performance:
// - Adds ~10ms average latency
// - Cloudflare's edge network = fast global routing
// - Free tier: 100,000 requests/day
// - Paid tier: 10M requests/month for $5
//
// ============================================================================
