from data import paket, MAKS_HARGA
from helper import clear_screen, enter, pilih_menu, tanya_teks, minta_angka
from tampilan import tampil_paket
from fiturtukang import ambil_nomor
import inquirer

def nama_paket_dipakai(nama, kecuali=None):
    for i in range(len(paket)):
        if i != kecuali and paket[i]["nama"].lower() == nama.lower():
            return True
    return False

def minta_teks(pesan, boleh_kosong=False):
    while True:
        teks = tanya_teks(pesan).strip()
        if teks or boleh_kosong:
            return teks
        print("Tidak boleh kosong!")
        
def kelola_paket():
    while True:
        clear_screen()
        print("---( KELOLA PAKET )---")
        print()
        tampil_paket(paket, False)
        print()
        sub = pilih_menu("Pilih", [("Tambah paket", 1), ("Ubah paket", 2), ("Ubah status paket", 3), ("Hapus Paket", 4), ("Kembali", 0)])
        if sub == 0:
            break
        elif sub == 1:
            nama = tanya_teks("Nama paket").strip()
            if nama == "":
                print("Nama nggak boleh kosong!")
            elif nama_paket_dipakai(nama):
                print("Yahh nama sudah ada!")
            else:
                harga = minta_angka("Harga per m2 : ", 1, MAKS_HARGA)
                fitur = minta_teks("Fitur")
                butuh = minta_angka("Jumlah tukang yang dibutuhkan : ", 1, 5)
                paket.append({"nama": nama, "harga": harga, "fitur": fitur, "membutuhkan": f"{butuh} tukang", "sedia": True})
                print("Paketnya udah ditambah!")
            enter()
        elif sub == 2:
            if len(paket) == 0:
                print("Belum ada paket!")
                enter()
                continue
            idx = ambil_nomor(paket)
            if idx is None:
                enter()
                continue
            nama = tanya_teks("Nama baru").strip()
            if nama == "":
                print("Nama nggak boleh kosong!")
            elif nama_paket_dipakai(nama, idx):
                print("Nama itu sudah ada!")
            else:
                harga = minta_angka("Harga baru per m2 : ", 1, MAKS_HARGA)
                fitur = minta_teks("Fitur baru")
                butuh = minta_angka("Jumlah tukang yang dibutuhkan : ", 1, 5)
                paket[idx]["nama"] = nama
                paket[idx]["harga"] = harga
                paket[idx]["fitur"] = fitur
                paket[idx]["membutuhkan"] = f"{butuh} tukang"
                print("Paketnya udah diubah!")
            enter()
        elif sub == 3:
            if len(paket) == 0:
                print("Belum ada paket!")
                enter()
                continue
            idx = ambil_nomor(paket)
            if idx is None:
                enter()
                continue
            status = pilih_menu("Status baru", [("Tersedia", True), ("Habis", False)])
            paket[idx]["sedia"] = status
            print("Status", paket[idx]["nama"], "udah jadi", "Tersedia" if status else "Habis")
            enter()
        elif sub == 4:
            if len(paket) == 0:
                print("Belum ada paket!")
                enter()
                continue
            idx = ambil_nomor(paket)
            if idx is None:
                enter()
                continue
            konfirmasi = pilih_menu(f"Yakin mau hapus paket {paket[idx]['nama']}?", [("Ya", True), ("Tidak", False)])
            if konfirmasi:
                del paket[idx]
                print("Paketnya udah dihapus!")
            else:
                print("Paketnya nggak jadi dihapus.")
            enter()