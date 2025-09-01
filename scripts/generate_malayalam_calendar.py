from kollavarsham import Kollavarsham
from datetime import date, timedelta
import json
import pytz
import datetime

# -------------------------
# CONFIGURATION
# -------------------------
start_year = 2025
end_year = 2025           # inclusive
output_file = "malayalam_calendar.json"

# Initialize Kollavarsham for Kerala
kv = Kollavarsham(latitude=10.5, longitude=76.0, system="SuryaSiddhanta")

# -------------------------
# GENERATE MAPPING
# -------------------------
mapping = {}

current_date = date(start_year, 1, 1)
end_date = date(end_year, 12, 31)

while current_date <= end_date:
    # Kollavarsham expects a datetime with timezone
    dt = datetime.datetime(current_date.year, current_date.month, current_date.day, tzinfo=pytz.UTC)
    mal_date = kv.from_gregorian_date(date=dt)
    mal_str = f"{mal_date.ml_masa_name} {mal_date.date}, {mal_date.year}"
    mapping[current_date.strftime("%Y-%m-%d")] = mal_str
    current_date += timedelta(days=1)

# -------------------------
# WRITE JSON
# -------------------------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"Generated {output_file} with {len(mapping)} dates.")
