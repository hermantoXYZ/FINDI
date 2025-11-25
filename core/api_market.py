import yfinance as yf
from app.models import Saham

def get_realtime_prices():
    data = []
    saham_list = Saham.objects.all()

    for saham in saham_list:
        ticker_symbol = saham.symbol + ".JK"
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.history(period="2d")

        if not info.empty and len(info) >= 2:
            previous_close = info['Close'].iloc[-2]
            last_price = info['Close'].iloc[-1]
            price_change = last_price - previous_close
            percent_change = (price_change / previous_close) * 100
        else:
            last_price = None
            price_change = None
            percent_change = None

        data.append({
            'symbol': saham.symbol,
            'nama_perusahaan': saham.nama_perusahaan,
            'harga': last_price,
            'perubahan_harga': price_change,
            'persentase': percent_change,
            'sektor': saham.sektor,
        })

    return data

def market_global_stocks():
    stocks = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'AMZN': 'Amazon.com Inc.',
        'GOGL': 'Alphabet Inc.',
        'TSLA': 'Tesla Inc.',
        'NVDA': 'NVIDIA Corporation',
        'META': 'Meta Platforms Inc.',
    }

    data = []
    for symbol, name in stocks.items():
        ticker = yf.Ticker(symbol)

        # ambil data lebih banyak agar tidak kosong
        info = ticker.history(period="5d")

        if not info.empty:
            previous_close = info['Close'].iloc[-2]
            last_price = info['Close'].iloc[-1]
            price_change = last_price - previous_close
            percent_change = (price_change / previous_close) * 100
        else:
            previous_close = last_price = price_change = percent_change = 0

        data.append({
            'symbol': symbol,
            'company_name': name,
            'price': round(last_price, 2),
            'price_change': round(price_change, 2),
            'percent_change': round(percent_change, 2),
        })

    return data