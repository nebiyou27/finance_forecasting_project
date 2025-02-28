import os
import yaml
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='logs/data_fetch.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    """Load configuration from config.yaml file"""
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise

def fetch_data(tickers, start_date, end_date):
    """Fetch financial data for multiple tickers and combine into one DataFrame"""
    try:
        all_data = {}
        
        for ticker in tickers:
            logging.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            data = yf.download(ticker, start=start_date, end=end_date)
            
            # Rename columns to include ticker name to avoid column name conflicts
            data.columns = [f"{ticker}_{col}" for col in data.columns]
            
            all_data[ticker] = data
        
        # Combine all DataFrames
        combined_data = pd.concat(all_data.values(), axis=1)
        
        return combined_data
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def save_to_csv(data, file_name="combined_financial_data.csv"):
    """Save fetched data to a single CSV file"""
    if data is not None and not data.empty:
        # Create the directory if it doesn't exist
        os.makedirs('data/raw', exist_ok=True)
        
        # Save to CSV
        file_path = f"data/raw/{file_name}"
        data.to_csv(file_path)
        logging.info(f"Combined data saved to {file_path}")
        return file_path
    else:
        logging.warning(f"No data to save")
        return None

def main():
    """Main function to fetch and save data for all tickers in one CSV"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logging.info("Starting data fetch process")
    
    try:
        # Load configuration
        config = load_config()
        start_date = config.get('start_date')
        end_date = config.get('end_date')
        tickers = config.get('tickers')
        
        if not all([start_date, end_date, tickers]):
            logging.error("Missing configuration parameters")
            return
        
        # Fetch data for all tickers
        combined_data = fetch_data(tickers, start_date, end_date)
        
        # Save combined data
        file_path = save_to_csv(combined_data)
        
        logging.info(f"Completed data fetch process. Saved to: {file_path}")
        
        # Print summary
        print("\nData Fetch Summary:")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Tickers Processed: {tickers}")
        print(f"File Saved: {file_path}")
        print(f"Combined DataFrame Shape: {combined_data.shape}")
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
