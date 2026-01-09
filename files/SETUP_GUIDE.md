# Quick Tick - Complete Setup Guide

This guide will walk you through setting up your company database website from scratch, even with zero coding experience.

## 📋 What You're Building

A searchable website at quicktick.ai where users can look up any US stock ticker (like NVDA, AAPL) and see AI-generated analysis about that company. The site automatically updates monthly with fresh data.

## 🗂️ Files Included

- **index.html** - The main search page (home page)
- **company.html** - The template for displaying company information
- **generate_company_data.py** - Python script to generate all company data
- **us_tickers.txt** - List of ~5,000 US stock tickers
- **data/** (folder) - Will contain JSON files with company information

## 🚀 Step-by-Step Setup

### Part 1: Install Python

**Mac/Linux:**
1. Open Terminal (search for "Terminal" in Spotlight/Applications)
2. Check if Python is installed: `python3 --version`
3. If not installed, download from: https://www.python.org/downloads/
4. Install and verify: `python3 --version`

**Windows:**
1. Download Python from: https://www.python.org/downloads/
2. Run installer - **CHECK "Add Python to PATH"**
3. Open Command Prompt and verify: `python --version`

### Part 2: Install Required Library

Open Terminal (Mac/Linux) or Command Prompt (Windows) and run:

```bash
pip install openai
```

Or if that doesn't work:
```bash
pip3 install openai --break-system-packages
```

### Part 3: Get Your xAI (Grok) API Key

1. Go to: https://console.x.ai/
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new API key
5. **COPY IT IMMEDIATELY** (you won't see it again)

### Part 4: Set Up Your API Key

**Mac/Linux:**
```bash
export XAI_API_KEY='your-api-key-here'
```

**Windows (Command Prompt):**
```bash
set XAI_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```bash
$env:XAI_API_KEY="your-api-key-here"
```

> **Note:** This sets the key temporarily. To make it permanent:
> - **Mac/Linux:** Add the export line to `~/.bash_profile` or `~/.zshrc`
> - **Windows:** Set it in System Environment Variables

### Part 5: Customize Your Prompt

1. Open `generate_company_data.py` in any text editor
2. Find the section marked `YOUR_PROMPT`
3. Replace it with your actual AI prompt
4. Make sure to keep `{ticker}` in your prompt - this gets replaced with each company's ticker symbol

Example prompt:
```python
YOUR_PROMPT = """
Analyze {ticker} and provide:
- Business overview
- Revenue model
- Key competitors
- Recent performance
- Investment outlook

Keep it under 600 words.
"""
```

### Part 6: Choose Your Tickers

The script includes ~50 major tickers by default. You have two options:

**Option A - Use the full list (recommended):**
1. Open `us_tickers.txt` 
2. Copy all the tickers
3. In `generate_company_data.py`, replace the `TICKERS` list with:

```python
# Read tickers from file
with open('us_tickers.txt', 'r') as f:
    TICKERS = [line.strip() for line in f if line.strip()]
```

**Option B - Start small:**
Keep the default 50 tickers for testing, then expand later.

### Part 7: Generate Your Data

1. Open Terminal/Command Prompt
2. Navigate to your project folder:
   ```bash
   cd path/to/your/folder
   ```
3. Run the script:
   ```bash
   python3 generate_company_data.py
   ```
   (Windows: use `python` instead of `python3`)

The script will:
- Create a `data/` folder
- Generate a JSON file for each ticker
- Show progress in real-time
- Take 1-2 seconds per company

**Time estimates:**
- 50 companies: ~2 minutes
- 500 companies: ~15 minutes  
- 5,000 companies: ~2-3 hours

### Part 8: Test Your Website Locally

**Option A - Simple Python Server (easiest):**
```bash
python3 -m http.server 8000
```
Then open: http://localhost:8000

**Option B - VS Code with Live Server:**
1. Install VS Code: https://code.visualstudio.com/
2. Install "Live Server" extension
3. Right-click `index.html` → "Open with Live Server"

**Option C - Just open the file:**
Double-click `index.html` (may have limited functionality)

### Part 9: Upload to the Internet

Once you've tested locally, here are the easiest hosting options:

**Option A - Netlify (Recommended - Free & Easy):**
1. Sign up at https://netlify.com
2. Drag and drop your folder (with index.html, company.html, and data folder)
3. Get your live URL instantly!
4. Every time you regenerate data, just drag the new folder again

**Option B - GitHub Pages (Free):**
1. Create GitHub account: https://github.com
2. Create new repository: `your-username.github.io`
3. Upload all files
4. Enable GitHub Pages in Settings
5. Your site will be at: `https://your-username.github.io`

**Option C - Vercel (Free):**
1. Sign up at https://vercel.com
2. Import your project
3. Deploy with one click

## 🔄 Monthly Updates

To update your data each month:

1. Make sure your API key is still set (see Part 4)
2. Run the generation script again:
   ```bash
   python3 generate_company_data.py
   ```
3. Re-upload to your hosting service (just drag the new `data/` folder)

**Pro tip:** Set a monthly calendar reminder!

## 💰 Cost Estimates

xAI Grok API pricing:
- Grok Beta: $5 per 1M input tokens, $15 per 1M output tokens
- Average company analysis: ~500 words output = ~700 tokens
- Cost per company: ~$0.01-0.02

**Total costs:**
- 50 companies: ~$0.50-1.00/month
- 500 companies: ~$5-10/month
- 5,000 companies: ~$50-100/month

Note: Grok pricing may vary. Check https://console.x.ai/ for current rates.

## 🛠️ Customization Ideas

**Change the Design:**
- Edit colors in the `:root` section of the `<style>` tags
- Modify fonts by changing the Google Fonts link
- Adjust spacing, sizes, and layout

**Add More Features:**
- Add company logos
- Include charts/graphs
- Add a "compare companies" feature
- Create industry categories

**Improve the AI Prompt:**
- Request specific metrics
- Ask for competitive analysis
- Include risk assessments
- Add industry trends

## ❓ Troubleshooting

**"Module not found: openai"**
→ Install the library: `pip install openai`

**"API key not found"**
→ Set your environment variable: `export XAI_API_KEY='your-key-here'`

**"Rate limit exceeded"**
→ Add more delay between requests in the script (increase `REQUEST_DELAY`)

**Website shows "Company not found"**
→ Make sure the `data/` folder is in the same directory as `index.html`

**Python command not found**
→ Try `python3` instead of `python`, or reinstall Python

**Characters display incorrectly**
→ Make sure files are saved with UTF-8 encoding

## 📚 Learn More

Want to understand the code better?

- **HTML/CSS basics:** https://www.w3schools.com/
- **JavaScript intro:** https://javascript.info/
- **Python tutorial:** https://docs.python.org/3/tutorial/
- **Grok API docs:** https://docs.x.ai/

## 🎉 You're Done!

You now have a fully functional, AI-powered company database website!

**Next steps:**
1. Test it thoroughly
2. Share with friends
3. Set up monthly updates
4. Customize the design to your liking

Questions? Issues? The hardest part is already done - you built a real website! 🚀
