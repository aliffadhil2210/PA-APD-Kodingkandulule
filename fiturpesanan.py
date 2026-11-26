import data
from data import orders, paket, tukang
from helper import clear_screen, enter, minta_angka, tanya_teks, pilih_menu
from tampilan import tampil_paket, tampil_pesanan
from fiturtukang import cari_tukang_siap, bebaskan_tukang
from prettytable import PrettyTable

def buat_nomor_order():
    nomor_baru = data.nomor_order
    data.nomor_order = data.nomor_order + 1
    return nomor_baru

def jumlah_tukang(p):
    return int(p["membutuhkan"].split()[0])

def hitung_total(p, ukuran):
    if p.get("per_meter", True):
        return p["harga"] * ukuran
    return p["harga"]

def cari_order(nomor, daftar):
    for o in daftar:
        if o["no_pesanan"] == nomor:
            return o
    return None

def pesanan_milik(user_login):
    return [o for o in orders if o["username"] == user_login["username"]]

def buat_pesanan(user_login):
    clear_screen()
    print("---( BUAT PESANAN )---")
    print()
    tukang_siap = cari_tukang_siap()
    try:
        if len(tukang_siap) == 0:
            raise ValueError("Maaf, belum ada tukang yang siap.")
        tampil_paket(paket, False)
        ukuran = minta_angka("Ukuran ruangan dalam m2 (0 = batal) : ", 0, 10000)
        if ukuran == 0:
            raise ValueError("Pesanan dibatalkan.")
        nomor = minta_angka("Pilih nomor paket (0 = batal) : ", 0, len(paket))
        if nomor == 0:
            raise ValueError("Pesanan dibatalkan.")
        pilihan = paket[True if nomor > 0 else False]
        butuh = jumlah_tukang(pilihan)
        if len(tukang_siap) < butuh:
            raise ValueError(f"Tukang siap hanya {len(tukang_siap)}, paket butuh {butuh}.")
        if pilihan["sedia"] == False:
            raise ValueError("Paket ini belum tersedia buat sekarang.")
        lokasi = tanya_teks("Lokasi antar jemput").strip()
        if lokasi == "":
            raise ValueError("Lokasimu masih kosong")
    except ValueError as e:
        print(e)
    else:
        no_baru = buat_nomor_order()
        dipakai = tukang_siap[:butuh]
        for t in dipakai:
            t["status"] = "Sibuk"
        total = hitung_total(pilihan, ukuran)
        orders.append({
            "no_pesanan": no_baru,
            "username": user_login["username"],
            "paket": pilihan["nama"],
            "lokasi": lokasi,
            "nama_tukang": [t["nama"] for t in dipakai],
            "total": total,
            "pembayaran": "Belum bayar",
            "status": "Diproses",
        })
        pilihan["stok"] = False
        for t in tukang_siap:
            t["status"] = "Sibuk"
        print("Pesanan berhasil dibuat!")
        print("No.pesanan :", no_baru)
        print("Tukang     :", ", ".join(t["nama"] for t in dipakai))
        print("Total      : Rp", total)
    finally:
        enter()

def lihat_status(user_login):
    clear_screen()
    print("---( STATUS PESANAN )---")
    print()
    clear_screen()
    tabel = PrettyTable(["Nomor", "Paket", "Status"])
    for p in orders:
        if p["username"] == user_login["username"]:
            tabel.add_row([p["no_pesanan"], p["paket"], p["status"]])
    print(tabel)
    enter()

def pembayaran(user_login):
    clear_screen()
    print("---( PEMBAYARAN )---")
    print()
    belum = [o for  o in orders if o["pembayaran"] == "Belum bayar"] 
    if len(belum) == 0:
        print("Nggak ada pesanan yang perlu dibayar.")
    else:
        tampil_pesanan(belum)
        print("Saldo kamu : Rp", user_login["saldo"])
        print()
        nomor = minta_angka("Nomor pesanan yang dibayar (0 = batal) : ", 0, data.nomor_order)
        if nomor == 0:
            print("Pembayaran dibatalkan.")
        else:
            o = cari_order(nomor, belum)
            if o is None:
                print("Pesanan itu nggak ada atau sudah dibayar!")
            elif user_login["saldo"] < o["total"]:
                print("Saldo kurang Rp", o["total"] - user_login["saldo"], "- top up dulu bos.")
            else:
                user_login["saldo"] -= o["total"]
                o["pembayaran"] = "Lunas"
                print("Pembayaran berhasil!")
                print("Sisa saldo : Rp", user_login["saldo"])
    enter()

def hapus_lokasi(user_login):
    clear_screen()
    print("---( HAPUS LOKASI PESANAN )---")
    print()
    bisa = [o for o in orders if o["status"] == "Diproses" and o["pembayaran"] == "Belum bayar"]
    if len(bisa) == 0:
        print("Tidak ada lokasi yang bisa dihapus (harus belum dibayar).")
    else:
        tampil_pesanan(bisa)
        print()
        nomor = minta_angka("Nomor pesanan yang dihapus (0 = batal) : ", 0, data.nomor_order)
        if nomor == 0:
            print("Dibatalkan.")
        else:
            o = cari_order(nomor, bisa)
            if o is None:
                print("Pesanan itu nggak ada atau nggak bisa dihapus!")
            elif pilih_menu(f"Yakin hapus pesanan {nomor} di {o['lokasi']}?", [("Ya", True), ("Tidak", False)]):
                bebaskan_tukang(o["nama_tukang"])
                orders.remove(o)
                print("Lokasi dan pesanannya udah dihapus, tukang dibebaskan lagi.")
            else:
                print("Nggak jadi dihapus.")
    enter()

def status_pembayaran():
    clear_screen()
    print("---( STATUS PEMBAYARAN )---")
    tampil_pesanan(orders, True)
    enter()

def tandai_selesai():
    clear_screen()
    print("---( TANDAI SELESAI )---")
    print()
    diproses = [o for o in orders if o["status"] == "Diproses"]
    if len(diproses) == 0:
        print("Nggak ada pesanan yang lagi diproses.")
    else:
        tampil_pesanan(diproses, True)
        print()
        nomor = minta_angka("Nomor pesanan yang selesai (0 = batal) : ", 0, data.nomor_order)
        if nomor == 0:
            print("Dibatalkan.")
        else:
            o = cari_order(nomor, diproses)
            if o is None:
                print("Pesanan itu nggak ada atau sudah selesai!")
            elif o["pembayaran"] != "Lunas":
                print("Pelanggan belum bayar, belum bisa ditandai selesai!")
            else:
                o["status"] = "Selesai"
                bebaskan_tukang(o["nama_tukang"])
                print("Pesanan", nomor, "selesai, tukang udah siap kerja lagi.")
    enter()

def hitung_pendapatan(daftar, i=0):
    if i >= len(daftar):
        return 0
    sisa = hitung_pendapatan(daftar, i + 1)
    if daftar[i]["status"] == "Selesai":
        return daftar[i]["total"] + sisa
    return sisa

def total_pendapatan():
    clear_screen()
    print("---( TOTAL PENDAPATAN )---")
    print()
    selesai = len([o for o in orders if o["status"] == "Selesai"])
    print("Pesanan selesai   :", selesai)
    print("Total pendapatan  : Rp", hitung_pendapatan(orders))
    enter()