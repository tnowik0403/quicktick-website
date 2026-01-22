import json
import requests
import time

FINNHUB_API_KEY = 'd5n9k69r01ql6sfq9l20d5n9k69r01ql6sfq9l2g'

# Map Finnhub industries to standard sectors
INDUSTRY_TO_SECTOR = {
    # Technology
    'Software': 'Technology',
    'Hardware': 'Technology',
    'Semiconductors': 'Technology',
    'Technology': 'Technology',
    'Electronic Equipment': 'Technology',
    'IT Services': 'Technology',
    'Computer': 'Technology',
    'Internet': 'Technology',
    'Telecom': 'Communication Services',
    'Telecommunications': 'Communication Services',
    
    # Healthcare
    'Biotechnology': 'Healthcare',
    'Pharmaceuticals': 'Healthcare',
    'Medical Devices': 'Healthcare',
    'Healthcare': 'Healthcare',
    'Health Care': 'Healthcare',
    'Life Sciences': 'Healthcare',
    
    # Financial
    'Banks': 'Financials',
    'Financial Services': 'Financials',
    'Insurance': 'Financials',
    'Investment Banking': 'Financials',
    'Asset Management': 'Financials',
    'Capital Markets': 'Financials',
    
    # Consumer
    'Retail': 'Consumer Discretionary',
    'Consumer Goods': 'Consumer Staples',
    'Food & Beverage': 'Consumer Staples',
    'Restaurants': 'Consumer Discretionary',
    'Apparel': 'Consumer Discretionary',
    'Automotive': 'Consumer Discretionary',
    'Hotels': 'Consumer Discretionary',
    'Media': 'Communication Services',
    'Entertainment': 'Communication Services',
    
    # Industrial
    'Industrial': 'Industrials',
    'Aerospace & Defense': 'Industrials',
    'Construction': 'Industrials',
    'Manufacturing': 'Industrials',
    'Transportation': 'Industrials',
    'Airlines': 'Industrials',
    
    # Energy
    'Energy': 'Energy',
    'Oil & Gas': 'Energy',
    'Utilities': 'Utilities',
    
    # Materials
    'Materials': 'Materials',
    'Chemicals': 'Materials',
    'Metals & Mining': 'Materials',
    
    # Real Estate
    'Real Estate': 'Real Estate',
    'REITs': 'Real Estate'
}

def map_industry_to_sector(industry):
    """Map Finnhub industry to standard sector"""
    if not industry:
        return None
    
    # Direct match
    if industry in INDUSTRY_TO_SECTOR:
        return INDUSTRY_TO_SECTOR[industry]
    
    # Partial match (check if any keyword is in the industry string)
    industry_lower = industry.lower()
    for key, sector in INDUSTRY_TO_SECTOR.items():
        if key.lower() in industry_lower:
            return sector
    
    return None

# Load existing company_lookup.json
with open('company_lookup.json', 'r') as f:
    companies = json.load(f)

# Enhance with exchange, country, AND sector/industry from Finnhub
enhanced = {}
success_count = 0
partial_count = 0
error_count = 0
sector_mapped = 0
total = len(companies)

print(f"Starting to process {total} tickers...")
print("="*60)

for index, (ticker, data) in enumerate(companies.items(), 1):
    print(f"[{index}/{total}] {ticker}...", end=" ")
    
    try:
        # Get Finnhub profile
        response = requests.get(
            f'https://finnhub.io/api/v1/stock/profile2',
            params={'symbol': ticker, 'token': FINNHUB_API_KEY}
        )
        
        if response.status_code == 200:
            profile = response.json()
            
            if profile and 'name' in profile:
                # Get Finnhub industry
                finnhub_industry = profile.get('finnhubIndustry', '')
                
                # Determine sector (use existing if available, otherwise map from Finnhub)
                sector = data.get('sector')
                if not sector or sector == 'N/A':
                    sector = map_industry_to_sector(finnhub_industry)
                    if sector:
                        sector_mapped += 1
                    else:
                        sector = 'N/A'
                
                # Determine subIndustry (use existing if available, otherwise use Finnhub)
                sub_industry = data.get('subIndustry')
                if not sub_industry or sub_industry == 'N/A':
                    sub_industry = finnhub_industry if finnhub_industry else 'N/A'
                
                enhanced[ticker] = {
                    'name': profile.get('name', data.get('name', ticker)),
                    'sector': sector,
                    'subIndustry': sub_industry,
                    'exchange': profile.get('exchange', 'N/A'),
                    'country': profile.get('country', 'USA')
                }
                
                # Check quality
                if (sector != 'N/A' and sub_industry != 'N/A' and 
                    profile.get('exchange') and profile.get('country')):
                    print("✓")
                    success_count += 1
                else:
                    print("⚠")
                    partial_count += 1
            else:
                # Finnhub returned empty
                enhanced[ticker] = {
                    'name': data.get('name', ticker),
                    'sector': data.get('sector', 'N/A'),
                    'subIndustry': data.get('subIndustry', 'N/A'),
                    'exchange': 'N/A',
                    'country': 'USA'
                }
                print("✗")
                error_count += 1
        else:
            # API error
            enhanced[ticker] = {
                'name': data.get('name', ticker),
                'sector': data.get('sector', 'N/A'),
                'subIndustry': data.get('subIndustry', 'N/A'),
                'exchange': 'N/A',
                'country': 'USA'
            }
            print(f"✗({response.status_code})")
            error_count += 1
        
        # Rate limiting
        time.sleep(1)
        
    except Exception as e:
        print(f"✗ {str(e)[:20]}")
        enhanced[ticker] = {
            'name': data.get('name', ticker),
            'sector': data.get('sector', 'N/A'),
            'subIndustry': data.get('subIndustry', 'N/A'),
            'exchange': 'N/A',
            'country': 'USA'
        }
        error_count += 1
    
    # Progress indicator
    if index % 100 == 0:
        elapsed = index  # seconds (since we sleep 1 sec per ticker)
        remaining = total - index
        eta_min = remaining // 60
        print(f"\n--- {index}/{total} ({index*100//total}%) | ETA: ~{eta_min} min ---")

# Save enhanced version
with open('company_lookup_enhanced.json', 'w') as f:
    json.dump(enhanced, f, indent=2)

# Final summary
print("\n" + "="*60)
print("✅ ENHANCEMENT COMPLETE!")
print("="*60)
print(f"Total tickers processed: {len(enhanced)}")
print(f"✓ Complete data: {success_count}")
print(f"⚠ Partial data: {partial_count}")
print(f"✗ Failed/No data: {error_count}")
print(f"🎯 Sectors mapped from industry: {sector_mapped}")
print("="*60)
print("\nOutput: company_lookup_enhanced.json")
print("\n📋 Next steps:")
print("1. Review the output file")
print("2. Backup: company_lookup.json -> company_lookup_backup.json")
print("3. Replace: company_lookup_enhanced.json -> company_lookup.json")
print("4. Upload to your website!")
