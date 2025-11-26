from app.models import Saham   # sesuaikan nama app-mu
from .utils import update_saham

def update_all_saham():
    # ambil semua symbol dari database
    symbols = Saham.objects.values_list("symbol", flat=True)

    for symbol in symbols:
        update_saham(symbol)

    print("Semua saham berhasil di-update.")
