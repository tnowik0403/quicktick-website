import json
import os
from datetime import datetime
from daily_buckets import get_bucket

def generate_todays_tickers():
    try:
        with open('current_day.txt', 'r') as f:
            current_day = int(f.read().strip())
    except Exception as e:
        print('Error reading current_day.txt: ' + str(e))
        current_day = 1
    
    todays_tickers = get_bucket(current_day)
    now = datetime.now()
    
    output = {
        "generated_at": now.isoformat(),
        "date": now.strftime("%B %d, %Y"),
        "day": current_day,
        "total_days": 91,
        "tickers": todays_tickers,
        "count": len(todays_tickers)
    }
    
    with open('todays_tickers.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print('SUCCESS: Generated todays_tickers.json')
    print('Day: ' + str(current_day) + '/91')
    print('Date: ' + output['date'])
    print('Tickers: ' + str(len(todays_tickers)))
    print('First 5: ' + ', '.join(todays_tickers[:5]))
    
    return output

if __name__ == "__main__":
    generate_todays_tickers()
