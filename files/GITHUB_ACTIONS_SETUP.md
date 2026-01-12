# GitHub Actions Setup Guide for QuickTick AI

This guide will help you set up automatic daily updates for your QuickTick AI website using GitHub Actions.

## 📋 What You're Setting Up

- **Automatic daily runs** at 1 AM EST
- **Day tracking** (automatically cycles through days 1-91)
- **Auto-commit** of new JSON files to GitHub
- **Auto-deploy** to Cloudflare Pages (already configured)
- **Date tracking** in each report (generated date + next refresh date)

---

## 🚀 Setup Instructions

### Step 1: Add API Key to GitHub Secrets

1. Go to your GitHub repository: `https://github.com/tnowik0403/quicktick-website`

2. Click **Settings** (top menu)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret**

5. Add your secret:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Your Claude API key (starts with `sk-ant-...`)
   - Click **Add secret**

### Step 2: Upload Files to GitHub

Upload these 3 new files to your repository:

1. **generate_company_data.py** (enhanced version with day tracking)
   - Replaces your old version
   - Location: Root directory of your repo

2. **daily_buckets.py** (the 91-day schedule)
   - Location: Root directory of your repo

3. **daily-update.yml** (GitHub Actions workflow)
   - Location: `.github/workflows/daily-update.yml`
   - **IMPORTANT:** Create the `.github/workflows/` folder structure first!

### Step 3: Create the Workflows Folder

In your local repository:

```bash
cd "C:\Users\tnowi\Documents\Quick Tick\Github\quicktick-website"

# Create the folders
mkdir .github
mkdir .github\workflows

# Copy the workflow file
copy daily-update.yml .github\workflows\daily-update.yml
```

### Step 4: Initialize Day Tracker

Create a file called `current_day.txt` in your repo root with just the number `1`:

```bash
echo 1 > current_day.txt
```

This tells the script to start at Day 1.

### Step 5: Commit Everything to GitHub

Using GitHub Desktop:

1. You should see 4 new/modified files:
   - `generate_company_data.py` (modified)
   - `daily_buckets.py` (new)
   - `current_day.txt` (new)
   - `.github/workflows/daily-update.yml` (new)

2. Write commit message: "Add automated daily updates with GitHub Actions"

3. Click **Commit to main**

4. Click **Push origin**

---

## ✅ Verifying It Works

### Check GitHub Actions is Enabled

1. Go to your repo on GitHub
2. Click the **Actions** tab
3. You should see "Daily QuickTick Update" workflow

### Run a Manual Test

1. In the Actions tab, click **Daily QuickTick Update**
2. Click **Run workflow** button (right side)
3. Click the green **Run workflow** button
4. Watch it run! It should complete in 15-20 minutes

### What to Expect

The workflow will:
1. ✅ Check out your code
2. ✅ Install Python and dependencies
3. ✅ Run the script for today's tickers
4. ✅ Commit new JSON files back to GitHub
5. ✅ Cloudflare automatically deploys the changes

---

## 📅 How the Day Tracking Works

### First Run (Day 1)
- Script reads `current_day.txt` → finds `1`
- Processes 39 tickers from Day 1 bucket
- Updates `current_day.txt` to `2`
- Commits JSONs and the updated day file

### Second Run (Day 2)
- Script reads `current_day.txt` → finds `2`
- Processes 39 tickers from Day 2 bucket
- Updates `current_day.txt` to `3`
- And so on...

### After Day 91
- Script reads `current_day.txt` → finds `91`
- Processes 38 tickers from Day 91 bucket
- Updates `current_day.txt` back to `1` (cycles!)
- The quarterly cycle repeats automatically

---

## 🕐 Schedule Details

- **Scheduled time:** 1 AM EST daily
- **GitHub runs at:** 6 AM UTC (converts to 1 AM EST in winter)
- **Duration:** ~15-20 minutes for 38-39 tickers
- **Completion:** Usually by 1:20 AM EST

### Adjusting the Time

To change the run time, edit `.github/workflows/daily-update.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # 6 AM UTC = 1 AM EST
```

Cron format: `minute hour day month dayofweek`

Examples:
- `0 10 * * *` = 5 AM EST (10 AM UTC)
- `30 8 * * *` = 3:30 AM EST (8:30 AM UTC)
- Use this converter: https://crontab.guru/

---

## 📊 Monitoring

### View Run History

1. Go to **Actions** tab in GitHub
2. See all past runs and their status
3. Click any run to see detailed logs

### Check Costs

After each run, the script prints:
- Total API cost for the day
- Average cost per ticker
- Cache hit rate

Look in the workflow logs under the "Generate company data" step.

### What the Reports Show

Each JSON file now includes:

```json
{
  "ticker": "AAPL",
  "content": "**Report Generated:** January 12, 2026\n**Next Refresh:** April 13, 2026\n\n...",
  "generated_date": "2026-01-12T01:05:32.123456",
  "next_refresh_date": "2026-04-13T01:05:32.123456",
  "model": "claude-sonnet-4-20250514",
  "cost": 0.3842,
  "tokens": { ... }
}
```

---

## 🔧 Troubleshooting

### Workflow Doesn't Appear
- Make sure `.github/workflows/` folder structure is correct
- Workflow file must end in `.yml` or `.yaml`
- Push the files to GitHub

### "ANTHROPIC_API_KEY not found"
- Check GitHub Settings → Secrets → Actions
- Make sure it's named exactly: `ANTHROPIC_API_KEY`
- No spaces, all caps

### Git Push Fails
- GitHub Actions has permission to push by default
- If it fails, check repo Settings → Actions → General
- Enable "Read and write permissions"

### Wrong Time Zone
- GitHub Actions runs in UTC
- Convert your local time to UTC
- EST = UTC - 5 hours (winter)
- EDT = UTC - 4 hours (summer)

---

## 💰 Cost Estimates

With prompt caching enabled:

- **Per day:** ~$15.20 (38 tickers × $0.40)
- **Per month:** ~$456
- **Per quarter:** ~$1,394 (full 3,486 company refresh)

Without caching (first run only):
- **First day:** ~$26.60 (38 tickers × $0.70)

---

## 🎯 Next Steps

After setup is complete:

1. ✅ Let it run for a few days
2. ✅ Monitor the Actions tab for any failures
3. ✅ Check quicktick.ai to see updated reports
4. ✅ Verify dates are showing correctly in reports
5. ✅ After 91 days, confirm it cycles back to Day 1

---

## 📝 Manual Override

If you need to manually set the day:

```bash
# Set to day 50
echo 50 > current_day.txt

# Commit and push
git add current_day.txt
git commit -m "Set day to 50"
git push
```

The next automated run will continue from day 50.

---

## 🎉 You're All Set!

Your QuickTick AI will now automatically update ~38 companies every day at 1 AM EST, cycling through all 3,486 companies every quarter!
