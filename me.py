# ============================================================
# FUNGSI UNTUK MENCARI POSISI KARAKTER DI DALAM MATRIX
# ============================================================

def posisi(matrix, char):
    # Periksa setiap baris pada matrix
    for i, row in enumerate(matrix):

        # Jika karakter ditemukan di baris tersebut
        if char in row:

            # Kembalikan posisi baris dan kolom karakter
            return i, row.index(char)


# ============================================================
# FUNGSI UTAMA PLAYFAIR
# Digunakan untuk encryption maupun decryption
# ============================================================

def playfair(a, b, matrix, encrypt=True):

    # Cari posisi karakter pertama
    # r1 = baris, c1 = kolom
    r1, c1 = posisi(matrix, a)

    # Cari posisi karakter kedua
    # r2 = baris, c2 = kolom
    r2, c2 = posisi(matrix, b)

    # Karena matrix berbentuk n x n,
    # panjang salah satu baris digunakan sebagai ukuran matrix
    n = len(matrix)

    # Saat encryption karakter digeser ke depan (+1)
    # Saat decryption karakter digeser ke belakang (-1)
    arah = 1 if encrypt else -1

    # ========================================================
    # RULE 1: KEDUA KARAKTER BERADA DI BARIS YANG SAMA
    # ========================================================

    if r1 == r2:

        # Geser masing-masing karakter satu posisi
        # ke kanan saat encrypt
        # atau ke kiri saat decrypt
        #
        # Operator % digunakan agar jika sudah berada
        # di ujung matrix, karakter kembali ke awal.
        return matrix[r1][(c1 + arah) % n] + \
               matrix[r2][(c2 + arah) % n]

    # ========================================================
    # RULE 2: KEDUA KARAKTER BERADA DI KOLOM YANG SAMA
    # ========================================================

    if c1 == c2:

        # Geser masing-masing karakter satu posisi
        # ke bawah saat encrypt
        # atau ke atas saat decrypt.
        #
        # Operator % digunakan untuk membuat
        # pergeseran bersifat circular.
        return matrix[(r1 + arah) % n][c1] + \
               matrix[(r2 + arah) % n][c2]

    # ========================================================
    # RULE 3: KEDUA KARAKTER MEMBENTUK RECTANGLE
    # ========================================================

    # Jika tidak berada di baris yang sama
    # dan tidak berada di kolom yang sama,
    # maka kedua karakter membentuk sebuah rectangle.
    #
    # Karakter pertama mengambil kolom karakter kedua.
    # Karakter kedua mengambil kolom karakter pertama.
    return matrix[r1][c2] + matrix[r2][c1]


# ============================================================
# FUNGSI ENCRYPTION
# ============================================================

def encrypt(text, matrix, filler):

    # Spasi dihapus karena Playfair bekerja
    # berdasarkan pasangan karakter.
    text = text.replace(" ", "")

    # Variabel untuk menyimpan hasil ciphertext
    hasil = ""

    # Index untuk membaca plaintext
    i = 0

    # Proses plaintext sampai seluruh karakter selesai dibaca
    while i < len(text):

        # Ambil karakter pertama dari pasangan
        a = text[i]

        # ====================================================
        # KONDISI 1: KARAKTER TERAKHIR TIDAK MEMILIKI PASANGAN
        # ====================================================

        if i + 1 == len(text):

            # Tambahkan filler sebagai pasangan
            b = filler

            # Maju satu karakter
            i += 1

        # ====================================================
        # KONDISI 2: DUA KARAKTER BERURUTAN SAMA
        # ====================================================

        elif text[i] == text[i + 1]:

            # Tidak boleh membuat pasangan seperti:
            # LL, AA, BB, dan sebagainya.
            #
            # Oleh karena itu tambahkan filler.
            b = filler

            # Hanya maju satu karakter.
            #
            # Karakter kedua yang sama akan diproses
            # pada iterasi berikutnya.
            i += 1

        # ====================================================
        # KONDISI 3: KARAKTER BERBEDA
        # ====================================================

        else:

            # Ambil karakter berikutnya sebagai pasangan
            b = text[i + 1]

            # Karena sudah mengambil dua karakter,
            # index langsung maju dua posisi.
            i += 2

        # Kirim pasangan karakter ke fungsi Playfair
        # True berarti melakukan encryption.
        hasil += playfair(a, b, matrix, True)

    # Kembalikan seluruh ciphertext
    return hasil


# ============================================================
# FUNGSI DECRYPTION
# ============================================================

def decrypt(text, matrix):

    # Variabel untuk menyimpan hasil plaintext
    hasil = ""

    # Ciphertext dibaca dua karakter sekaligus
    #
    # Contoh:
    # ABCDEF
    #
    # menjadi:
    # AB
    # CD
    # EF
    for i in range(0, len(text), 2):

        # Kirim dua karakter ke fungsi Playfair
        #
        # False berarti melakukan decryption.
        hasil += playfair(
            text[i],
            text[i + 1],
            matrix,
            False
        )

    # Kembalikan plaintext
    return hasil


# ============================================================
# PROGRAM UTAMA
# ============================================================

# ============================================================
# 1. INPUT BASE CHARACTER
# ============================================================

# User menentukan sendiri karakter yang ingin digunakan.
#
# Base bisa berisi:
# - Huruf
# - Angka
# - Simbol
# - Kombinasi semuanya
#
# Contoh:
# ABCDEFGHIJKLMNOPQRSTUVWXYZ012
# atau
# ABC123!@#
base = input("Masukkan base karakter: ")


# ============================================================
# 2. VALIDASI BASE
# ============================================================

# set() digunakan untuk mendapatkan karakter yang unik.
#
# Jika:
# len(base) != len(set(base))
#
# berarti terdapat karakter yang sama/duplikat.
#
# Contoh:
# ABCDA
#
# Base tersebut tidak valid karena A muncul dua kali.
while len(set(base)) != len(base):

    print("Base tidak boleh memiliki karakter yang sama.")

    # User diminta memasukkan base kembali
    base = input("Masukkan base karakter: ")


# ============================================================
# 3. MENGHITUNG JUMLAH KARAKTER BASE
# ============================================================

# Hitung berapa banyak karakter yang dimasukkan user.
#
# Contoh:
# ABCDEFGHIJKLMNOPQRSTUVWXYZ012
#
# jumlah = 29
jumlah = len(base)


# ============================================================
# 4. MENENTUKAN UKURAN MATRIX
# ============================================================

# Playfair membutuhkan matrix berbentuk n x n.
#
# Oleh karena itu kita mencari nilai n dari akar jumlah
# karakter yang dimasukkan user.
#
# Contoh:
# jumlah = 29
#
# √29 = 5.38
#
# int() membuang angka desimal:
# n = 5
#
# Sehingga matrix yang digunakan adalah:
# 5 x 5 = 25 karakter
n = int(jumlah ** 0.5)


# ============================================================
# 5. MENGHITUNG JUMLAH EXCEPTION
# ============================================================

# Jumlah karakter yang dapat dimasukkan ke matrix
# adalah n x n.
#
# Contoh:
#
# Base = 29 karakter
# Matrix = 5 x 5
# Kapasitas matrix = 25
#
# Maka:
# 29 - 25 = 4
#
# Artinya user harus menentukan 4 karakter
# yang akan dikeluarkan dari matrix.
exception_jumlah = jumlah - (n * n)


# Tampilkan informasi kepada user
print(f"\nJumlah karakter : {jumlah}")
print(f"Matrix          : {n} x {n}")
print(f"Exception       : {exception_jumlah} karakter")


# ============================================================
# 6. INPUT EXCEPTION
# ============================================================

# User memasukkan karakter yang tidak akan digunakan
# di dalam matrix.
#
# Misalnya:
#
# Base = ABCDEFGHIJKLMNOPQRSTUVWXYZ012
# Jumlah = 29
# Matrix = 5 x 5
# Exception = 4
#
# User dapat memasukkan:
# JQ12
exception = input(
    f"Masukkan {exception_jumlah} karakter exception: "
)


# ============================================================
# 7. VALIDASI EXCEPTION
# ============================================================

while (
    # Jumlah exception harus tepat
    len(exception) != exception_jumlah

    # Semua karakter exception harus berasal dari base
    or not set(exception).issubset(set(base))

    # Karakter exception tidak boleh duplikat
    or len(set(exception)) != len(exception)
):

    print("Exception tidak valid.")

    # Minta user memasukkan exception kembali
    exception = input(
        f"Masukkan {exception_jumlah} karakter exception: "
    )


# ============================================================
# 8. MENGHAPUS CHARACTER EXCEPTION DARI BASE
# ============================================================

# Setelah exception valid, karakter tersebut dikeluarkan
# dari base.
#
# Contoh:
#
# Base:
# ABCDEFGHIJKLMNOPQRSTUVWXYZ012
#
# Exception:
# JQ12
#
# Maka chars menjadi:
# ABCDEFGHIKLMNOPRSTUVWXYZ
#
# Jumlahnya sekarang menjadi 25 karakter.
chars = "".join(
    c for c in base
    if c not in exception
)


# ============================================================
# 9. INPUT KEY
# ============================================================

# Key digunakan untuk menentukan urutan karakter
# pada awal matrix.
#
# Contoh:
# MONARCHY
while True:

    key = input("Masukkan key: ")

    # Semua karakter key harus terdapat di BASE.
    #
    # Validasi ini bersifat CASE-SENSITIVE.
    #
    # Misalnya base:
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #
    # Key:
    # MONARCHY
    #
    # valid.
    #
    # Tetapi:
    # Monarchy
    #
    # tidak valid karena:
    # M != m
    if all(c in base for c in key):

        # Jika semua karakter valid,
        # keluar dari while loop.
        break

    # Jika ada satu saja karakter yang tidak ada
    # di dalam base, user harus mengulang.
    print(
        "Key tidak valid! Semua karakter key harus "
        "ada di dalam base dan case-sensitive."
    )


# ============================================================
# 10. MEMBUAT URUTAN KARAKTER BERDASARKAN KEY
# ============================================================

# Variabel kosong untuk menyimpan karakter
# yang akan dimasukkan ke matrix.
urutan = ""


# Program membaca key terlebih dahulu,
# kemudian membaca chars.
#
# Artinya karakter yang terdapat di key
# akan ditempatkan di bagian awal matrix.
for c in key + chars:

    # Karakter harus berasal dari chars
    # dan belum boleh masuk ke urutan sebelumnya.
    #
    # Kondisi ini juga menghilangkan duplikat
    # dari key.
    if c in chars and c not in urutan:

        # Masukkan karakter ke urutan matrix
        urutan += c


# ============================================================
# 11. MEMBENTUK MATRIX
# ============================================================

# String urutan dipotong setiap n karakter.
#
# Contoh n = 5:
#
# MONAR CHYBD EFGIK LPQST UVWXZ
#
# kemudian menjadi:
#
# M O N A R
# C H Y B D
# E F G I K
# L P Q S T
# U V W X Z
matrix = [
    urutan[i:i + n]
    for i in range(0, len(urutan), n)
]


# ============================================================
# 12. MENAMPILKAN MATRIX
# ============================================================

print("\nMatrix:")

# Tampilkan matrix baris demi baris
for row in matrix:

    # " ".join() digunakan agar setiap karakter
    # dipisahkan oleh spasi saat ditampilkan.
    print(" ".join(row))


# ============================================================
# 13. INPUT FILLER
# ============================================================

# Filler digunakan ketika:
#
# 1. Dua karakter dalam pasangan sama
# 2. Plaintext memiliki jumlah karakter ganjil
#
# Contoh:
#
# HELLO
#
# LL tidak boleh menjadi pasangan.
# Maka:
#
# HE LX LO
#
# Jika filler = X.
filler = input("\nMasukkan filler: ")


# ============================================================
# 14. VALIDASI FILLER
# ============================================================

# Filler harus:
# 1. Hanya satu karakter
# 2. Karakter tersebut harus berada di chars
while filler not in chars or len(filler) != 1:

    print(
        "Filler harus satu karakter "
        "yang ada di matrix."
    )

    # User diminta mengulang
    filler = input("Masukkan filler: ")


# ============================================================
# 15. MENU PROGRAM
# ============================================================

# while True membuat menu terus berjalan
# sampai user memilih menu keluar.
while True:

    print("\n1. Encrypt")
    print("2. Decrypt")
    print("3. Keluar")

    # User memilih operasi
    pilihan = input("Pilih: ")


    # ========================================================
    # MENU 1: ENCRYPT
    # ========================================================

    if pilihan == "1":

        # User memasukkan plaintext
        text = input("Plaintext: ")

        # Pastikan setiap karakter plaintext
        # terdapat di dalam chars.
        #
        # Spasi diperbolehkan karena nantinya
        # akan dihapus oleh fungsi encrypt().
        if all(c in chars or c == " " for c in text):

            # Jalankan fungsi encryption
            print(
                "Ciphertext:",
                encrypt(text, matrix, filler)
            )

        else:

            # Jika terdapat karakter yang tidak
            # ada di matrix, tampilkan error.
            print(
                "Ada karakter plaintext "
                "yang tidak ada di matrix."
            )


    # ========================================================
    # MENU 2: DECRYPT
    # ========================================================

    elif pilihan == "2":

        # User memasukkan ciphertext
        text = input("Ciphertext: ")

        # Playfair selalu bekerja dengan pasangan.
        #
        # Oleh karena itu jumlah ciphertext
        # harus genap.
        if len(text) % 2 == 0:

            # Jalankan fungsi decryption
            print(
                "Plaintext:",
                decrypt(text, matrix)
            )

        else:

            # Jika jumlah karakter ganjil,
            # ciphertext dianggap tidak valid.
            print(
                "Ciphertext harus memiliki "
                "jumlah karakter genap."
            )


    # ========================================================
    # MENU 3: KELUAR
    # ========================================================

    elif pilihan == "3":

        # Tampilkan pesan sebelum program berhenti
        print("Program selesai.")

        # break menghentikan while True
        # sehingga program selesai.
        break


    # ========================================================
    # INPUT MENU TIDAK VALID
    # ========================================================

    else:

        # Jika user memasukkan selain:
        # 1, 2, atau 3
        print("Pilihan tidak valid.")