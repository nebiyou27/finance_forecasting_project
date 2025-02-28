import os

def create_folders():
    folders = [
        ".github/workflows",
        "data/raw",
        "data/processed",
        "notebooks",
        "scripts",
        "src",
        "tests",
        "logs"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")

def create_files():
    files = {
        ".gitignore": "data/raw/*.csv\nlogs/*.log\n__pycache__/\n",
        "README.md": "# Finance Forecasting Project\n\nProject for time series forecasting and portfolio optimization.",
        "requirements.txt": "yfinance\npandas\nnumpy\nmatplotlib\nseaborn\nstatsmodels\nscikit-learn",
        "config.yaml": "start_date: 2015-01-01\nend_date: 2025-01-31\ntickers: [TSLA, BND, SPY]",
        "scripts/data_fetch.py": """import yfinance as yf\n\ndef fetch_data(ticker, start, end):\n    data = yf.download(ticker, start=start, end=end)\n    return data\n""",
        ".github/workflows/ci.yml": """name: CI\n\non: [push]\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n    - name: Checkout code\n      uses: actions/checkout@v2\n    - name: Set up Python\n      uses: actions/setup-python@v2\n      with:\n        python-version: '3.9'\n    - name: Install dependencies\n      run: pip install -r requirements.txt"""
    }
    
    for file, content in files.items():
        with open(file, "w") as f:
            f.write(content)
        print(f"Created: {file}")

if __name__ == "__main__":
    create_folders()
    create_files()
    print("Project structure setup complete!")
