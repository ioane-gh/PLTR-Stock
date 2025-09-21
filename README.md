# PLTR Stock API

A RESTful API service for accessing historical PLTR (Palantir Technologies Inc.) stock data. This project provides endpoints to retrieve stock market data including OHLCV (Open, High, Low, Close, Volume) information stored in a SQLite database.

## 📊 Overview

This API serves historical PLTR stock data from September 30, 2020 to September 9, 2025, providing comprehensive market data for analysis, visualization, and trading applications.

## 🚀 Features

- **RESTful API Design**: Clean, intuitive endpoints following REST conventions
- **Comprehensive Stock Data**: OHLCV data plus adjusted close prices
- **Date-based Queries**: Retrieve data for specific dates or all available data
- **JSON Responses**: Structured, easy-to-parse JSON responses
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Health Monitoring**: Built-in health check endpoint for monitoring
- **SQLite Database**: Lightweight, file-based database for easy deployment

## 📁 Project Structure

```
PLTR Stock/
├── routes.py                    # Flask API server with endpoints
├── data_ingestion.py           # Script to load CSV data into database
├── requirements.txt            # Python dependencies
├── pltr.db                     # SQLite database (created after data ingestion)
├── Datasets/
│   └── PLTR_2020-09-30_2025-09-09.csv  # Source stock data
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd PLTR-Stock
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Load Data into Database

Run the data ingestion script to load the CSV data into the SQLite database:

```bash
python data_ingestion.py
```

This will:
- Load the PLTR stock data from the CSV file
- Create a SQLite database (`pltr.db`)
- Create a `stocks` table with all the historical data

### 4. Start the API Server

```bash
python routes.py
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### 1. Get All Stock Data

**Endpoint:** `GET /api/stocks`

**Description:** Retrieves all available PLTR stock data in chronological order.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "date": "2020-09-30",
      "open": 10.0,
      "high": 11.41,
      "low": 9.11,
      "close": 9.5,
      "adj_close": 9.5,
      "volume": 338584400
    }
  ],
  "count": 1241,
  "message": "Successfully retrieved 1241 stock records"
}
```

**Example Usage:**
```bash
curl "http://localhost:5000/api/stocks"
```

### 2. Get Stock Data by Date

**Endpoint:** `GET /api/stocks/date/<date>`

**Description:** Retrieves stock data for a specific trading date.

**Parameters:**
- `date` (string): Trading date in YYYY-MM-DD format

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "date": "2021-06-15",
    "open": 25.5,
    "high": 26.2,
    "low": 25.1,
    "close": 25.8,
    "adj_close": 25.8,
    "volume": 45000000
  },
  "message": "Successfully retrieved stock data for 2021-06-15"
}
```

**Response (Not Found):**
```json
{
  "success": false,
  "error": "Not found",
  "message": "No stock data found for date 2025-01-01"
}
```

**Example Usage:**
```bash
curl "http://localhost:5000/api/stocks/date/2021-06-15"
```

### 3. Get Latest Stock Data

**Endpoint:** `GET /api/stocks/latest`

**Description:** Retrieves the most recent stock data (latest trading date) from the database.

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "date": "2025-09-09",
    "open": 25.5,
    "high": 26.2,
    "low": 25.1,
    "close": 25.8,
    "adj_close": 25.8,
    "volume": 45000000
  },
  "message": "Successfully retrieved latest stock data"
}
```

**Response (Not Found):**
```json
{
  "success": false,
  "error": "Not found",
  "message": "No stock data found"
}
```

**Example Usage:**
```bash
curl "http://localhost:5000/api/stocks/latest"
```

### 4. Health Check

**Endpoint:** `GET /api/health`

**Description:** Returns the current status of the API service.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Example Usage:**
```bash
curl "http://localhost:5000/api/health"
```

## 📊 Data Schema

### Stock Record Structure

Each stock record contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Trading date (YYYY-MM-DD format) |
| `open` | float | Opening price for the trading day |
| `high` | float | Highest price during the trading day |
| `low` | float | Lowest price during the trading day |
| `close` | float | Closing price for the trading day |
| `adj_close` | float | Adjusted closing price (accounts for splits/dividends) |
| `volume` | integer | Number of shares traded |

## 🔧 Configuration

### Server Configuration

The Flask server runs with the following default settings:

- **Host:** `0.0.0.0` (accessible from any IP)
- **Port:** `5000`
- **Debug Mode:** `True` (enables auto-reload and detailed error pages)

To modify these settings, edit the last line in `routes.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Database Configuration

The SQLite database file (`pltr.db`) is created in the project root directory. The database uses the following configuration:

- **Database Engine:** SQLite
- **Table Name:** `stocks`
- **Row Factory:** `sqlite3.Row` (enables column access by name)

## 🚨 Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

### HTTP Status Codes

- **200 OK:** Successful request
- **404 Not Found:** No data found for the specified date
- **500 Internal Server Error:** Database or server error

### Error Response Format

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

## 🧪 Testing

### Manual Testing with cURL

```bash
# Test health endpoint
curl "http://localhost:5000/api/health"

# Test all stocks endpoint
curl "http://localhost:5000/api/stocks"

# Test specific date endpoint
curl "http://localhost:5000/api/stocks/date/2021-06-15"

# Test latest stock data endpoint
curl "http://localhost:5000/api/stocks/latest"

# Test invalid date
curl "http://localhost:5000/api/stocks/date/2025-01-01"
```

### Testing with Python

```python
import requests

# Test health endpoint
response = requests.get("http://localhost:5000/api/health")
print(response.json())

# Test all stocks endpoint
response = requests.get("http://localhost:5000/api/stocks")
data = response.json()
print(f"Retrieved {data['count']} stock records")

# Test specific date
response = requests.get("http://localhost:5000/api/stocks/date/2021-06-15")
print(response.json())

# Test latest stock data
response = requests.get("http://localhost:5000/api/stocks/latest")
data = response.json()
if data['success']:
    print(f"Latest stock data: {data['data']['date']} - Close: ${data['data']['close']}")
else:
    print(f"Error: {data['message']}")
```

## 📈 Data Analysis Examples

### Using the API for Analysis

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Get all stock data
response = requests.get("http://localhost:5000/api/stocks")
data = response.json()

# Convert to DataFrame for analysis
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Calculate daily returns
df['daily_return'] = df['close'].pct_change()

# Find highest volume days
top_volume_days = df.nlargest(10, 'volume')[['date', 'volume', 'close']]
print("Top 10 highest volume days:")
print(top_volume_days)

# Calculate moving averages
df['ma_20'] = df['close'].rolling(window=20).mean()
df['ma_50'] = df['close'].rolling(window=50).mean()
```

## 🔒 Security Considerations

- **SQL Injection Protection:** All database queries use parameterized statements
- **Input Validation:** Date parameters are validated by the database
- **Error Information:** Error messages don't expose sensitive system information

## 🚀 Deployment

### Development Deployment

The current configuration is suitable for development. For production deployment, consider:

1. **Disable Debug Mode:**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. **Use a Production WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 routes:app
   ```

3. **Environment Variables:**
   ```python
   import os
   app.run(
       debug=os.getenv('DEBUG', 'False').lower() == 'true',
       host=os.getenv('HOST', '0.0.0.0'),
       port=int(os.getenv('PORT', 5000))
   )
   ```

## 📝 Dependencies

### Core Dependencies

- **Flask 2.3.3:** Web framework for building the API
- **pandas 2.1.4:** Data manipulation and analysis
- **numpy 1.26.2:** Numerical computing (required by pandas)
- **sqlalchemy 2.0.21:** Database connectivity and ORM

### Installation

```bash
pip install Flask==2.3.3 pandas==2.1.4 numpy==1.26.2 sqlalchemy==2.0.21
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🔄 Version History

- **v1.1.0** - Added latest stock data endpoint
  - GET /api/stocks/latest - Retrieve most recent stock data
  - Fixed SQL query typo in latest endpoint
  - Updated documentation and testing examples

- **v1.0.0** - Initial release with basic CRUD operations
  - GET /api/stocks - Retrieve all stock data
  - GET /api/stocks/date/<date> - Retrieve data by date
  - GET /api/health - Health check endpoint

## 📊 Data Source

The stock data is sourced from historical PLTR trading data covering the period from September 30, 2020 to September 9, 2025. The data includes:

- **Trading Days:** Approximately 1,241 trading days
- **Data Points:** OHLCV data for each trading day
- **Format:** CSV with standard financial data columns

---

**Note:** This API is for educational and development purposes. For production financial applications, ensure compliance with relevant financial data regulations and consider using official financial data providers.

