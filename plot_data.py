import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import load_nfl_dates

# Create directory structure for charts
def create_chart_dirs(season):
    chart_dir = f"data/charts/{season}"
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)
    return chart_dir

def plot_tps(data_file, nfl_period, target_date):
    df = pd.read_csv(data_file, names=["minute", "tpm", "tps_med", "tps_max"])
    
    plt.figure(figsize=(10,6))
    
    # Plot the average TPS and max TPS
    plt.plot(df["minute"], df["tps_med"], label="TPS Average", color='blue')
    plt.plot(df["minute"], df["tps_max"], label="TPS Max", color='red')
    
    # Highlight top points
    top_avg = df["tps_med"].max()
    top_max = df["tps_max"].max()
    plt.annotate(f"Top AVG: {top_avg}", xy=(df["minute"][df["tps_med"].idxmax()], top_avg), xytext=(10,10),
                 textcoords="offset points", arrowprops=dict(arrowstyle="->", color='blue'))
    plt.annotate(f"Top MAX: {top_max}", xy=(df["minute"][df["tps_max"].idxmax()], top_max), xytext=(10,10),
                 textcoords="offset points", arrowprops=dict(arrowstyle="->", color='red'))
    
    # Set labels and title
    plt.xlabel("Time")
    plt.ylabel("TPS")
    plt.title(f'TPS Chart: {nfl_period["phase"]} ({nfl_period["season"]}) on {target_date}')
    plt.legend()
    
    # Save the chart in the correct folder
    chart_dir = create_chart_dirs(nfl_period["season"])
    output_file = f'{chart_dir}/{target_date}.png'
    plt.savefig(output_file)
    plt.close()

def main():
    # Calculate "yesterday"
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    nfl_dates = load_nfl_dates()
    
    for period in nfl_dates:
        start_date = datetime.strptime(period["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(period["end_date"], "%Y-%m-%d").date()
        
        if start_date <= yesterday <= end_date:
            data_file = f"data/tps/{period['season']}/transactions_{yesterday}.csv"
            
            if os.path.exists(data_file):
                plot_tps(data_file, period, yesterday)
                print(f"Chart generated for {period['phase']} - {yesterday}")

if __name__ == "__main__":
    main()
