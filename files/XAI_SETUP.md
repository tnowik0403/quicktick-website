# Quick Tick - xAI/Grok API Setup Instructions

## ✅ What's Already Done

All files have been updated to work with xAI's Grok API instead of Claude. The website name is now "Quick Tick" throughout all files.

## 🔑 What You Need to Do

### 1. Get Your xAI API Key

**Steps:**
1. Go to: **https://console.x.ai/**
2. Sign up for an xAI account (if you don't have one)
3. Navigate to the "API Keys" section
4. Click "Create New API Key"
5. **Copy the key immediately** - you won't be able to see it again!

### 2. Install Required Python Library

Open your terminal and run:

```bash
pip install openai
```

**Why OpenAI library?** xAI's Grok API uses the OpenAI-compatible format, so we use the `openai` library but point it to xAI's endpoint.

### 3. Set Your API Key as Environment Variable

**Mac/Linux:**
```bash
export XAI_API_KEY='your-actual-api-key-here'
```

**Windows (Command Prompt):**
```bash
set XAI_API_KEY=your-actual-api-key-here
```

**Windows (PowerShell):**
```bash
$env:XAI_API_KEY="your-actual-api-key-here"
```

### 4. Update Your AI Prompt (Important!)

Open `generate_company_data.py` in any text editor and find this section:

```python
YOUR_PROMPT = """
Analyze the company with ticker symbol {ticker}.

Provide the following information:
1. Company Overview (what they do, founded when, headquarters)
2. Business Model (how they make money)
3. Financial Highlights (recent revenue, profitability, market cap estimate)
4. Competitive Position (main competitors, market position)
5. Recent Developments (last 1-2 years)
6. Risks and Opportunities

Format the response in a clear, structured way with headers.
Keep it concise but informative (500-800 words).
"""
```

**Replace this entire section with YOUR prompt.** Make sure to keep `{ticker}` in your prompt - this gets replaced with each company's ticker symbol.

### 5. Choose Your Tickers (Optional)

By default, the script includes 50 major companies. You have two options:

**Option A - Use the full list (420 tickers):**

In `generate_company_data.py`, find the `TICKERS = [...]` section and replace it with:

```python
# Read tickers from file
with open('us_tickers.txt', 'r') as f:
    TICKERS = [line.strip() for line in f if line.strip()]
```

**Option B - Keep the default 50** for testing, then expand later.

### 6. Run the Script

```bash
python3 generate_company_data.py
```

The script will:
- Create a `data/` folder
- Generate a JSON file for each ticker
- Show progress in real-time
- Take 1-2 seconds per company

### 7. Test Your Website Locally

```bash
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

### 8. Buy Your Domain (quicktick.ai)

Once you're ready to go live:

1. **Purchase the domain** at your preferred registrar (Namecheap, GoDaddy, etc.)
2. **Deploy your site** to one of these free hosting services:
   - **Netlify** (recommended - easiest)
   - **Vercel**
   - **GitHub Pages**
3. **Point your domain** to your hosting (each service has documentation for this)

## 📊 xAI/Grok API Details

**Current Model:** `grok-beta`
- This is what the script uses by default
- Check https://docs.x.ai/ for other available models

**API Endpoint:** `https://api.x.ai/v1`
- Already configured in the script
- Uses OpenAI-compatible format

**Pricing (approximate):**
- Input: ~$5 per 1M tokens
- Output: ~$15 per 1M tokens
- Average cost: ~$0.01-0.02 per company

**Rate Limits:**
- Check your console at https://console.x.ai/
- The script includes 1-second delays between requests
- Adjust `REQUEST_DELAY` if needed

## 🔄 Monthly Updates

Set a calendar reminder to run this monthly:

```bash
# Make sure API key is set
export XAI_API_KEY='your-key-here'

# Run the script
python3 generate_company_data.py

# Upload the new data/ folder to your hosting
```

Or use the provided automation script:
```bash
chmod +x monthly_update.sh
./monthly_update.sh
```

## 🎨 Customizing the Prompt for Better Results

**Tips for writing a great prompt:**

1. **Be specific about structure:**
   ```
   Use markdown headers (##) for each section.
   ```

2. **Request exact word count:**
   ```
   Keep total response between 600-800 words.
   ```

3. **Ask for specific data points:**
   ```
   Include: market cap, revenue (most recent year), employee count
   ```

4. **Format requirements:**
   ```
   Use bullet points for lists of competitors or products.
   ```

5. **Tone specification:**
   ```
   Write in a professional but accessible tone for retail investors.
   ```

## ⚠️ Important Notes

1. **Keep `{ticker}` in your prompt** - This is automatically replaced with each company's ticker
2. **Test with a few companies first** - Don't run all 5,000 immediately
3. **Monitor your API usage** - Check your xAI console for costs
4. **Review the output** - Check a few generated files to ensure quality
5. **Backup your data** - Keep copies of your data/ folder

## 🔍 Verifying Everything Works

1. ✅ Can you import openai? → `python3 -c "import openai; print('OK')"`
2. ✅ Is your API key set? → `echo $XAI_API_KEY`
3. ✅ Does the script run? → `python3 generate_company_data.py`
4. ✅ Are JSON files created? → Check the `data/` folder
5. ✅ Does the website work? → Open `index.html` in browser

## 🆘 Troubleshooting

**Error: "openai library not installed"**
→ Run: `pip install openai` or `pip3 install openai`

**Error: "XAI_API_KEY not set"**
→ Export your API key (see step 3 above)

**Error: "Authentication failed"**
→ Your API key might be invalid. Generate a new one at console.x.ai

**Error: "Rate limit exceeded"**
→ Increase `REQUEST_DELAY` in the script (change from 1 to 2 seconds)

**Files aren't generating**
→ Check if the `data/` folder was created
→ Run with `python3 generate_company_data.py` to see errors

**Website shows "Company not found"**
→ Make sure the `data/` folder is in the same directory as `index.html`
→ Check that the ticker JSON file exists (e.g., `data/AAPL.json`)

## 📞 Need Help?

1. Check the full **SETUP_GUIDE.md** for detailed instructions
2. Review xAI documentation: **https://docs.x.ai/**
3. Test with just 5-10 companies first before scaling up

---

**You're all set!** Everything is configured for xAI's Grok API. Just follow the steps above and you'll have Quick Tick running in no time! 🚀
