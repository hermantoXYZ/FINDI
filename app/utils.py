# utils.py
import yfinance as yf
from django.utils import timezone
from datetime import timedelta
from .models import Saham

def get_realtime_prices():
    saham_sample = Saham.objects.first()
    batas_waktu = timezone.now() - timedelta(minutes=30)
    
    perlu_update = False
    if not saham_sample or not saham_sample.last_updated:
        perlu_update = True
    elif saham_sample.last_updated < batas_waktu:
        perlu_update = True

    if perlu_update:
        try:
            update_data_saham_lokal()
        except Exception as e:
            print(f"⚠️ Gagal update saham: {e}")

    data = Saham.objects.all().values(
        'symbol', 'nama_perusahaan', 'last_price', 
        'price_change', 'percent_change', 'sektor'
    )
    return data

def update_data_saham_lokal():
    all_saham = Saham.objects.all()
    if not all_saham:
        return
    tickers_list = [f"{s.symbol}.JK" for s in all_saham]
    tickers_str = " ".join(tickers_list)
    
    df = yf.download(tickers_str, period="5d", group_by='ticker', progress=False)
    
    updates = []
    for saham in all_saham:
        symbol_jk = f"{saham.symbol}.JK"
        
        try:
            if len(all_saham) == 1:
                hist = df # Jika cuma 1 saham, langsung dataframe
            else:
                if symbol_jk in df.columns.levels[0]: # Cek apakah ticker ada di hasil
                    hist = df[symbol_jk]
                else:
                    continue

            # Bersihkan data kosong
            hist = hist.dropna(subset=['Close'])

            if not hist.empty and len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                last_price = hist['Close'].iloc[-1]
                
                # Hitung kenaikan/penurunan
                change = last_price - prev_close
                pct_change = (change / prev_close) * 100
                
                # Update field di object memory
                saham.last_price = last_price
                saham.price_change = change
                saham.percent_change = pct_change
                saham.last_updated = timezone.now()
                
                updates.append(saham)
                
        except Exception as e:
            print(f"Skip {saham.symbol}: {e}")

    # Simpan ke DB sekaligus (Bulk Update) agar hemat koneksi
    if updates:
        Saham.objects.bulk_update(updates, ['last_price', 'price_change', 'percent_change', 'last_updated'])

