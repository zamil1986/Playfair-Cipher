# ============================================================
# FUNGSI MENCARI POSISI KARAKTER DI DALAM MATRIX
# ============================================================

def posisi(matrix, char):
    # Periksa setiap baris matrix
    for i, row in enumerate(matrix):

        # Jika karakter ditemukan
        if char in row:

            # Kembalikan posisi baris dan kolom
            return i, row.index(char)


# ============================================================
# FUNGSI PLAYFAIR
# Digunakan untuk ENCRYPT dan DECRYPT
# ============================================================

def playfair(a, b, matrix, encrypt=True):

    # Cari posisi karakter pertama
    r1, c1 = posisi(matrix, a)

    # Cari posisi karakter kedua
    r2, c2 = posisi(matrix, b)

    # Ukuran matrix
    n = len(matrix)

    # Encrypt = maju
    # Decrypt = mundur
    arah = 1 if encrypt else -1

    # --------------------------------------------------------
    # RULE 1: KEDUA KARAKTER BERADA DI BARIS YANG SAMA
    # --------------------------------------------------------

    if r1 == r2:
        return matrix[r1][(c1 + arah) % n] + \
               matrix[r2][(c2 + arah) % n]

    # --------------------------------------------------------
    # RULE 2: KEDUA KARAKTER BERADA DI KOLOM YANG SAMA
    # --------------------------------------------------------

    if c1 == c2:
        return matrix[(r1 + arah) % n][c1] + \
               matrix[(r2 + arah) % n][c2]

    # --------------------------------------------------------
    # RULE 3: MEMBENTUK RECTANGLE
    # --------------------------------------------------------

    # Tukar posisi kolom kedua karakter
    return matrix[r1][c2] + matrix[r2][c1]


# ============================================================
# FUNGSI MEMBUAT LETTER PAIRS
# ============================================================

def buat_pairs(text, filler):

    # Hapus semua spasi dari plaintext
    # karena Playfair bekerja dengan pasangan karakter.
    text = text.replace(" ", "")

    # List untuk menyimpan pasangan karakter
    pairs = []

    # Index untuk membaca plaintext
    i = 0

    # Proses sampai semua karakter selesai dibaca
    while i < len(text):

        # Ambil karakter pertama
        a = text[i]

        # ----------------------------------------------------
        # JIKA KARAKTER TERAKHIR
        # ----------------------------------------------------

        if i + 1 == len(text):

            # Karena tidak memiliki pasangan,
            # tambahkan filler.
            pairs.append(a + filler)

            # Selesai karena sudah mencapai karakter terakhir
            i += 1

        # ----------------------------------------------------
        # JIKA DUA KARAKTER SAMA
        # ----------------------------------------------------

        elif text[i] == text[i + 1]:

            # Jangan mengambil karakter kedua.
            #
            # Contoh:
            # HELLO
            #
            # Ketika menemukan LL:
            #
            # LX
            #
            # L kedua akan diproses lagi pada iterasi berikutnya.
            pairs.append(a + filler)

            # Hanya maju satu karakter
            i += 1

        # ----------------------------------------------------
        # JIKA DUA KARAKTER BERBEDA
        # ----------------------------------------------------

        else:

            # Ambil karakter berikutnya sebagai pasangan
            b = text[i + 1]

            # Simpan pasangan
            pairs.append(a + b)

            # Maju dua karakter
            i += 2

    # Kembalikan semua pasangan
    return pairs


# ============================================================
# FUNGSI ENCRYPT
# ============================================================

def encrypt(text, matrix, filler):

    # Buat pasangan plaintext menggunakan aturan Playfair
    pairs = buat_pairs(text, filler)

    # Variabel untuk menyimpan ciphertext
    hasil = ""

    # Proses setiap pasangan
    for pair in pairs:

        # Ambil karakter pertama dan kedua
        a = pair[0]
        b = pair[1]

        # Encrypt pasangan tersebut
        hasil += playfair(a, b, matrix, True)

    # Kembalikan ciphertext
    return hasil


# ============================================================
# FUNGSI DECRYPT
# ============================================================

def decrypt(text, matrix):

    # Variabel untuk menyimpan plaintext
    hasil = ""

    # Ciphertext dibaca dua karakter sekaligus
    for i in range(0, len(text), 2):

        # Decrypt pasangan
        hasil += playfair(
            text[i],
            text[i + 1],
            matrix,
            False
        )

    return hasil


# ============================================================
# PROGRAM UTAMA
# ============================================================

# ============================================================
# 1. INPUT BASE CHARACTER
# ============================================================

# User menentukan sendiri karakter yang digunakan.
#
# Bisa berupa huruf, angka, simbol, atau kombinasi.
base = input("Masukkan base karakter: ")


# ============================================================
# 2. VALIDASI BASE
# ============================================================

# Base tidak boleh memiliki karakter yang sama.
while len(set(base)) != len(base):

    print("Base tidak boleh memiliki karakter yang sama.")

    base = input("Masukkan base karakter: ")


# ============================================================
# 3. MENGHITUNG JUMLAH KARAKTER
# ============================================================

jumlah = len(base)


# ============================================================
# 4. MENENTUKAN UKURAN MATRIX
# ============================================================

# Cari ukuran matrix n x n berdasarkan jumlah karakter.
#
# Contoh:
# 29 karakter
# √29 = 5.38
# int() = 5
#
# Matrix = 5 x 5
n = int(jumlah ** 0.5)


# ============================================================
# 5. MENGHITUNG JUMLAH EXCEPTION
# ============================================================

# Contoh:
#
# Base = 29 karakter
# Matrix = 5 x 5 = 25 karakter
#
# Exception = 29 - 25 = 4 karakter
exception_jumlah = jumlah - (n * n)

print(f"\nJumlah karakter : {jumlah}")
print(f"Matrix          : {n} x {n}")
print(f"Exception       : {exception_jumlah} karakter")


# ============================================================
# 6. INPUT EXCEPTION
# ============================================================

exception = input(
    f"Masukkan {exception_jumlah} karakter exception: "
)


# ============================================================
# 7. VALIDASI EXCEPTION
# ============================================================

while (
    len(exception) != exception_jumlah
    or not set(exception).issubset(set(base))
    or len(set(exception)) != len(exception)
):

    print(
        "Exception tidak valid!"
        "\n- Jumlah karakter harus sesuai."
        "\n- Harus berasal dari base."
        "\n- Tidak boleh ada karakter yang sama."
    )

    exception = input(
        f"Masukkan {exception_jumlah} karakter exception: "
    )


# ============================================================
# 8. MENGHAPUS EXCEPTION DARI BASE
# ============================================================

# Karakter exception tidak boleh digunakan lagi
# dalam key, filler, plaintext, maupun matrix.
chars = "".join(
    c for c in base
    if c not in exception
)


# ============================================================
# 9. INPUT KEY
# ============================================================

while True:

    key = input("Masukkan key: ")

    # Key harus berasal dari chars.
    #
    # Karena exception sudah dihapus dari chars,
    # maka karakter exception otomatis ditolak.
    #
    # Validasi ini juga CASE-SENSITIVE.
    if key and all(c in chars for c in key):
        break

    print(
        "Key tidak valid!"
        "\n- Karakter harus berasal dari base."
        "\n- Karakter exception tidak boleh digunakan."
        "\n- Huruf besar dan kecil dianggap berbeda."
    )


# ============================================================
# 10. MEMBUAT URUTAN MATRIX BERDASARKAN KEY
# ============================================================

# Key diletakkan terlebih dahulu.
# Kemudian karakter chars yang belum digunakan ditambahkan.
urutan = ""

for c in key + chars:

    # Hindari karakter duplikat
    if c in chars and c not in urutan:
        urutan += c


# ============================================================
# 11. MEMBUAT MATRIX
# ============================================================

matrix = [
    urutan[i:i + n]
    for i in range(0, len(urutan), n)
]


# ============================================================
# 12. MENAMPILKAN MATRIX
# ============================================================

print("\nMatrix:")

for row in matrix:
    print(" ".join(row))


# ============================================================
# 13. INPUT FILLER
# ============================================================

while True:

    filler = input("\nMasukkan filler: ")

    # Filler harus satu karakter
    # dan harus ada di dalam matrix.
    if len(filler) == 1 and filler in chars:
        break

    print(
        "Filler tidak valid!"
        "\nFiller harus satu karakter "
        "dan tidak boleh merupakan exception."
    )


# ============================================================
# 14. MENU
# ============================================================

while True:

    print("\n1. Encrypt")
    print("2. Decrypt")
    print("3. Keluar")

    pilihan = input("Pilih: ")


    # ========================================================
    # ENCRYPT
    # ========================================================

    if pilihan == "1":

        # User memasukkan plaintext
        text = input("Plaintext: ")

        # Pastikan semua karakter plaintext
        # ada di dalam matrix.
        #
        # Spasi diperbolehkan dan akan dihapus
        # oleh fungsi buat_pairs().
        if all(c in chars or c == " " for c in text):

            # ------------------------------------------------
            # BUAT LETTER PAIRS
            # ------------------------------------------------

            # Buat pasangan plaintext berdasarkan
            # aturan Playfair.
            pairs = buat_pairs(text, filler)

            # Tampilkan pasangan dengan spasi.
            #
            # Contoh:
            # HELLO
            #
            # menjadi:
            # HE LX LO
            print(
                "Letter Pairs:",
                " ".join(pairs)
            )

            # ------------------------------------------------
            # ENCRYPT
            # ------------------------------------------------

            # Encrypt menggunakan pasangan yang sama
            # dengan yang ditampilkan di atas.
            ciphertext = encrypt(
                text,
                matrix,
                filler
            )

            print(
                "Ciphertext:",
                ciphertext
            )

        else:

            print(
                "Plaintext tidak valid!"
                "\nTerdapat karakter yang tidak ada "
                "di dalam matrix atau merupakan exception."
            )


    # ========================================================
    # DECRYPT
    # ========================================================

    elif pilihan == "2":

        # User memasukkan ciphertext
        text = input("Ciphertext: ")

        # Ciphertext harus genap karena
        # Playfair menggunakan pasangan karakter.
        if len(text) % 2 == 0:

            # Pastikan semua karakter ada di matrix.
            if all(c in chars for c in text):

                print(
                    "Plaintext:",
                    decrypt(text, matrix)
                )

            else:

                print(
                    "Ciphertext tidak valid!"
                    "\nTerdapat karakter yang tidak ada "
                    "di dalam matrix atau merupakan exception."
                )

        else:

            print(
                "Ciphertext harus memiliki "
                "jumlah karakter genap."
            )


    # ========================================================
    # KELUAR
    # ========================================================

    elif pilihan == "3":

        print("Program selesai.")
        break


    # ========================================================
    # PILIHAN MENU TIDAK VALID
    # ========================================================

    else:

        print("Pilihan tidak valid.")