import json
import os
from datetime import datetime
from daily_buckets import get_bucket

def generate_todays_tickers():
    """
    Generate todays_tickers.json
    
    IMPORTANT: The Daily QuickTick Update workflow increments current_day.txt
    at the end of its run. So current_day.txt contains TOMORROW's bucket number.
    We subtract 1 to get TODAY's actual bucket.
    """
    try:
        with open('current_day.txt', 'r') as f:
            next_day = int(f.read().strip())
    except Exception as e:
        print('Error reading current_day.txt: ' + str(e))
        next_day = 2  # Default (will become day 1)
    
    # Calculate today's day (current_day.txt is already incremented for tomorrow)
    today_day = next_day - 1
    
    # Handle wrap-around (if next_day is 1, today was 91)
    if today_day == 0:
        today_day = 91
    
    print('Next scheduled day (from current_day.txt): ' + str(next_day))
    print('Today\'s actual day (what we\'re generating): ' + str(today_day))
    
    todays_tickers = get_bucket(today_day)
    now = datetime.now()
    
    output = {
        "generated_at": now.isoformat(),
        "date": now.strftime("%B %d, %Y"),
        "day": today_day,
        "total_days": 91,
        "tickers": todays_tickers,
        "count": len(todays_tickers)
    }
    
    with open('todays_tickers.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print('')
    print('SUCCESS: Generated todays_tickers.json')
    print('Day: ' + str(today_day) + '/91')
    print('Date: ' + output['date'])
    print('Tickers: ' + str(len(todays_tickers)))
    print('First 5: ' + ', '.join(todays_tickers[:5]))
    
    return output

if __name__ == "__main__":
    generate_todays_tickers()
