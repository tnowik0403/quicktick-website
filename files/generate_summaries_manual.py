"""
Quick Tick TLDR Summary Generator - MANUAL VERSION

This script generates executive summaries for company analysis reports.
You can specify any custom list of tickers to process.

Requirements:
- Python 3.7+
- anthropic library (install: pip install anthropic)
- ANTHROPIC_API_KEY environment variable set

Usage:
1. Set your API key: 
   Windows (PowerShell): $env:ANTHROPIC_API_KEY='your-key-here'
   Mac/Linux: export ANTHROPIC_API_KEY='your-key-here'

2. Edit the TICKERS list below with your desired tickers

3. Run: python generate_summaries_manual.py
"""

import os
import json
import time
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
# Just replace this list with any tickers you want to generate summaries for
TICKERS = [
    "HIVE"

]

SUMMARY_PROMPT = """You are analyzing a comprehensive stock analysis report. Your task is to create a concise TLDR executive summary.

Here is the report content to analyze:

{content}

Create a TLDR summary following this structure:

1. Start with 1-2 sentences describing what the company does
2. Then, given the information provided and your general understanding of financial markets and investing, determine and summarize the most critical information to know and understand about the company for an individual deciding if they should invest in this company. This could include at a high level their primary products/services, growth strategy, market share and main competitors, SIGNIFICANT recent developments (no news about earnings reports) and qualitative assessments of financial performance.
3. Conclude with one sentence on the AI buy rating and fair value with reasoning.

Keep the total summary between 100-150 words. Write in a professional, direct tone. Focus on investment-critical information only.

Do NOT include any preamble like "Here is the summary:" - just provide the summary text directly."""

DATA_DIR = "data"

# API settings
MAX_RETRIES = 3
RETRY_DELAY = 60
REQUEST_DELAY = 2  # Short delay between requests (Haiku is fast)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_company_data(ticker):
    """Load existing company data from JSON file"""
    filepath = Path(DATA_DIR) / f"{ticker}.json"
    
    if not filepath.exists():
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  Error loading {ticker}: {str(e)}")
        return None


def save_company_data(data, ticker):
    """Save updated company data back to JSON file"""
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


def generate_summary(client, content, ticker):
    """
    Generate TLDR summary using Claude Haiku 4
    
    Args:
        client: Anthropic client instance
        content: Full markdown content from the report
        ticker: Stock ticker symbol
        
    Returns:
        str: Generated summary or None if failed
    """
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Generating summary for {ticker}... ", end="", flush=True)
            
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": SUMMARY_PROMPT.format(content=content)
                    }
                ]
            )
            
            # Extract text content
            summary = ""
            for block in message.content:
                if hasattr(block, 'type') and block.type == "text":
                    summary += block.text
            
            summary = summary.strip()
            
            # Calculate cost
            usage = message.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            
            # Haiku 3.5 pricing: Input $1/M, Output $5/M
            cost = (
                (input_tokens / 1_000_000 * 1.00) +
                (output_tokens / 1_000_000 * 5.00)
            )
            
            print(f"✓ (${cost:.4f})")
            
            return summary
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ (Attempt {attempt + 1}/{MAX_RETRIES})")
            print(f"    Error: {error_msg}")
            
            if attempt < MAX_RETRIES - 1:
                print(f"    Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"    Failed after {MAX_RETRIES} attempts")
                return None


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


def main():
    """Main execution function"""
    print("=" * 60)
    print("QUICK TICK - TLDR SUMMARY GENERATOR (MANUAL)")
    print("=" * 60)
    print()
    
    api_key = check_api_key()
    
    print(f"✓ Processing {len(TICKERS)} custom tickers")
    print()
    
    client = Anthropic(api_key=api_key)
    
    print(f"Generating summaries for your custom ticker list...")
    print("=" * 60)
    
    successful = 0
    skipped = 0
    failed = 0
    total_cost = 0.0
    start_time = time.time()
    
    for i, ticker in enumerate(TICKERS, 1):
        print(f"\n[{i}/{len(TICKERS)}] Processing {ticker}:")
        
        # Load existing company data
        data = load_company_data(ticker)
        
        if data is None:
            print(f"  ⚠ No JSON file found for {ticker} - skipping")
            skipped += 1
            continue
        
        # Extract content
        content = data.get("content", "")
        if not content:
            print(f"  ⚠ No content found in JSON - skipping")
            skipped += 1
            continue
        
        # Generate summary (always regenerate, even if exists)
        summary = generate_summary(client, content, ticker)
        
        if summary:
            # Add/update summary in data
            data["tldr_summary"] = summary
            
            # Save updated data
            if save_company_data(data, ticker):
                print(f"  Saved updated JSON with summary")
                successful += 1
                
                # Rough cost tracking
                total_cost += 0.01  # Approximate Haiku cost
            else:
                failed += 1
        else:
            failed += 1
        
        # Short delay between requests
        if i < len(TICKERS):
            time.sleep(REQUEST_DELAY)
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("SUMMARY GENERATION COMPLETE")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    if successful > 0:
        print(f"Average time per summary: {elapsed_time/successful:.1f} seconds")
        print(f"Estimated total cost: ${total_cost:.2f}")
        print(f"Average cost per summary: ${total_cost/successful:.4f}")
    print()
    print(f"Updated files in: {Path(DATA_DIR).absolute()}")
    print()


if __name__ == "__main__":
    main()
