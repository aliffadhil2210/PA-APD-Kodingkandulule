from helper import clear_screen, pilih_menu
from autentikasi import lihat_pengguna
from fiturtukang import kelola_tukang, lihat_tukang
from fiturpaket import kelola_paket
from fiturpesanan import buat_pesanan, lihat_status, pembayaran, hapus_lokasi, status_pembayaran, tandai_selesai, total_pendapatan
from fitursaldo import topup_saldo, jumlah_saldo

def menu_admin():
    while True:
        clear_screen()
        print("---( Yang Atmin Atmin Aja )---")
        print()
        menu = pilih_menu("Pilih menunya bos", [
            ("Kelola Tukang", 1),
            ("Kelola Paket", 2),
            ("Total Pendapatan", 3),
            ("Lihat Pengguna", 4),
            ("Tandai Selesai", 5),
            ("Status Pembayaran", 6),
            ("Logout", 0),
        ])
        if menu == 0:
            break
        elif menu == 1:
            kelola_tukang()
        elif menu == 2:
            kelola_paket()
        elif menu == 3:
            total_pendapatan()
        elif menu == 4:
            lihat_pengguna()
        elif menu == 5:
            tandai_selesai()
        elif menu == 6:
            status_pembayaran()
            
def menu_pelanggan(user_login):
    while True:
        clear_screen()
        print("---( MENU PELANGGAN )---")
        menu = pilih_menu("Pilih menu", [
            ("Lihat Tukang", 1),
            ("Lihat Status", 2),
            ("Buat Pesanan", 3),
            ("Jumlah Saldo", 4),
            ("Top Up Saldo", 5),
            ("Pembayaran", 6),
            ("Hapus Lokasi Pesanan", 7),
            ("Logout", 0),
        ])
        if menu == 0:
            break
        elif menu == 1:
            lihat_tukang()
        elif menu == 2:
            lihat_status(user_login)
        elif menu == 3:
            buat_pesanan(user_login)
        elif menu == 4:
            jumlah_saldo(user_login)
        elif menu == 5:
            topup_saldo(user_login)
        elif menu == 6:
            pembayaran(user_login)
        elif menu == 7:
            hapus_lokasi(user_login)