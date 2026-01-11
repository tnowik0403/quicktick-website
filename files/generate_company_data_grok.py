"""
Quick Tick Data Generator - GROK VERSION (IMPROVED)

This script generates AI analysis for all publicly traded US companies.
It uses xAI's Grok API to generate company information based on your prompt.

Requirements:
- Python 3.7+
- openai library (install: pip install openai)
- XAI_API_KEY environment variable set

Usage:
1. Set your API key: export XAI_API_KEY='your-key-here'
2. Run: python generate_company_data_grok.py

IMPROVEMENTS:
- Better filtering of Grok's reasoning process
- Consistent title format enforcement
- Cleaner output for website display
- Realistic prompt given Grok's end-of-2024 data limitation
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai library not installed")
    print("Install it with: pip install openai")
    exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

YOUR_PROMPT = """
For the company (ticker: {ticker}), generate a comprehensive sell-side analysis report. Use your knowledge base to provide detailed analysis including: company overview (high-level summary of what the company does in 100-300 words), recent developments, growth strategy, company and sector headwinds and tailwinds, existing products/services, new products/services/projects that are being planned or developed, market share approximations by percent, forecast of growth or decline in market share, comparison to competitors, partnerships, M&A, current and potential major clients, and other qualitative measures associated with the company. 

Get as specific as possible. Include dates of specific events when possible and applicable. ONLY provide quantitative values for information from earnings reports (revenues, earnings, gross margins, etc.) if they are from verified sources. For stock price and market capitalization, use the most recent data you have available. Do NOT make up values and dates.

Given all the information you have, provide a "Buy Rating" on a scale of 1 to 10 based on whether the stock should be "bought, held or sold", and an estimated fair value price for the stock for a portfolio looking for strong growth upside and a moderate risk appetite. Organize your output in an easily digestible format including using bullet points, tables, etc where appropriate to allow for fast reading without sacrificing context or level of detail.

CRITICAL: Start your report with EXACTLY this title format (replace with actual company name):
# [Company Name] ({ticker}) - Comprehensive Analysis Report

Then organize the report in the following sections:

## 1. Company Overview
## 2. Current Market Data
## 3. Existing Products/Services
## 4. Planned Products/Services/Projects
## 5. Growth Strategy
## 6. Current and Potential Major Clients
## 7. Financial Data & Performance
## 8. Market Shares
## 9. Comparison to Competitors
## 10. Partnerships, Mergers and Acquisitions
## 11. Recent Developments
## 12. AI Investment Rating & Fair Value Assessment

Do NOT include any preamble, reasoning steps, or explanatory text before the title. Start directly with the # title.
"""

DATA_DIR = "data"

# Tickers to process - customize this list
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
    "V", "UNH", "JNJ", "WMT", "JPM", "MA", "PG", "XOM", "HD", "CVX",
]

# API settings
MAX_RETRIES = 5
RETRY_DELAY = 120  # 2 minutes
REQUEST_DELAY = 10  # 10 seconds between requests


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_thinking_text(content):
    """
    Remove Grok's reasoning/thinking text and extract only the final report.
    """
    
    # Common thinking patterns to remove (case-insensitive)
    thinking_patterns = [
        r"(?i)^.*?I'll (conduct|search|analyze|gather|provide|create).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Let me (search|conduct|analyze|gather|compile|create).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Now (I'll|let me|I will).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Based on (my|the) (research|search|analysis|information).*?(?=\n#|\n##|$)",
        r"(?i)^.*?I (have|will) (gathered|compiled|analyzed).*?(?=\n#|\n##|$)",
        r"(?i)^.*?After (searching|analyzing|reviewing).*?(?=\n#|\n##|$)",
        r"(?i)^.*?First,? (I'll|let me|I will).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Here's (a|the) (comprehensive|detailed).*?(?=\n#|\n##|$)",
    ]
    
    # Apply all thinking patterns
    for pattern in thinking_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Remove any lines that look like thinking before the first header
    lines = content.split('\n')
    clean_lines = []
    found_header = False
    
    for line in lines:
        # Check if this is a markdown header (# or ##)
        if re.match(r'^#{1,6}\s+', line):
            found_header = True
            clean_lines.append(line)
        elif found_header:
            # After finding first header, include everything
            clean_lines.append(line)
        elif not line.strip():
            # Keep blank lines
            clean_lines.append(line)
        elif any(phrase in line.lower() for phrase in [
            "i'll", "let me", "now i", "first,", "based on", "here's",
            "after searching", "i have", "i will", "i've compiled"
        ]):
            # Skip lines that look like thinking
            continue
        else:
            # If we haven't found a header yet but line looks like content, keep it
            if len(line) > 50:  # Substantial content line
                clean_lines.append(line)
    
    return '\n'.join(clean_lines).strip()


def enforce_title_format(content, ticker):
    """
    Ensure the report starts with the correct title format.
    """
    
    lines = content.split('\n')
    
    # Look for the first # header
    first_header_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^#\s+', line):
            first_header_idx = i
            break
    
    # If no title found, add one at the beginning
    if first_header_idx == -1:
        # Try to extract company name from any h2 headers
        company_name = None
        for line in lines:
            if re.match(r'^##\s+', line):
                match = re.search(r'##\s+([^-\(]+)', line)
                if match:
                    company_name = match.group(1).strip()
                    break
        
        if not company_name:
            company_name = ticker  # Fallback
        
        title = f"# {company_name} ({ticker}) - Comprehensive Analysis Report\n\n"
        return title + content
    
    # Title exists, check if it's in the right format
    current_title = lines[first_header_idx]
    
    # Check if it already has the correct format
    if f"({ticker})" in current_title and "Comprehensive Analysis Report" in current_title:
        return content  # Already correct
    
    # Otherwise, try to extract company name and fix the title
    match = re.search(r'#\s+([^-\(]+)', current_title)
    if match:
        company_name = match.group(1).strip()
        company_name = re.sub(r'\s*(Inc\.?|Corp\.?|Corporation|Company|Ltd\.?).*$', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub(r'\s*\([A-Z]+\).*$', '', company_name)
    else:
        company_name = ticker  # Fallback
    
    # Create corrected title
    new_title = f"# {company_name} ({ticker}) - Comprehensive Analysis Report"
    lines[first_header_idx] = new_title
    
    return '\n'.join(lines)


# ============================================================================
# MAIN FUNCTIONS
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
                        "content": "You are a financial analyst creating sell-side research reports. Provide comprehensive, accurate analysis based on verified data. Only report events and dates that have actually occurred. Be concise and start directly with the report title."
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
            
            # Clean up any thinking/reasoning text
            content = clean_thinking_text(content)
            
            # Enforce consistent title format
            content = enforce_title_format(content, ticker)
            
            # Add disclaimer at the top
            disclaimer = """**Disclaimer:** This sell-side report was generated using Grok 4.1 Fast Reasoning (grok-4-1-fast-reasoning). Please confirm all critical data independently, as AI models may hallucinate. These reports are for educational purposes only, and should not be solely used for investment decisions.

**Data Limitation:** Grok's knowledge is limited to information available through the **end of 2024**. For the most current market data, earnings reports, and recent developments, please verify with up-to-date sources or consider our Claude Sonnet 4.5-powered reports which have real-time web search capabilities.

**Support QuickTick AI:** Claude Sonnet 4.5 provides superior, real-time analysis but costs significantly more per report (~$0.18 vs ~$0.01). To help us provide the most current analysis across all companies, plus future features like earnings summaries, breaking news digests, and Fed speech analysis, please consider supporting us on **[Patreon](https://patreon.com/QuickTickAI)**. 100% of funds go toward API costs to bring you the best investment intelligence tools.

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
            
            is_rate_limit = "rate_limit" in error_msg.lower() or "429" in error_msg
            
            if is_rate_limit:
                print(f"    Rate limit hit - waiting longer before retry")
            
            if attempt < MAX_RETRIES - 1:
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
    
    setup_data_directory()
    api_key = check_api_key()
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )
    
    print(f"\nProcessing {len(TICKERS)} tickers...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    start_time = time.time()
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"\n[{i}/{len(TICKERS)}] Processing {ticker}:")
        
        data = generate_company_data(client, ticker)
        
        if save_company_data(data, ticker):
            print(f"  Saved to {DATA_DIR}/{ticker}.json")
            successful += 1
        else:
            failed += 1
        
        if i < len(TICKERS):
            time.sleep(REQUEST_DELAY)
    
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
