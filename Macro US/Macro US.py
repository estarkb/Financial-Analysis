import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas_datareader.data as web
start = datetime(1987,1,1)

#S&P
start = datetime(1987,1,1)
sp = web.get_data_yahoo(["^GSPC"], start).fillna(method="ffill")
sp = sp["Close"]
sp = sp.T
sp = sp.groupby(pd.PeriodIndex(sp.columns, freq='Q'), axis=1).mean()
sp = sp.T

#Data
data = pd.read_excel(r"data.xlsx", index_col="Fecha").dropna()
percentiles = data.rank(pct=True)
percentiles[1] = 1-percentiles[1]
percentiles[2] = 1-percentiles[2]
percentiles[3] = 1-percentiles[3]
percentiles[4] = 1-percentiles[4]
percentiles[5] = 1-percentiles[5]
aphades_macro = pd.DataFrame(percentiles.mean(axis=1), columns=["percentil"])

from scipy import stats
aphades_macro = pd.DataFrame(stats.zscore(aphades_macro), columns=["modelo"], index=percentiles.index)
aphades_macro = aphades_macro.rank(pct=True)

#Gráfico
ax = aphades_macro.plot()
plt.axvspan("1990-7-1", "1991-3-1", alpha=0.3, color='red') #S&L
plt.axvspan("2001-3-1", "2001-11-1", alpha=0.3, color='red') #Dotcom
plt.axvspan("2007-12-1", "2009-5-1", alpha=0.3, color='red') #Subprime (aproximación fechas basados en FRED)
plt.axhline(0.20, color='black', linewidth=1, linestyle="--")
plt.axhline(0.90, color='black', linewidth=1, linestyle="--")
plt.title("US Macro")
ax1 = ax.twinx()
sp['^GSPC'].plot.area(ax=ax1, color='b', alpha=0.3)