import refinitiv.data as rd
import pandas as pd
import os
from datetime import datetime, timedelta

def is_fund_data_current(file_path: str = "data/fund_analysis_results.csv", max_age_hours: int = 6) -> bool:
    """
    Check if fund data file exists and is recent enough.
    
    Args:
        file_path: Path to the fund analysis results CSV
        max_age_hours: Maximum age in hours before data is considered stale
    
    Returns:
        bool: True if data is current, False if needs refresh
    """
    try:
        if not os.path.exists(file_path):
            print("Fund data file doesn't exist - refresh needed")
            return False
        
        # Check file modification time
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        time_diff = datetime.now() - file_mod_time
        
        if time_diff.total_seconds() > (max_age_hours * 3600):
            print(f"Fund data is {time_diff.total_seconds()/3600:.1f} hours old - refresh needed")
            return False
        
        # Check if data contains today's or recent business day's data
        df = pd.read_csv(file_path)
        if df.empty:
            print("Fund data file is empty - refresh needed")
            return False
        
        # Get the most recent date in the data
        latest_data_date = pd.to_datetime(df['Date']).max()
        
        # Check if data is from today or last business day
        today = datetime.now().date()
        data_date = latest_data_date.date()
        
        # If it's weekend, accept Friday data; if Monday, accept Friday data
        weekday = today.weekday()
        if weekday == 0:  # Monday
            acceptable_date = today - timedelta(days=3)  # Friday
        elif weekday == 6:  # Sunday
            acceptable_date = today - timedelta(days=2)  # Friday
        elif weekday == 5:  # Saturday
            acceptable_date = today - timedelta(days=1)  # Friday
        else:  # Tue-Fri
            acceptable_date = today - timedelta(days=1)  # Previous day
        
        if data_date >= acceptable_date:
            print(f"Fund data is current (from {data_date}) - no refresh needed")
            return True
        else:
            print(f"Fund data is outdated (from {data_date}) - refresh needed")
            return False
            
    except Exception as e:
        print(f"Error checking fund data currency: {e} - refresh needed")
        return False

def refresh_fund_data(force: bool = False): 
    """
    Refresh fund data only if needed or forced.
    
    Args:
        force: If True, refresh regardless of current data age
    """
    # Check if refresh is needed
    if not force and is_fund_data_current():
        print("✓ Fund data is already current")
        return True
    
    print("Refreshing fund data...")
    
    try:
        rd.open_session()

        # Read the CSV file
        funds_df = pd.read_csv("data/listed_funds_tickers.csv")

        fields_nav   = "TR.NETASSETVAL"
        fields_price = "TR.CLOSEPRICE"

        # Get data from last 5 business days to ensure we get the most recent available
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        results = []

        for index, row in funds_df.iterrows():
            fund_name = row['Investment trust name']
            ticker = row['Ticker']
            
            try:
                # Get recent NAV and price data
                nav = rd.get_history(ticker, fields=fields_nav, interval="daily", 
                                start=start_date.strftime("%Y-%m-%d"), 
                                end=end_date.strftime("%Y-%m-%d"))
                px = rd.get_history(ticker, fields=fields_price, interval="daily", 
                                start=start_date.strftime("%Y-%m-%d"), 
                                end=end_date.strftime("%Y-%m-%d"))
                
                if px is not None and nav is not None and not px.empty and not nav.empty:
                    data = px.join(nav, how="inner")
                    
                    price_col = px.columns[0]
                    nav_col = nav.columns[0]
                    
                    # Get latest available values and their date
                    latest_price = data[price_col].iloc[-1]
                    latest_nav = data[nav_col].iloc[-1]
                    latest_date = data.index[-1]
                    discount_pct = (latest_price - latest_nav) / latest_nav * 100
                    
                    results.append({
                        'Fund Name': fund_name,
                        'Ticker': ticker,
                        'Date': latest_date.strftime("%Y-%m-%d"),
                        'Close Price': latest_price,
                        'NAV': latest_nav,
                        'Discount (%)': discount_pct
                    })
                    
            except Exception as e:
                print(f"✗ {fund_name}: Error - {str(e)}")

        # Create results DataFrame
        results_df = pd.DataFrame(results)

        # Ensure directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save to CSV
        results_df.to_csv("data/fund_analysis_results.csv", index=False)
        print(f"✓ Fund data refreshed successfully - {len(results)} funds updated")
        
        rd.close_session()
        return True
        
    except Exception as e:
        print(f"✗ Error refreshing fund data: {e}")
        try:
            rd.close_session()
        except:
            pass
        return False

if __name__ == "__main__":
    # Allow forcing refresh via command line argument
    import sys
    force_refresh = "--force" in sys.argv
    refresh_fund_data(force=force_refresh)