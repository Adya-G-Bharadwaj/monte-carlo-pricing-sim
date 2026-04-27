# monte-carlo-pricing-sim
This project takes a stock ticker from the Yahoo Finance library and prices European call and put options using Monte Carlo methods. It also compares Monte Carlo predictions to Black-Scholes pricing options and visualizes this difference through matplotlib. Designed as a small project to understand and practice equation implementation for Monte Carlo European Pricing, Black-Scholes Analytical Price, and Geometric Brownian Motion Simulation.

## Usage
Install all dependencies (including Yahoo Finance, numpy, scipy, pandas, and matplotlib):  
`pip install -r requirements.txt`

Change intended stock ticker: Add intended NYSE stock ticker at line 9 of monte-carlo-pricing-sim/main.py at `ticker = yf.Ticker("AAPL")`. In the same file, around lines 9-16, you can change implied volatility, strike price, or time to maturity.

Run simulation:  
`python3 main.py`

## Formulas

### Parameters

## Concepts
