import yfinance as yf
import pandas as pd
import numpy as np
import sys


def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def evaluate_stock(ticker):
    stock = yf.Ticker(ticker)

    # Historiske data
    hist = stock.history(period="1y")

    # Moving averages
    hist["MA50"] = hist["Close"].rolling(50).mean()
    hist["MA200"] = hist["Close"].rolling(200).mean()

    # RSI
    hist["RSI"] = calculate_rsi(hist["Close"])

    latest = hist.iloc[-1]

    score = 0
    reasons = []

    # Teknisk analyse
    if latest["Close"] > latest["MA200"]:
        score += 2
        reasons.append("Pris over MA200 (bullish)")
    else:
        score -= 2
        reasons.append("Pris under MA200 (bearish)")

    if latest["MA50"] > latest["MA200"]:
        score += 2
        reasons.append("Golden trend (MA50 > MA200)")
    else:
        score -= 2
        reasons.append("Weak trend (MA50 < MA200)")

    if latest["RSI"] < 30:
        score += 1
        reasons.append("Oversolgt (potensiell rebound)")
    elif latest["RSI"] > 70:
        score -= 1
        reasons.append("Overkjøpt")

    # Fundamentale data
    info = stock.info

    pe = info.get("trailingPE", None)
    profit_margin = info.get("profitMargins", None)
    debt_equity = info.get("debtToEquity", None)
    revenue_growth = info.get("revenueGrowth", None)

    if pe and pe < 25:
        score += 1
        reasons.append(f"P/E OK ({pe})")
    elif pe:
        score -= 1
        reasons.append(f"P/E høy ({pe})")

    if revenue_growth and revenue_growth > 0.10:
        score += 2
        reasons.append(f"Sterk vekst ({revenue_growth*100:.1f}%)")

    if profit_margin and profit_margin > 0.15:
        score += 1
        reasons.append(f"God margin ({profit_margin*100:.1f}%)")

    if debt_equity and debt_equity < 100:
        score += 1
        reasons.append(f"Sunn gjeld ({debt_equity})")
    elif debt_equity:
        score -= 1
        reasons.append(f"Høy gjeld ({debt_equity})")

    # Konklusjon
    if score >= 5:
        verdict = "STRONG BUY"
    elif score >= 2:
        verdict = "BUY / WATCHLIST"
    elif score >= 0:
        verdict = "NEUTRAL"
    else:
        verdict = "AVOID / BEARISH"

    print(f"\nTicker: {ticker}")
    print(f"Score: {score}")
    print(f"Verdict: {verdict}")
    print("\nReasons:")
    for r in reasons:
        print("-", r)


# Eksempel
# stock_input = str(input("Skriv inn ticker (f.eks. AAPL): "))
stock_input = str(sys.argv[1]+".ol")

evaluate_stock(stock_input)