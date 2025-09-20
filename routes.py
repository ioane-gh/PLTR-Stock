"""
PLTR Stock API - Flask Web Service
==================================

This module provides REST API endpoints for accessing PLTR (Palantir) stock data.
The API serves historical stock data stored in a SQLite database.

Author: [Your Name]
Date: [Current Date]
Version: 1.0.0

Endpoints:
- GET /api/stocks - Retrieve all stock data
- GET /api/stocks/date/<date> - Retrieve stock data for specific date
- GET /api/health - Health check endpoint

Dependencies:
- Flask: Web framework
- sqlite3: Database connectivity
- datetime: Timestamp generation
"""

from flask import Flask, jsonify
import sqlite3
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

def get_db_connection():
    """
    Create and return a database connection to the PLTR stock database.
    
    Returns:
        sqlite3.Connection: Database connection object with row factory enabled
        
    Note:
        The row_factory is set to sqlite3.Row to enable column access by name
        instead of index, making the code more readable and maintainable.
    """
    conn = sqlite3.connect('pltr.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name (e.g., row['date'])
    return conn

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """
    GET endpoint to retrieve all stock data from the stocks table.
    
    This endpoint returns all available PLTR stock records in chronological order.
    Each record contains OHLCV (Open, High, Low, Close, Volume) data plus adjusted close.
    
    Returns:
        JSON response containing:
        - success: Boolean indicating if request was successful
        - data: List of stock records with OHLCV data
        - count: Number of records returned
        - message: Human-readable status message
        
    HTTP Status Codes:
        - 200: Success
        - 500: Server error (database or internal error)
        
    Example Response:
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
    """
    try:
        # Establish database connection
        conn = get_db_connection()
        
        # Execute query to retrieve all stock data ordered by date
        # ORDER BY ensures chronological sequence for better data analysis
        query = "SELECT * FROM stocks ORDER BY date"
        stocks_data = conn.execute(query).fetchall()
        
        # Convert SQLite Row objects to Python dictionaries for JSON serialization
        # This step is necessary because SQLite Row objects are not JSON serializable
        stocks_list = []
        for row in stocks_data:
            stock_record = {
                'date': row['date'],                    # Trading date (YYYY-MM-DD)
                'open': float(row['open']),             # Opening price
                'high': float(row['high']),             # Highest price of the day
                'low': float(row['low']),               # Lowest price of the day
                'close': float(row['close']),           # Closing price
                'adj_close': float(row['adj_close']),   # Adjusted closing price (for splits/dividends)
                'volume': int(row['volume'])            # Number of shares traded
            }
            stocks_list.append(stock_record)
        
        # Close database connection to free resources
        conn.close()
        
        # Return successful response with all stock data
        return jsonify({
            'success': True,
            'data': stocks_list,
            'count': len(stocks_list),
            'message': f'Successfully retrieved {len(stocks_list)} stock records'
        }), 200
        
    except sqlite3.Error as e:
        # Handle database-specific errors (connection issues, query problems, etc.)
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': str(e)
        }), 500
        
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring API status.
    
    This endpoint is commonly used by monitoring systems, load balancers,
    and deployment tools to verify that the API is running and responsive.
    
    Returns:
        JSON response with API status and current timestamp
        
    HTTP Status Codes:
        - 200: API is healthy and running
        
    Example Response:
        {
            "status": "healthy",
            "timestamp": "2024-01-15T10:30:45.123456"
        }
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/stocks/date/<date>', methods=['GET'])
def get_stocks_by_date(date):
    """
    GET endpoint to retrieve stock data for a specific date.
    
    This endpoint allows querying PLTR stock data for a single trading day.
    The date parameter should be in YYYY-MM-DD format.
    
    Args:
        date (str): Trading date in YYYY-MM-DD format (e.g., "2021-06-15")
        
    Returns:
        JSON response containing:
        - success: Boolean indicating if request was successful
        - data: Single stock record with OHLCV data (if found)
        - message: Human-readable status message
        
    HTTP Status Codes:
        - 200: Success - data found for the specified date
        - 404: Not found - no data available for the specified date
        - 500: Server error (database or internal error)
        
    Example Usage:
        GET /api/stocks/date/2021-06-15
        
    Example Response (Success):
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
        
    Example Response (Not Found):
        {
            "success": false,
            "error": "Not found",
            "message": "No stock data found for date 2025-01-01"
        }
    """
    try:
        # Establish database connection
        conn = get_db_connection()
        
        # Execute parameterized query to prevent SQL injection
        # Using ? placeholder and passing date as parameter ensures security
        query = "SELECT * FROM stocks WHERE date = ?"
        stocks_date = conn.execute(query, (date,)).fetchone()

        # Close database connection
        conn.close()
        
        # Check if data was found for the specified date
        if stocks_date:
            # Convert SQLite Row object to dictionary for JSON serialization
            stock_record = {
                'date': stocks_date['date'],                    # Trading date
                'open': float(stocks_date['open']),             # Opening price
                'high': float(stocks_date['high']),             # Highest price of the day
                'low': float(stocks_date['low']),               # Lowest price of the day
                'close': float(stocks_date['close']),           # Closing price
                'adj_close': float(stocks_date['adj_close']),   # Adjusted closing price
                'volume': int(stocks_date['volume'])            # Number of shares traded
            }
            
            # Return successful response with stock data
            return jsonify({
                'success': True,
                'data': stock_record,
                'message': f'Successfully retrieved stock data for {date}'
            }), 200
        else:
            # Return 404 if no data found for the specified date
            # This handles cases like weekends, holidays, or invalid dates
            return jsonify({
                'success': False,
                'error': 'Not found',
                'message': f'No stock data found for date {date}'
            }), 404
        
    except sqlite3.Error as e:
        # Handle database-specific errors
        return jsonify({
            'success': False,
            'error': 'Database Error',
            'message': str(e)
        }), 500

    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


# Application entry point
if __name__ == '__main__':
    # Run Flask development server
    # debug=True enables auto-reload and detailed error pages
    # host='0.0.0.0' makes server accessible from any IP address
    # port=5000 is the default Flask development port
    app.run(debug=True, host='0.0.0.0', port=5000)
