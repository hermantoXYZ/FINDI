import requests
from django.utils.dateparse import parse_datetime
from .models import Saham

def update_saham(symbol):
    url = f"https://data-api-saham.andihermanto.id/api/stock/quote?symbol={symbol}"

    r = requests.get(url, timeout=10)
    data = r.json()

    if not data:
        return

    Saham.objects.update_or_create(
        symbol=symbol,
        defaults={
            "short_name": data.get("shortName"),
            "long_name": data.get("longName"),
            "currency": data.get("currency"),

            "price": data.get("regularMarketPrice"),
            "change": data.get("regularMarketChange"),
            "change_pct": data.get("regularMarketChangePercent"),
            "volume": data.get("regularMarketVolume"),
            "open_price": data.get("regularMarketOpen"),
            "time": parse_datetime(data.get("regularMarketTime")),

            "market_cap": data.get("marketCap"),
            "pbv": data.get("priceToBook"),
            "pe": data.get("trailingPE"),
            "forward_pe": data.get("forwardPE"),

            "div_yield": data.get("trailingAnnualDividendYield"),
            "div_rate": data.get("trailingAnnualDividendRate"),

            "eps_ttm": data.get("epsTrailingTwelveMonths"),
            "eps_forward": data.get("epsForward"),
            "eps_year": data.get("epsCurrentYear"),
            "price_eps_year": data.get("priceEpsCurrentYear"),

            "shares_outstanding": data.get("sharesOutstanding"),

            "prev_close": data.get("previousClose"),
            "day_high": data.get("dayHigh"),
            "day_low": data.get("dayLow"),

            "avg_vol_3m": data.get("averageDailyVolume3Month"),
            "avg_vol_10d": data.get("averageDailyVolume10Day"),

            "book_value": data.get("bookValue"),
            "confidence": data.get("customPriceAlertConfidence"),

            "week52_high": data.get("fiftyTwoWeekHigh"),
            "week52_low": data.get("fiftyTwoWeekLow"),
            "week52_high_change_pct": data.get("fiftyTwoWeekHighChangePercent"),
            "week52_high_change": data.get("fiftyTwoWeekHighChange"),
            "week52_low_change_pct": data.get("fiftyTwoWeekLowChangePercent"),
            "week52_low_change": data.get("fiftyTwoWeekLowChange"),

            "firt_trade_date": data.get("firstTradeDateMilliseconds"),
        }
    )
