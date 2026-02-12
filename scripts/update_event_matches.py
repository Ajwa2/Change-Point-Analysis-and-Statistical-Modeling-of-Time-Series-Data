import pandas as pd
import json
from datetime import timedelta

# Paths (relative to repo root)
EV_PATH = 'data/processed/events.csv'
CP_PATH = 'data/processed/change_points.json'

# Load events
events = pd.read_csv(EV_PATH, parse_dates=['date'], dayfirst=False)

# Load change points JSON
with open(CP_PATH,'r',encoding='utf-8') as f:
    cp = json.load(f)

# Expect cp['tau_median'] to be an ISO date string; try parse
try:
    tau_date = pd.to_datetime(cp.get('tau_median'))
except Exception:
    print('Could not parse tau_median:', cp.get('tau_median'))
    tau_date = None

matched = []
WINDOW_DAYS = 90

if tau_date is not None:
    start = tau_date - timedelta(days=WINDOW_DAYS)
    end = tau_date + timedelta(days=WINDOW_DAYS)
    mask = (events['date'] >= start) & (events['date'] <= end)
    matches = events.loc[mask]
    for _, row in matches.iterrows():
        matched.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'event': row['event'],
            'category': row.get('category',''),
            'description': row.get('description',''),
            'source': row.get('source','')
        })

# Attach matched events to cp JSON and write back
cp['matched_events'] = matched
with open(CP_PATH,'w',encoding='utf-8') as f:
    json.dump(cp, f, indent=2, ensure_ascii=False)

print('Found', len(matched), 'matched events. Updated', CP_PATH)
for m in matched:
    print('-', m['date'], m['event'])
