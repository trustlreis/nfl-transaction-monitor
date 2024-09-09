import os
import datetime
import argparse
from db import get_db_connection
from config import load_nfl_dates

# Create directory structure for TPS data
def create_data_dirs(season):
    tps_dir = f"data/tps/{season}"
    if not os.path.exists(tps_dir):
        os.makedirs(tps_dir)
    return tps_dir

# Function to collect transaction data
def collect_transactions(start_date, end_date):
    # Use the shared get_db_connection function
    conn = get_db_connection()
    
    cursor = conn.cursor()
    
    query = """
    select date_trunc('minute', sec) as minuto, sum(cnt) as tpm, round(sum(cnt)::numeric/60,1) as tps_med, max(cnt) as tps_max
    from (
        select date_trunc('second', created_at) as sec, count(*) as cnt
        from pwmb.pwmb_transactions
        where created_at between %s and %s
        group by sec
    ) as m
    group by minuto
    order by 1;
    """
    
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return data

def main():
    # Setup argparse to optionally accept a date
    parser = argparse.ArgumentParser(description="Collect TPS data for a specific date or yesterday by default.")
    parser.add_argument('--date', type=str, help="Specific date to collect data (format: YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    # Calculate the date to collect data for
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        # Default to yesterday
        target_date = datetime.date.today() - datetime.timedelta(days=1)
    
    # Define start and end time for the target date (from 00:00:00 to 23:59:59)
    start_datetime = datetime.datetime.combine(target_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(target_date, datetime.time.max)
    
    nfl_dates = load_nfl_dates()
    
    for period in nfl_dates:
        start_date = datetime.datetime.strptime(period["start_date"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(period["end_date"], "%Y-%m-%d").date()
        
        # Check if the target date falls within the NFL period
        if start_date <= target_date <= end_date:
            # Collect data for the target date (from 00:00:00 to 23:59:59)
            data = collect_transactions(start_datetime, end_datetime)
            
            # Create directory structure for the season
            tps_dir = create_data_dirs(period["season"])
            file_name = f"{tps_dir}/transactions_{target_date}.csv"
            
            # Save the collected data to CSV
            with open(file_name, "w") as f:
                for row in data:
                    f.write(",".join([str(x) for x in row]) + "\n")
                    
            print(f"Data collected for {target_date} (from {start_datetime} to {end_datetime}) and saved to {file_name}")

if __name__ == "__main__":
    main()
