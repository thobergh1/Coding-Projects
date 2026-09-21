import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
import time

# Create input field for our desired stock

tickers = [
    "AAPL", "TSLA", "MSFT", "AMZN", "GOOG", "FB", "NVDA", "V", "MA", "JPM", "BABA", 
    "BRK.A", "WMT", "DIS", "PYPL", "PFE", "NKE", "INTC", "IBM", "GME", "AMC", "CCL",
    "ZOM", "SNDL", "SPCE", "TSNP", "APHA", "PLTR", "TLRY", "FUBO", "SQ", "AFRM", 
    "BBBY", "LUV", "NKLA", "PRST", "SENS", "SOS", "NOK", "IMMP", "FCEL", "SEAC", 
    "HCMC", "BCRX", "XSPA", "ENPH", "GEVO", "AQST", "ACB", "VYNE", "TELL", "GILT", 
    "OSTK", "ENZ", "IFMK", "KOSS", "DGLY", "NAK", "IMV", "XELB", "SINT", "VLRX", 
    "TRNX", "GNUS"
]

norske_tickers = [ 
    "5PG.OL","AASB.OL","ABG.OL","ABL.OL","ADS.OL","AFG.OL","AGLX.OL","AIRX.OL",
    "AKAST.OL","AKER.OL","AKBM.OL","AKRBP.OL","ACC.OL","AKH.OL","AKSO.OL",
    "AKOBO.OL","AKVA.OL","ALT.OL","AMSC.OL","ANDF.OL","ABTEC.OL","AQUIL.OL",
    "ARCH.OL","ABS.OL","AFISH.OL","AZT.OL","AFK.OL","ARGEO.OL","ARR.OL","ATEA.OL",
    "ASAS.OL","ASA.OL","AURA.OL","AURG.OL","AUSS.OL","AUTO.OL","AGAS.OL","AWDR.OL",
    "ALNG.OL","ACR.OL", "AIX.OL","B2I.OL","BAKKA.OL","BALT.OL","BARRA.OL","BMK.OL",
    "BCS.OL", "BGBIO.OL", "BEWI.OL", "BIEN.OL","BFISH.OL","BSP.OL","BNOR.OL",
    "BONHR.OL","BOR.OL","BRG.OL","BOUV.OL","BRUT.OL","BWE.OL","BWLPG.OL","BWO.OL",
    "BMA.OL","CADLR.OL","CAMBI.OL","CAPSL.OL","CAVEN.OL","CRNA.OL","CSS.OL",
    "CLOUD.OL","CODE.OL","COSH.OL","CONTX.OL","CLCO.OL","CRAYN.OL","CYVIZ.OL",
    "DVD.OL","DSRT.OL","DNB.OL","DNO.OL","DOFG.OL","DDRIL.OL","EAM.OL","EWIND.OL",
    "EIOF.OL","EMGS.OL","ELIMP.OL","ELK.OL","ELABS.OL","ELMRA.OL","ELO.OL",
    "ENDUR.OL","ENERG.OL","ENSU.OL","ENTRA.OL","ENVIP.OL","EQNR.OL","EQVA.OL",
    "EPR.OL","EXTX.OL","FFSB.OL","FLNG.OL","FRO.OL","GENT.OL","G2MNO.OL","GIGA.OL",
    "GJF.OL","GEOS.OL","GOGL.OL","GOD.OL","GEM.OL","GSF.OL","GRONG.OL","GYL.OL",
    "HAFNI.OL","HGSB.OL","HAV.OL","HKY.OL","HAVI.OL","HERMA.OL","HEX.OL","HPUR.OL",
    "HSHP.OL","HBC.OL","HRGI.OL","HUDL.OL","HDLY.OL","HUNT.OL","HYPRO.OL","HYN.OL",
    "HAUTO.OL","HSPG.OL","ISLAX.OL","IDEX.OL","INDCT.OL","INIFY.OL","ININ.OL",
    "INSTA.OL","IWS.OL","IOX.OL","ITERA.OL","JIN.OL","JAREN.OL","KLDVK.OL,",
    "KID.OL","KIT.OL","KCC.OL","KMCP.OL","KOMPL.OL","KOA.OL","KOG.OL","KRAB.OL",
    "LSG.OL","LIFE.OL","LIFES.OL","LINK.OL","LOKO.OL","LUMI.OL","LYTIX.OL","MVW.OL",
    "MGN.OL","MVE.OL","MEDI.OL","MELG.OL","MORLD.OL","MOBA.OL","MOWI.OL","MPCC.OL",
    "MPCES.OL","MULTI.OL","MAS.OL","NAPA.OL","NAVA.OL","NKR.OL","NEL.OL","NEXT.OL",
    "NISB.OL","NORAM.OL","NORBT.OL","NCOD.OL","NORCO.OL","NORDH.OL","NOAP.OL",
    "NOFIN.OL","NOHAL.OL","NOM.OL","NOD.OL","NTG.OL","NORSE.OL","NHY.OL",
    "NTI.OL","NSKOG.OL","NORTH.OL","NOL.OL","NAS.OL","NBX.OL","NRC.OL","NYKD.OL",
    "OBSRV.OL","OCEAN.OL","OSUN.OL","ODL.OL","ODF.OL","ODFB.OL","OTL.OL","OKEA.OL",
    "OET.OL","OLT.OL","OMDA.OL","ONCIN.OL","ORK.OL","OTEC.OL","OTOVO.OL","PEN.OL",
    "PLSV.OL","PARB.OL","PCIB.OL","PSE.OL","PNOR.OL","PEXIP.OL","PHLY.OL","PHO.OL",
    "PPG.OL","POL.OL","PLT.OL","PRS.OL","PROT.OL","PROXI.OL","PRYME.OL","PUBLI.OL",
    "PYRUM.OL","QEC.OL","RANA.OL","REACH.OL","RECSI.OL","REFL.OL","RIVER.OL","ROGS.OL",
    "ROMER.OL","ROM.OL","ROMSB.OL","SDSD.OL","SAGA.OL","SALM.OL","SALME.OL","SATS.OL",
    "SCANA.OL","SCATC.OL","SCHA.OL","SCHB.OL","SEA1.OL","SBX.OL","SEAPT.OL","SBO.OL",
    "SHLF.OL","SDNS.OL","SKAND.OL","SKUE.OL","SMCRT.OL","SMOP.OL","SOFTX.OL","SOGN.OL",
    "STECH.OL","SOFF.OL","SB68.OL","MING.OL","SB1NO.OL","MORG.OL","SOr.OL","SVEG.OL",
    "SPOG.OL","SNOR.OL","SPOL.OL","HELG.OL","NONG.OL","RING.OL","SOAG.OL","SPIR.OL",
    "SPOT.OL","STST.OL","STSU.OL","SNI.OL","STB.OL","STRO.OL","SUBC.OL","SUNSB.OL",
    "TECH.OL","TEKNA.OL","TEL.OL","TGS.OL","KING.OL","TRMED.OL","TIETO.OL","TOM.OL",
    "TRE.OL","TRSB.OL","TYSB.OL","VDI.OL","VEI.OL","VTURA.OL","VISTN.OL","VVL.OL",
    "VOW.OL","VGM.OL","VAR.OL","WAWI.OL","WSTEP.OL","WEST.OL","WWI.OL","WWIB.OL",
    "XPLRA.OL","XXL.OL","YAR.OL","ZAL.OL","ZAP.OL","ZLNA.OL","ZENA.OL"
]


# url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# headers = {"User-Agent": "Mozilla/5.0"}
# html = requests.get(url, headers=headers).text
# sp500_tickers = pd.read_html(html)[0]['Symbol'].tolist()


stock_data = {}

# ----- RSI Calculation -----
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

print("Fetching data. This might take a while")




for ticker in norske_tickers:
    # Retrieve stock data frame (df) from yfinance API at an interval of 1d
    df = yf.download(ticker, period="1y", interval="1d")
    time.sleep(5)
    if df.empty:
        print(f"Data for {ticker} ble ikke funnet.")
        continue

    volumes = df["Volume"].fillna(0).values.astype(int).flatten()
    dates = df.index

    if len(volumes) < 30:
        print(f"Ikke nok data for {ticker}")
        continue
    else:
        # Extract the volume, stock prices, and dates
        stock_prices = df["Close"].values
        stock_price_yesterday = stock_prices[-2]

        dates = df.index

        # Get yesterday's volume 
        volume_yesterday = volumes[-2]

        # Get the volumes for the past days (all except the last one)
        volume_past_days = volumes[:-1]

        # Calculate the first and third quartiles (Q1 and Q3)
        Q1 = np.percentile(volume_past_days, 25)
        Q3 = np.percentile(volume_past_days, 75)

        # Calculate the Interquartile Range (IQR)
        IQR = Q3 - Q1

        # Define the lower and upper bounds for identifying outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Remove outliers: volumes that are outside the bounds
        filtered_volumes = [vol for vol in volume_past_days if lower_bound <= vol <= upper_bound]

        # Sort the remaining volumes
        filtered_volumes.sort()

        # Remove the 10 lowest and 10 highest volumes from the sorted list
        trimmed_volumes = np.array(filtered_volumes[10:-10])

        # Calculate the mean volume of the trimmed volumes
        mean_value = trimmed_volumes.mean()

        # Mean value not trimmed
        # mean_value = np.array(filtered_volumes).mean()


        mean = round(volume_yesterday/mean_value, 2)

        df['RSI'] = calculate_rsi(df['Close'])
        rsi_previous_day = df['RSI'].iloc[-2]


        if pd.isna(rsi_previous_day):
            rsi_previous_day = 50
        
        volume_price = round(volume_yesterday*stock_price_yesterday[0], 2)

        stock_data[ticker] = {
            "mean_volume": mean,
            "volume_yesterday": volume_yesterday,
            "rsi": int(rsi_previous_day),
            "total_volume_nok": volume_price
        }

sorted_stock_data_mean = dict(sorted(stock_data.items(), key=lambda x: x[1]["mean_volume"], reverse=True))
sorted_stock_data_rsi = dict(sorted(stock_data.items(), key=lambda x: x[1]["rsi"], reverse=True))



print("Sell")
print(f"{'Stock':<10} | {'RSI':>5} | {'Volume':>8}")
print("-------------------------------")
# Iterer gjennom aksjene og skriv ut verdiene formatert
for ticker, data in sorted_stock_data_rsi.items():
    if data['rsi'] >= 70:
        print(f"{ticker:<10} | {data['rsi']:>5} | {data['volume_yesterday']:>10}, | nok:{data['total_volume_nok']:>18}")
print()

print("Buy")
print(f"{'Stock':<10} | {'RSI':>5} | {'Volume':>8}")
print("-------------------------------")
# Iterer gjennom aksjene og skriv ut verdiene formatert
for ticker, data in sorted_stock_data_rsi.items():
    if data['rsi'] <= 30:
        print(f"{ticker:<10} | {data['rsi']:>5} | {data['volume_yesterday']:>10}, | nok:{data['total_volume_nok']:>18}")
print()

print(f"{'Stock':<10} | {'Mean':>5} | {'Volume':>8}")
print("-------------------------------")
# Iterer gjennom aksjene og skriv ut verdiene formatert
for ticker, data in sorted_stock_data_mean.items():
    if data['mean_volume'] >= 1:
        print(f"{ticker:<10} | {data['mean_volume']:>5} | {data['volume_yesterday']:>10}, | nok:{data['total_volume_nok']:>18}")