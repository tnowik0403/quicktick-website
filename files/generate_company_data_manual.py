"""
Quick Tick Data Generator - MANUAL VERSION

This script generates AI analysis for a custom list of tickers you specify.
Perfect for running locally on your computer whenever you want specific updates.

Requirements:
- Python 3.7+
- anthropic library (install: pip install anthropic)
- ANTHROPIC_API_KEY environment variable set

Usage:
1. Set your API key: 
   Windows (PowerShell): $env:ANTHROPIC_API_KEY='your-key-here'
   Mac/Linux: export ANTHROPIC_API_KEY='your-key-here'

2. Edit the TICKERS list below with your desired tickers

3. Run: python generate_company_data_manual.py

Features:
- Custom ticker list (edit anytime!)
- Generated date and next refresh date in reports
- Prompt caching for cost savings
- Better thinking text filtering
- No day tracking - just processes your list
"""

import os
import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic library not installed")
    print("Install it with: pip install anthropic")
    exit(1)


# ============================================================================
# CONFIGURATION - EDIT YOUR TICKERS HERE!
# ============================================================================

# *** ADD YOUR TICKERS HERE ***
# Just replace this list with any tickers you want to analyze
TICKERS = [
    # Grid & Power
    "EOSE", "BE", "NVTS",
    # AI Utility
    "IREN", "CIFR", "NBIS", "APLD", "CRWV",
    # Space Economy
    "ASTS", "RKLB", "PL", "RDW", "FLY",
    # Nuclear
    "OKLO", "SMR", "NNE", "CCJ", "BWXT", "LEU",
    # Drones
    "KTOS", "ONDS", "AVAV", "DPRO", "PDYN", "RCAT",
    # Critical Materials
    "CRML", "UUUU", "UAMY", "ASPI", "USAR",
    # Chip Manufacturing & Memory
    "INTC", "MU", "AMKR", "SNDK", "LRCX", "SKYT",
]

YOUR_PROMPT = """
You MUST use real-time web search to gather current information. Do not rely solely on training data. For the company (ticker: {ticker}), do a thorough review of all the latest discussions, articles, announcements, online talking points, earnings calls transcripts, etc. With this information, generate a company profile sell-side analysis report that includes a company overview (high-level summary of what the company does in 100-300 words), recent developments, growth strategy, company and sector headwinds and tailwinds, existing products/services, new products/services/projects that are being planned or developed, market share approximations by percent, forecast of growth or decline in market share, comparison to competitors, partnerships, M&A, current and potential major clients, and other qualitative measures associated with the company. Get as specific as possible. Include dates of specific events when possible and applicable. ONLY provide quantitative values for information from earnings reports and equivalents- such as revenues, earnings, gross margins, etc. – if they are from verified and recent (less than 6 months old) sources. Stock price and market capitalization information should be the verified values from sources that are up to date of the current day. Do NOT make up these values and dates. Given all the information you have gathered, latest stock price and company fundamentals, and general understanding of markets, give a "Buy Rating" on a scale of 1 to 10 (up to one decimal place) based on if the stock should be "bought, held or sold", and an estimated fair value price for the stock for a portfolio looking for strong growth upside and a moderate risk appetite. Organize your output in an easily digestible format including using bullet points, tables, etc where appropriate to allow for fast reading without sacrificing context or level of detail.

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

Do NOT include any preamble, thinking process, or explanatory text before the title. Start directly with the # title.
"""

DATA_DIR = "data"

# API settings
MAX_RETRIES = 5
RETRY_DELAY = 120  # 2 minutes
REQUEST_DELAY = 20  # 20 seconds between requests


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_thinking_text(content):
    """
    Remove Claude's thinking/reasoning text and extract only the final report.
    This function is aggressive to ensure no thinking text leaks through.
    """
    
    # Common thinking patterns to remove (case-insensitive)
    thinking_patterns = [
        r"(?i)^.*?I'll conduct.*?(?=\n#|\n##|$)",
        r"(?i)^.*?Let me (search|conduct|analyze|gather).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Now (I'll|let me|I will).*?(?=\n#|\n##|$)",
        r"(?i)^.*?Based on (my|the) (research|search|analysis).*?(?=\n#|\n##|$)",
        r"(?i)^.*?I have (gathered|collected|found).*?(?=\n#|\n##|$)",
        r"(?i)^.*?After (searching|analyzing|reviewing).*?(?=\n#|\n##|$)",
        r"(?i)^.*?First,? (I'll|let me).*?(?=\n#|\n##|$)",
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
            "i'll", "let me", "now i", "first,", "based on",
            "after searching", "i have gathered", "i will"
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
    If it doesn't, add it. If it has the wrong format, fix it.
    """
    
    # Check if content starts with a title (# header)
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
                # Try to extract company name from something like "## Apple Inc. Overview"
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
        # Remove things like "Inc.", "Corp", "Comprehensive Analysis", etc.
        company_name = re.sub(r'\s*(Inc\.?|Corp\.?|Corporation|Company|Ltd\.?).*$', '', company_name, flags=re.IGNORECASE)
        company_name = re.sub(r'\s*\([A-Z]+\).*$', '', company_name)  # Remove ticker if present
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
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  Mac/Linux: export ANTHROPIC_API_KEY='your-key-here'")
        print("  Windows (PowerShell): $env:ANTHROPIC_API_KEY='your-key-here'")
        print("  Windows (CMD): set ANTHROPIC_API_KEY=your-key-here")
        exit(1)
    print("✓ API key found")
    return api_key


def generate_company_data(client, ticker):
    """
    Generate company data for a single ticker using Claude API with prompt caching
    
    This implementation uses prompt caching to reduce costs:
    - Static instructions are cached in the system message
    - Only the ticker symbol changes per request
    - Can reduce costs by 40-60% after the first request
    
    Args:
        client: Anthropic client instance
        ticker: Stock ticker symbol
        
    Returns:
        dict: Company data or None if failed
    """
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Requesting data for {ticker}... ", end="", flush=True)
            
            # Use prompt caching: put static instructions in system message with cache_control
            # The large prompt template is cached, only the ticker changes per request
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                system=[
                    {
                        "type": "text",
                        "text": YOUR_PROMPT.replace("{ticker}", "{{TICKER}}"),
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search"
                }],
                messages=[
                    {
                        "role": "user", 
                        "content": f"Generate the report for ticker: {ticker}"
                    }
                ]
            )
            
            # Extract text content only (no tool use blocks)
            content = ""
            for block in message.content:
                if hasattr(block, 'type') and block.type == "text":
                    content += block.text
            
            # Track usage and costs for monitoring
            usage = message.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            cache_creation_tokens = getattr(usage, 'cache_creation_input_tokens', 0)
            cache_read_tokens = getattr(usage, 'cache_read_input_tokens', 0)
            
            # Calculate cost (in dollars)
            # Input: $3/M, Output: $15/M, Cache write: $3.75/M, Cache read: $0.30/M
            cost = (
                (input_tokens / 1_000_000 * 3.00) +
                (output_tokens / 1_000_000 * 15.00) +
                (cache_creation_tokens / 1_000_000 * 3.75) +
                (cache_read_tokens / 1_000_000 * 0.30)
            )
            
            print(f"✓ (${cost:.4f}, cache: {'HIT' if cache_read_tokens > 0 else 'MISS'})")
            
            # Clean up any thinking text
            content = clean_thinking_text(content)
            
            # Enforce consistent title format
            content = enforce_title_format(content, ticker)
            
            # Calculate dates
            generated_date = datetime.now()
            next_refresh_date = generated_date + timedelta(days=91)
            
            # Format dates for display
            generated_str = generated_date.strftime("%B %d, %Y")
            next_refresh_str = next_refresh_date.strftime("%B %d, %Y")
            
            # Add disclaimer at the top with date information
            disclaimer = f"""**Report Generated:** {generated_str}  
**Next Refresh:** {next_refresh_str}

**Disclaimer:** This sell-side report was generated using Claude Sonnet 4 (claude-sonnet-4-20250514). Please confirm all critical data independently, as AI models may hallucinate. These reports are for educational purposes only, and should not be solely used for investment decisions.

---

"""
            content = disclaimer + content
            
            return {
                "ticker": ticker,
                "content": content,
                "generated_date": generated_date.isoformat(),
                "next_refresh_date": next_refresh_date.isoformat(),
                "model": "claude-sonnet-4-20250514",
                "cost": cost,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "cache_creation": cache_creation_tokens,
                    "cache_read": cache_read_tokens
                }
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ (Attempt {attempt + 1}/{MAX_RETRIES})")
            print(f"    Error: {error_msg}")
            
            is_rate_limit = "rate_limit" in error_msg.lower() or "429" in error_msg
            
            if "unable to access" in error_msg.lower() or "web search" in error_msg.lower():
                print(f"    Note: Web search temporarily unavailable for {ticker}")
                print(f"    This is usually temporary - will retry in {RETRY_DELAY} seconds")
            elif is_rate_limit:
                print(f"    Rate limit hit - waiting extra time before retry...")
            
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
    print("QUICK TICK - DATA GENERATOR (MANUAL VERSION)")
    print("=" * 60)
    print()
    
    setup_data_directory()
    api_key = check_api_key()
    
    print(f"✓ Processing {len(TICKERS)} custom tickers")
    print()
    
    client = Anthropic(api_key=api_key)
    
    print(f"Processing your custom ticker list...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    total_cost = 0.0
    start_time = time.time()
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"\n[{i}/{len(TICKERS)}] Processing {ticker}:")
        
        data = generate_company_data(client, ticker)
        
        if save_company_data(data, ticker):
            print(f"  Saved to {DATA_DIR}/{ticker}.json")
            successful += 1
            if data and 'cost' in data:
                total_cost += data['cost']
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
    if total_cost > 0:
        print(f"Total API cost: ${total_cost:.2f}")
        print(f"Average cost per ticker: ${total_cost/successful:.4f}")
    print()
    print(f"Data saved to: {Path(DATA_DIR).absolute()}")
    print()


if __name__ == "__main__":
    main()
