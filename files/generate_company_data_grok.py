"""
Quick Tick Data Generator - GROK VERSION

This script generates AI analysis for all publicly traded US companies.
It uses xAI's Grok API to generate company information based on your prompt.

Requirements:
- Python 3.7+
- openai library (install: pip install openai)
- XAI_API_KEY environment variable set

Usage:
1. Set your API key: export XAI_API_KEY='your-key-here'
2. Update YOUR_PROMPT_HERE with your actual prompt
3. Run: python generate_company_data_grok.py
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai library not installed")
    print("Install it with: pip install openai")
    exit(1)


# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

# Your AI prompt for analyzing companies
# Replace this with your actual prompt. Use {ticker} as a placeholder.
YOUR_PROMPT = """
You MUST use real-time web search to gather current information. Do not rely solely on training data. For the company (ticker: {ticker}), do a thorough review of all the latest discussions, articles, announcements, online talking points, earnings calls transcripts, etc. With this information, generate a company profile sell-side analysis report that includes a company overview (high-level summary of what the company does in 100-300 words), recent developments, growth strategy, company and sector headwinds and tailwinds, existing products/services, new products/services/projects that are being planned or developed, market share approximations by percent, forecast of growth or decline in market share, comparison to competitors, partnerships, M&A, current and potential major clients, and other qualitative measures associated with the company. Get as specific as possible. Include dates of specific events when possible and applicable. ONLY provide quantitative values for information from earnings reports and equivalents- such as revenues, earnings, gross margins, etc. – if they are from verified and recent (less than 6 months old) sources. Stock price and market capitalization information should be the verified values from sources that are up to date of the current day. Do NOT make up these values and dates. Given all the information you have gathered, latest stock price and company fundamentals, and general understanding of markets, give a "Buy Rating" on a scale of 1 to 10 based on if the stock should be "bought, held or sold", and an estimated fair value price for the stock for a portfolio looking for strong growth upside and a moderate risk appetite. Organize your output in an easily digestible format including using bullet points, tables, etc where appropriate to allow for fast reading without sacrificing context or level of detail.
"""

# Directory to save the generated data
DATA_DIR = "data"

# List of US stock tickers to process
# NOTE: For large lists, consider processing in batches to manage rate limits
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
    "V", "UNH", "JNJ", "WMT", "JPM", "MA", "PG", "XOM", "HD", "CVX",
    "MRK", "ABBV", "KO", "PEP", "COST", "AVGO", "TMO", "MCD", "CSCO",
    "ABT", "ACN", "DHR", "VZ", "ADBE", "NKE", "TXN", "CRM", "NFLX",
    "PM", "CMCSA", "NEE", "UPS", "BMY", "ORCL", "AMD", "QCOM", "HON",
    "RTX", "UNP", "INTC", "AMGN", "COP", "LOW", "BA", "SPGI", "IBM",
    # Add more tickers here...
]

# API settings
# NOTE: Grok has different rate limits than Claude
# Adjust these based on your actual rate limit experience
MAX_RETRIES = 5  # Increased retries
RETRY_DELAY = 120  # Wait 2 minutes on retry
REQUEST_DELAY = 10  # 10 seconds between requests


# ============================================================================
# MAIN CODE
# ============================================================================

def setup_data_directory():
    """Create the data directory if it doesn't exist"""
    Path(DATA_DIR).mkdir(exist_ok=True)
    print(f"✓ Data directory ready: {DATA_DIR}/")


def check_api_key():
    """Verify that the API key is set"""
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("ERROR: XAI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  Mac/Linux: export XAI_API_KEY='your-key-here'")
        print("  Windows (PowerShell): $env:XAI_API_KEY='your-key-here'")
        print("  Windows (CMD): set XAI_API_KEY=your-key-here")
        exit(1)
    print("✓ API key found")
    return api_key


def generate_company_data(client, ticker):
    """
    Generate company data for a single ticker using Grok API
    
    Args:
        client: OpenAI client instance configured for xAI
        ticker: Stock ticker symbol
        
    Returns:
        dict: Company data or None if failed
    """
    prompt = YOUR_PROMPT.format(ticker=ticker)
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Requesting data for {ticker}... ", end="", flush=True)
            
            response = client.chat.completions.create(
                model="grok-4-1-fast-reasoning",
                messages=[
                    {
                        "role": "system",
                        "content": "You have access to real-time information. Provide comprehensive, accurate analysis with verified financial data from reliable sources. Only report events and dates that have actually occurred."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=8000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Filter out any thinking process if present
            # Grok may include reasoning steps, we only want the final report
            if "I'll conduct" in content or "Let me search" in content:
                # Try to extract just the report section
                lines = content.split('\n')
                filtered_lines = []
                skip_thinking = True
                
                for line in lines:
                    # Look for report start indicators
                    if any(indicator in line.lower() for indicator in ['# ', '## ', 'company overview', 'executive summary', 'sell-side']):
                        skip_thinking = False
                    
                    if not skip_thinking:
                        filtered_lines.append(line)
                
                if filtered_lines:
                    content = '\n'.join(filtered_lines)
            
            # Add disclaimer at the top
            disclaimer = """**Disclaimer:** This sell-side report was generated using Grok 4.1 Fast Reasoning (grok-4-1-fast-reasoning). Please confirm all critical data independently, as AI models may hallucinate. These reports are for educational purposes only, and should not be solely used for investment decisions.

Grok's API is currently limited to information up to the **end of 2024**. Claude's Sonnet 4.5 has access to up-to-date information, but is considerably more expensive per output (nearly $1 per ticker). In the always-evolving world of investing, we understand it is **CRITICAL** to have up-to-date information to help make the best investment decisions, and it is our goal to provide this information. But considering there are thousands of companies that we would ideally be updating monthly, as well as future goals of also providing quick and digestible summaries and insights for newly released earnings and conference calls, breaking news, FED speeches, etc, this quickly becomes very costly.

For this reason, please consider **subscribing to our Patreon** or donating to enable QuickTick AI to provide as much value and up-to-date insight as possible to **allow you to make the most informed investment decisions with a level of efficiency not possible even a few years ago.** 100% of the funds will go straight to purchasing more API credits to continue expanding our high quality, up-to-date analysis for more and more companies, and further then into our future value-generating plans. Thanks! - QuickTick AI

---

"""
            content = disclaimer + content
            
            print("✓")
            
            return {
                "ticker": ticker,
                "content": content,
                "generated_date": datetime.now().isoformat(),
                "model": "grok-4-1-fast-reasoning"
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ (Attempt {attempt + 1}/{MAX_RETRIES})")
            print(f"    Error: {error_msg}")
            
            # Check if it's a rate limit error
            is_rate_limit = "rate_limit" in error_msg.lower() or "429" in error_msg
            
            if is_rate_limit:
                print(f"    Rate limit hit - waiting longer before retry")
            
            if attempt < MAX_RETRIES - 1:
                # Use exponential backoff for rate limits
                wait_time = RETRY_DELAY * (2 ** attempt) if is_rate_limit else RETRY_DELAY
                print(f"    Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"    Failed after {MAX_RETRIES} attempts")
                print(f"    Skipping {ticker} - you can re-run just this ticker later")
                return None


def save_company_data(data, ticker):
    """Save company data to a JSON file"""
    if data is None:
        return False
        
    filepath = Path(DATA_DIR) / f"{ticker}.json"
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  Error saving {ticker}: {str(e)}")
        return False


def main():
    """Main execution function"""
    print("=" * 60)
    print("QUICK TICK - DATA GENERATOR (GROK)")
    print("=" * 60)
    print()
    
    # Setup
    setup_data_directory()
    api_key = check_api_key()
    
    # Initialize OpenAI client with xAI endpoint
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )
    
    print(f"\nProcessing {len(TICKERS)} tickers...")
    print("=" * 60)
    
    # Statistics
    successful = 0
    failed = 0
    start_time = time.time()
    
    # Process each ticker
    for i, ticker in enumerate(TICKERS, 1):
        print(f"\n[{i}/{len(TICKERS)}] Processing {ticker}:")
        
        # Generate data
        data = generate_company_data(client, ticker)
        
        # Save data
        if save_company_data(data, ticker):
            print(f"  Saved to {DATA_DIR}/{ticker}.json")
            successful += 1
        else:
            failed += 1
        
        # Rate limiting - wait between requests
        if i < len(TICKERS):
            time.sleep(REQUEST_DELAY)
    
    # Final statistics
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    print(f"Average time per ticker: {elapsed_time/len(TICKERS):.1f} seconds")
    print()
    print(f"Data saved to: {Path(DATA_DIR).absolute()}")
    print()


if __name__ == "__main__":
    main()
