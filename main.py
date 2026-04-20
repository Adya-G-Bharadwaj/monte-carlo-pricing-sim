import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import simulate_gbm_paths, monte_carlo_option_price, black_scholes_price
import yfinance as yf

#Parameters using Yfinance as API call
ticker = yf.Ticker("AAPL")
S0= ticker.info["currentPrice"] #stock current price
K = round(S0 / 5) * 5 #strike price
r = 0.05 #risk-free rate
sigma = ticker.option_chain("2026-08-21").calls["impliedVolatility"].mean() #implied volatility
T = 1.0 #Time to maturity (yrs)
steps = 252 #Steps per path (daily)
n_paths = 1000

#GBM paths
t, paths = simulate_gbm_paths(S0, r, sigma, T, steps, n_paths)

#Monte Carlo pricing
mc_call = monte_carlo_option_price(paths, K, r, T, option_type='call')
mc_put = monte_carlo_option_price(paths, K, r, T, option_type='put')

#Black-Scholes pricing
bs_call = black_scholes_price(S0, K, r, sigma, T, option_type='call')
bs_put = black_scholes_price(S0, K, r, sigma, T, option_type='put')

#Live Price differences
diff_call = mc_call - bs_call
diff_put = mc_put - bs_put

#dataframe
df_prices = pd.DataFrame({
    'Method': ['Monte Carlo', 'Black-Scholes'],
    'Call Price': [mc_call, bs_call],
    'Put Price': [mc_put, bs_put]
})

#ANIMATION
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('Monte Carlo Stock Price Simulation', fontsize=16, color='white')
ax.set_xlabel('Time (years)')
ax.set_ylabel('Stock Price')

#parameters
params_text = f"Strike: {K}\nVolatility: {sigma}\nRisk-free rate: {r}\nT: {T}"
param_box = ax.text(0.02, 0.95, params_text, transform=ax.transAxes, fontsize=12, color='white', va='top', bbox=dict(facecolor='#333333', alpha=0.7))

# Option price display
price_box = ax.text(0.98, 0.95, '', transform=ax.transAxes, fontsize=12, color='white', va='top', ha='right', bbox=dict(facecolor='#333333', alpha=0.7))

#plot lines
lines = [ax.plot([], [], lw=1, alpha=0.5)[0] for _ in range(20)]  # Animate 20 paths

ax.set_xlim(0, T)
ax.set_ylim(np.min(paths), np.max(paths))

def animate(i):
    for j, line in enumerate(lines):
        line.set_data(t[:i], paths[j, :i])
    #Update price box
    price_box.set_text(f"MC Call: {mc_call:.4f}\nBS Call: {bs_call:.4f}\nDiff: {diff_call:.4f}\n\nMC Put: {mc_put:.4f}\nBS Put: {bs_put:.4f}\nDiff: {diff_put:.4f}")
    return lines + [price_box]

# ani = animation.FuncAnimation(fig, animate, frames=steps+1, interval=20, blit=True)
ani = animation.FuncAnimation(fig, animate, interval=20, blit=True)

plt.tight_layout()
plt.show()

#Price comparison table
print("\nOption Price Comparison:")
print(df_prices.to_string(index=False))
print(f"\nCall Price Difference (MC - BS): {diff_call:.4f}")
print(f"Put Price Difference (MC - BS): {diff_put:.4f}")
