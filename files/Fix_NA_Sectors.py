import json
import requests
import time

FINNHUB_API_KEY = 'd5n9k69r01ql6sfq9l20d5n9k69r01ql6sfq9l2g'

# Load the enhanced JSON file
with open('company_lookup_enhanced.json', 'r') as f:
    companies = json.load(f)

# Find tickers with N/A sectors
na_sectors = {ticker: data for ticker, data in companies.items() 
              if data.get('sector') == 'N/A' or data.get('subIndustry') == 'N/A'}

total_na = len(na_sectors)
fixed_count = 0
still_na_count = 0

print(f"Found {total_na} tickers with N/A sector/subIndustry")
print("="*60)

if total_na == 0:
    print("✅ No N/A sectors found! All tickers have sector data.")
else:
    print("Starting to fix N/A sectors...")
    print("="*60)
    
    for index, (ticker, data) in enumerate(na_sectors.items(), 1):
        print(f"[{index}/{total_na}] Fixing {ticker}...", end=" ")
        
        try:
            # Get Finnhub profile again
            response = requests.get(
                f'https://finnhub.io/api/v1/stock/profile2',
                params={'symbol': ticker, 'token': FINNHUB_API_KEY}
            )
            
            if response.status_code == 200:
                profile = response.json()
                
                if profile and 'finnhubIndustry' in profile:
                    finnhub_industry = profile.get('finnhubIndustry', '')
                    
                    if finnhub_industry:
                        # Update the sector and subIndustry with raw Finnhub data
                        if companies[ticker]['sector'] == 'N/A':
                            companies[ticker]['sector'] = finnhub_industry
                        
                        if companies[ticker]['subIndustry'] == 'N/A':
                            companies[ticker]['subIndustry'] = finnhub_industry
                        
                        print(f"✓ Updated to '{finnhub_industry}'")
                        fixed_count += 1
                    else:
                        print("✗ Finnhub has no industry data")
                        still_na_count += 1
                else:
                    print("✗ No profile data")
                    still_na_count += 1
            else:
                print(f"✗ API error {response.status_code}")
                still_na_count += 1
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"✗ Error: {str(e)[:30]}")
            still_na_count += 1
        
        # Progress indicator every 50 tickers
        if index % 50 == 0:
            elapsed = index
            remaining = total_na - index
            eta_min = remaining // 60
            print(f"\n--- {index}/{total_na} ({index*100//total_na}%) | ETA: ~{eta_min} min ---")

# Save the updated file
with open('company_lookup_final.json', 'w') as f:
    json.dump(companies, f, indent=2)

# Final summary
print("\n" + "="*60)
print("✅ CLEANUP COMPLETE!")
print("="*60)
print(f"Total N/A sectors found: {total_na}")
print(f"✓ Fixed with Finnhub data: {fixed_count}")
print(f"✗ Still N/A (no data): {still_na_count}")
print("="*60)
print("\nOutput: company_lookup_final.json")
print("\n📋 Next steps:")
print("1. Review company_lookup_final.json")
print("2. Backup: company_lookup.json -> company_lookup_backup.json")
print("3. Replace: company_lookup_final.json -> company_lookup.json")
print("4. Upload to your website!")
