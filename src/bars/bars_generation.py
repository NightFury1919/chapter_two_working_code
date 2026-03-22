import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import seaborn as sns
import scipy.stats as stats


def delta(df):
    a = np.diff(df['Price'])
    a = np.insert(a, 0, 0)
    df['Delta'] = a
    return df

def labelling(df):
    b = np.ones(len(df['Price']))
    for i, delta in enumerate(df['Delta']):
        if i > 0:
            if delta == 0:
                b[i] = b[i-1]
            else:
                b[i] = abs(delta) / delta
    df['Label'] = b
    return df

def initial_conditions(df):
    prob = pd.DataFrame(pd.pivot_table(df, index='Label', values='Price', aggfunc='count'))
    prob = np.array(prob)
    p_b = prob[1]/(prob[0]+prob[1])
    p_s = prob[0]/(prob[0]+prob[1])
    return p_b, p_s

def bar_gen_run(df, thresh):
    cumm, open, low, high, close, cumm_vol, vol_price, b, s = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    collector, bar, thresh_buffer = [], [], []

    for i, (label, price, date, volume) in enumerate(zip(df['Label'], df['Price'], df['Date'], df['Volume'])):
        if label == 1:
            b = b + label
        else:
            s = s + label
        theta = max(b, abs(s))

        cumm_vol = cumm_vol + volume
        vol_price = vol_price + (price * volume)
        collector.append(price)
        if theta >= thresh:
            open = collector[0]
            high = np.max(collector)
            low = np.min(collector)
            close = collector[-1]
            vwap = vol_price / cumm_vol
            bar.append((date, i, open, low, high, close, vwap))
            a = len(collector) * max(((b/len(collector)), (1-(b/len(collector)))))
            thresh_buffer.append(a)
            if i > 500000: thresh = np.average(thresh_buffer)
            theta, open, low, high, close, cumm_vol, vol_price, b, s = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            collector = []
    cols = ['Date', 'Index', 'Open', 'Low', 'High', 'Close', 'Vwap']
    run_bar = pd.DataFrame(bar, columns= cols)
    return run_bar

def bar_gen(df, thresh):
    cumm, open, low, high, close, cumm_vol, vol_price, b = 0, 0, 0, 0, 0, 0, 0, 0
    collector, bar, thresh_buffer = [], [], []

    for i, (label, price, date, volume) in enumerate(zip(df['Label'], df['Price'], df['Date'], df['Volume'])):
        if label == 1:
            b = b + 1
        cumm = cumm + label
        cumm_vol = cumm_vol + volume
        vol_price = vol_price + (price * volume)
        collector.append(price)
        if abs(cumm) >= thresh:
            open = collector[0]
            high = np.max(collector)
            low = np.min(collector)
            close = collector[-1]
            vwap = vol_price / cumm_vol
            bar.append((date, i, open, low, high, close, vwap))
            a = len(collector) * abs((2*(b/len(collector)))-1)
            thresh_buffer.append(a)
            if i > 500000: thresh = np.average(thresh_buffer)
            cumm, open, low, high, close, cumm_vol, vol_price, b = 0, 0, 0, 0, 0, 0, 0, 0
            collector = []
    cols = ['Date', 'Index', 'Open', 'Low', 'High', 'Close', 'Vwap']
    imbalance_bar = pd.DataFrame(bar, columns= cols)
    return imbalance_bar

def volume_bars(df, thresh):
    cumm_vol = 0
    vol_price = 0
    collector = []
    bars = []

    for i, (price, volume, date) in enumerate(zip(df['Price'], df['Volume'], df['Date'])):
        cumm_vol += volume
        vol_price += price * volume
        collector.append(price)

        if cumm_vol >= thresh:
            open_p = collector[0]
            high_p = np.max(collector)
            low_p = np.min(collector)
            close_p = collector[-1]
            vwap = vol_price / cumm_vol

            bars.append((date, i, open_p, low_p, high_p, close_p, vwap))

            # reset
            cumm_vol = 0
            vol_price = 0
            collector = []

    cols = ['Date', 'Index', 'Open', 'Low', 'High', 'Close', 'Vwap']
    return pd.DataFrame(bars, columns=cols)

def dollar_bars(df, thresh):
    cumm_dollar = 0
    cumm_vol = 0
    vol_price = 0
    collector = []
    bars = []

    for i, (price, volume, date) in enumerate(zip(df['Price'], df['Volume'], df['Date'])):
        dollar = price * volume
        cumm_dollar += dollar
        cumm_vol += volume
        vol_price += dollar
        collector.append(price)

        if cumm_dollar >= thresh:
            open_p = collector[0]
            high_p = np.max(collector)
            low_p = np.min(collector)
            close_p = collector[-1]
            vwap = vol_price / cumm_vol

            bars.append((date, i, open_p, low_p, high_p, close_p, vwap))

            # reset
            cumm_dollar = 0
            cumm_vol = 0
            vol_price = 0
            collector = []

    cols = ['Date', 'Index', 'Open', 'Low', 'High', 'Close', 'Vwap']
    return pd.DataFrame(bars, columns=cols)


