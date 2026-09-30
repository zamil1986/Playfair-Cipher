# ============================================================
# PLAYFAIR CIPHER
# ============================================================
#
# Program ini merupakan implementasi sederhana Playfair Cipher.
#
# Hal yang dibuat fleksibel:
# 1. User menentukan sendiri karakter BASE.
#    Contoh:
#       ABCDEFGHIJKLMNOPQRSTUVWXYZ
#       ABCDEFGHIJKLMNOPQRSTUVWXYZ012
#       ABC123!@#$%
#
# 2. Ukuran matrix ditentukan otomatis berdasarkan jumlah
#    karakter BASE.
#
# 3. User menentukan sendiri karakter EXCEPTION.
#
# 4. Karakter EXCEPTION akan dikeluarkan dari matrix dan
#    tidak boleh digunakan lagi pada KEY, FILLER, PLAINTEXT,
#    maupun CIPHERTEXT.
#
# 5. User menentukan sendiri KEY.
#
# 6. User menentukan sendiri FILLER.
#
# 7. Letter pairs plaintext ditampilkan sebelum encryption.
#
# ============================================================

# ============================================================
# FUNCTION 1: posisi()
# ============================================================
#
# Tujuan:
# Mencari posisi/koordinat sebuah karakter di dalam matrix.
#
# Contoh matrix:
#
# M O N A R
# C H Y B D
# E F G I K
# L P S T U
# V W X Z 0
#
# Jika karakter yang dicari adalah H:
#
# H berada di:
# baris = 1
# kolom = 1
#
# Ingat bahwa index Python dimulai dari 0.
# ============================================================

def posisi(matrix, char):

    # enumerate() digunakan agar kita mendapatkan:
    # i   = nomor/index baris
    # row = isi baris
    #
    # Contoh:
    # i = 0 → M O N A R
    # i = 1 → C H Y B D
    # i = 2 → E F G I K
    for i, row in enumerate(matrix):

        # Mengecek apakah karakter yang dicari berada
        # di dalam baris tersebut.
        #
        # Contoh:
        # char = H
        # row  = C H Y B D
        #
        # H in row → True
        if char in row:

            # Jika ditemukan, kembalikan:
            #
            # i              → posisi baris
            # row.index(char) → posisi kolom
            #
            # Contoh:
            # H → (1, 1)
            return i, row.index(char)


# ============================================================
# FUNCTION 2: playfair()
# ============================================================
#
# Function ini merupakan inti dari algoritma Playfair Cipher.
#
# Function menerima dua karakter sekaligus karena Playfair
# selalu memproses plaintext dalam bentuk pasangan karakter.
#
# Contoh:
#
# HE
# ↑↑
# a b
#
# Parameter:
#
# a       = karakter pertama
# b       = karakter kedua
# matrix  = matrix Playfair
# encrypt = True  → encryption
#           False → decryption
# ============================================================

def playfair(a, b, matrix, encrypt=True):

    # Cari koordinat karakter pertama.
    #
    # Contoh:
    # H → (1, 1)
    r1, c1 = posisi(matrix, a)

    # Cari koordinat karakter kedua.
    #
    # Contoh:
    # E → (2, 0)
    r2, c2 = posisi(matrix, b)

    # len(matrix) digunakan untuk mengetahui ukuran matrix.
    #
    # Jika matrix:
    # 5 × 5
    #
    # maka:
    # n = 5
    n = len(matrix)

    # Menentukan arah pergeseran.
    #
    # Encryption:
    #   maju → +1
    #
    # Decryption:
    #   mundur → -1
    #
    # Conditional expression:
    # 1 if encrypt else -1
    arah = 1 if encrypt else -1


    # ========================================================
    # RULE 1: KEDUA KARAKTER BERADA DI BARIS YANG SAMA
    # ========================================================
    #
    # Contoh:
    #
    # M O N A R
    #
    # Misalnya pasangan O A.
    #
    # Keduanya berada pada baris yang sama.
    #
    # Encryption:
    # geser ke kanan.
    #
    # Decryption:
    # geser ke kiri.
    # ========================================================

    if r1 == r2:

        # c1 + arah digunakan untuk menggeser kolom
        # karakter pertama.
        #
        # c2 + arah digunakan untuk menggeser kolom
        # karakter kedua.
        #
        # % n digunakan agar jika sudah mencapai ujung
        # matrix, posisi kembali ke awal.
        #
        # Contoh:
        # index terakhir = 4
        #
        # 4 + 1 = 5
        #
        # 5 % 5 = 0
        #
        # Jadi terjadi wrap-around.
        return matrix[r1][(c1 + arah) % n] + \
               matrix[r2][(c2 + arah) % n]


    # ========================================================
    # RULE 2: KEDUA KARAKTER BERADA DI KOLOM YANG SAMA
    # ========================================================
    #
    # Jika dua karakter berada di kolom yang sama:
    #
    # Encryption:
    # geser ke bawah.
    #
    # Decryption:
    # geser ke atas.
    # ========================================================

    if c1 == c2:

        # Sekarang yang digeser adalah BARIS.
        #
        # r1 + arah → posisi karakter pertama
        # r2 + arah → posisi karakter kedua
        #
        # % n kembali digunakan untuk wrap-around.
        return matrix[(r1 + arah) % n][c1] + \
               matrix[(r2 + arah) % n][c2]


    # ========================================================
    # RULE 3: MEMBENTUK RECTANGLE
    # ========================================================
    #
    # Jika:
    #
    # r1 != r2
    # c1 != c2
    #
    # maka kedua karakter membentuk persegi panjang.
    #
    # Contoh:
    #
    # C H Y B D
    # E F G I K
    #
    # H berada di:
    # (1, 1)
    #
    # E berada di:
    # (2, 0)
    #
    # Maka:
    #
    # H mengambil kolom milik E
    # E mengambil kolom milik H
    #
    # H → C
    # E → F
    #
    # HE → CF
    # ========================================================

    return matrix[r1][c2] + matrix[r2][c1]


# ============================================================
# FUNCTION 3: buat_pairs()
# ============================================================
#
# Function ini digunakan untuk mengubah plaintext menjadi
# pasangan karakter sesuai RULE PLAYFAIR.
#
# Contoh sederhana:
#
# HELLO
#
# Tidak boleh langsung menjadi:
#
# HE LL O
#
# Karena terdapat LL.
#
# Dalam Playfair, dua karakter yang sama tidak boleh berada
# dalam satu pasangan.
#
# Jika filler = X:
#
# HELLO
#   ↓
# HE LX LO
#
# Perhatikan bahwa L kedua tetap diproses kembali.
# ============================================================

def buat_pairs(text, filler):

    # Spasi tidak digunakan dalam proses pasangan Playfair.
    #
    # Contoh:
    # HELLO WORLD
    #
    # menjadi:
    # HELLOWORLD
    text = text.replace(" ", "")

    # List kosong untuk menyimpan pasangan.
    #
    # Contoh akhir:
    # ["HE", "LX", "LO"]
    pairs = []

    # i merupakan index untuk membaca plaintext.
    #
    # Python dimulai dari index 0.
    i = 0


    # Selama index masih berada di dalam plaintext,
    # proses pasangan terus dilakukan.
    while i < len(text):

        # Ambil karakter pertama.
        #
        # Misalnya:
        # i = 0
        # text = HELLO
        #
        # a = H
        a = text[i]


        # ====================================================
        # KONDISI 1: KARAKTER TERAKHIR
        # ====================================================
        #
        # Jika karakter terakhir tidak mempunyai pasangan,
        # maka tambahkan filler.
        #
        # Contoh:
        #
        # HELLO
        #
        # O adalah karakter terakhir.
        #
        # Maka:
        # O → OX
        # ====================================================

        if i + 1 == len(text):

            # Gabungkan karakter terakhir dengan filler.
            pairs.append(a + filler)

            # Karena karakter terakhir sudah diproses,
            # index dinaikkan satu.
            i += 1


        # ====================================================
        # KONDISI 2: DUA KARAKTER SAMA
        # ====================================================
        #
        # Contoh:
        #
        # HELLO
        #   ↑↑
        #   LL
        #
        # LL tidak boleh menjadi satu pasangan.
        #
        # Maka jika filler = X:
        #
        # LL → LX
        #
        # Tetapi L kedua BELUM dianggap selesai.
        # ====================================================

        elif text[i] == text[i + 1]:

            # Pasangkan karakter pertama dengan filler.
            #
            # L + X → LX
            pairs.append(a + filler)

            # Hanya maju SATU karakter.
            #
            # Ini sangat penting.
            #
            # Karena karakter kedua dari pasangan LL
            # masih harus diproses pada iterasi berikutnya.
            i += 1


        # ====================================================
        # KONDISI 3: DUA KARAKTER BERBEDA
        # ====================================================
        #
        # Jika karakter sekarang dan karakter berikutnya
        # berbeda, keduanya boleh menjadi satu pasangan.
        #
        # Contoh:
        #
        # H E
        #
        # H != E
        #
        # Maka:
        # HE
        # ====================================================

        else:

            # Ambil karakter kedua.
            b = text[i + 1]

            # Gabungkan karakter pertama dan kedua.
            #
            # H + E → HE
            pairs.append(a + b)

            # Karena dua karakter sudah digunakan,
            # index maju dua.
            i += 2


    # Setelah seluruh plaintext selesai diproses,
    # kembalikan semua pasangan.
    #
    # Contoh:
    # ["HE", "LX", "LO"]
    return pairs


# ============================================================
# FUNCTION 4: encrypt()
# ============================================================
#
# Function ini mengubah plaintext menjadi ciphertext.
#
# Flow:
#
# plaintext
#     ↓
# buat_pairs()
#     ↓
# pasangan karakter
#     ↓
# playfair()
#     ↓
# ciphertext
# ============================================================

def encrypt(text, matrix, filler):

    # Pertama, plaintext diubah menjadi pasangan.
    #
    # Contoh:
    # HELLO
    #
    # menjadi:
    # HE LX LO
    pairs = buat_pairs(text, filler)

    # String kosong untuk menampung hasil encryption.
    hasil = ""

    # Proses setiap pasangan satu per satu.
    #
    # Misalnya:
    # HE
    # LX
    # LO
    for pair in pairs:

        # Ambil karakter pertama dari pasangan.
        #
        # HE → H
        a = pair[0]

        # Ambil karakter kedua dari pasangan.
        #
        # HE → E
        b = pair[1]

        # Kirim pasangan ke function playfair().
        #
        # True berarti kita sedang melakukan encryption.
        #
        # Hasil encryption kemudian ditambahkan ke
        # string ciphertext.
        hasil += playfair(a, b, matrix, True)

    # Kembalikan ciphertext.
    return hasil


# ============================================================
# FUNCTION 5: decrypt()
# ============================================================
#
# Function ini digunakan untuk mengembalikan ciphertext
# menjadi plaintext.
#
# Karena ciphertext Playfair sudah berbentuk pasangan,
# kita tidak perlu membuat pairs lagi.
# ============================================================

def decrypt(text, matrix):

    # Tempat menyimpan hasil plaintext.
    hasil = ""

    # Membaca ciphertext dua karakter sekaligus.
    #
    # Contoh:
    #
    # ABCDEF
    #
    # index:
    # 0 1 → AB
    # 2 3 → CD
    # 4 5 → EF
    #
    # step = 2 berarti index bertambah dua.
    for i in range(0, len(text), 2):

        # Kirim pasangan ke function playfair().
        #
        # False berarti DECRYPTION.
        #
        # text[i]     → karakter pertama
        # text[i + 1] → karakter kedua
        hasil += playfair(
            text[i],
            text[i + 1],
            matrix,
            False
        )

    # Kembalikan plaintext.
    return hasil


# ============================================================
# PROGRAM UTAMA
# ============================================================
#
# Mulai dari sini program mulai berinteraksi dengan user.
# ============================================================


# ============================================================
# STEP 1 — INPUT BASE CHARACTER
# ============================================================
#
# User bebas menentukan alfabet sendiri.
#
# Contoh:
#
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
#
# atau:
#
# ABCDEFGHIJKLMNOPQRSTUVWXYZ012
#
# atau:
#
# ABC123!@#
#
# Tidak ada ketentuan bahwa base harus A-Z.
# ============================================================

base = input("Masukkan base karakter: ")


# ============================================================
# STEP 2 — VALIDASI BASE
# ============================================================
#
# Base tidak boleh memiliki karakter duplikat.
#
# Contoh:
#
# ABCDEA
#
# tidak valid karena A muncul dua kali.
#
# set() menghilangkan duplikat.
#
# len(set(base))
# dibandingkan dengan:
# len(base)
#
# Jika berbeda → terdapat duplikat.
# ============================================================

while len(set(base)) != len(base):

    print("Base tidak boleh memiliki karakter yang sama.")

    # User diminta menginput ulang base.
    base = input("Masukkan base karakter: ")


# ============================================================
# STEP 3 — HITUNG JUMLAH KARAKTER BASE
# ============================================================
#
# Contoh:
#
# ABCDEFGHIJKLMNOPQRSTUVWXYZ012
#
# jumlah = 29
# ============================================================

jumlah = len(base)


# ============================================================
# STEP 4 — MENENTUKAN UKURAN MATRIX
# ============================================================
#
# Playfair membutuhkan matrix berbentuk persegi.
#
# Artinya:
#
# n × n
#
# Untuk mencari n:
#
# √jumlah karakter
#
# Contoh:
#
# 29 karakter
#
# √29 ≈ 5.38
#
# int(5.38) = 5
#
# Maka:
#
# matrix = 5 × 5 = 25 karakter
# ============================================================

n = int(jumlah ** 0.5)


# ============================================================
# STEP 5 — HITUNG JUMLAH EXCEPTION
# ============================================================
#
# Jumlah karakter matrix yang bisa ditampung adalah:
#
# n × n
#
# Jika base mempunyai 29 karakter:
#
# 5 × 5 = 25
#
# Maka 4 karakter harus dikeluarkan:
#
# 29 - 25 = 4
#
# Inilah jumlah exception yang wajib diberikan user.
# ============================================================

exception_jumlah = jumlah - (n * n)


# Tampilkan informasi kepada user.
print(f"\nJumlah karakter : {jumlah}")
print(f"Matrix          : {n} x {n}")
print(f"Exception       : {exception_jumlah} karakter")


# ============================================================
# STEP 6 — INPUT EXCEPTION
# ============================================================
#
# User harus memasukkan jumlah exception sesuai hasil
# perhitungan sebelumnya.
#
# Contoh:
#
# Base = 29
#
# Exception = 4
#
# User harus memasukkan tepat 4 karakter.
# ============================================================

exception = input(
    f"Masukkan {exception_jumlah} karakter exception: "
)


# ============================================================
# STEP 7 — VALIDASI EXCEPTION
# ============================================================
#
# Ada tiga hal yang diperiksa:
#
# 1. Jumlah exception harus benar.
#
# 2. Semua exception harus ada di BASE.
#
# 3. Exception tidak boleh duplikat.
#
# ============================================================

while (
    # --------------------------------------------------------
    # VALIDASI 1
    # --------------------------------------------------------
    # Jumlah exception harus sesuai.
    len(exception) != exception_jumlah

    or

    # --------------------------------------------------------
    # VALIDASI 2
    # --------------------------------------------------------
    # Semua exception harus berasal dari BASE.
    #
    # Contoh:
    #
    # BASE      = ABCDEF
    # EXCEPTION = ABZ
    #
    # Z tidak ada di BASE → ditolak.
    not set(exception).issubset(set(base))

    or

    # --------------------------------------------------------
    # VALIDASI 3
    # --------------------------------------------------------
    # Exception tidak boleh memiliki karakter yang sama.
    #
    # Contoh:
    #
    # AABC
    #
    # A muncul dua kali → ditolak.
    len(set(exception)) != len(exception)
):

    print(
        "Exception tidak valid!"
        "\n- Jumlah karakter harus sesuai."
        "\n- Harus berasal dari base."
        "\n- Tidak boleh ada karakter yang sama."
    )

    # User diminta menginput ulang exception.
    exception = input(
        f"Masukkan {exception_jumlah} karakter exception: "
    )


# ============================================================
# STEP 8 — MEMBUAT CHARS
# ============================================================
#
# Sekarang exception dikeluarkan dari BASE.
#
# Contoh:
#
# BASE:
# ABCDEFG
#
# EXCEPTION:
# BD
#
# Maka:
#
# CHARS:
# ACEFG
#
# chars inilah yang nantinya digunakan sebagai karakter
# yang valid untuk matrix.
# ============================================================

chars = "".join(
    c for c in base
    if c not in exception
)


# ============================================================
# STEP 9 — INPUT KEY
# ============================================================
#
# Key akan ditempatkan di bagian awal matrix.
#
# Contoh:
#
# Key = MONARCHY
#
# Maka matrix akan dimulai dari:
#
# M O N A R C H Y ...
#
# ============================================================

while True:

    key = input("Masukkan key: ")


    # ========================================================
    # VALIDASI KEY
    # ========================================================
    #
    # Key harus:
    #
    # 1. Tidak kosong.
    #
    # 2. Semua karakter ada di CHARS.
    #
    # Mengapa menggunakan CHARS dan bukan BASE?
    #
    # Karena EXCEPTION sudah dihapus dari CHARS.
    #
    # Jadi jika user mencoba:
    #
    # Base:
    # ABCDEFGHIJ
    #
    # Exception:
    # J
    #
    # Key:
    # ABCJ
    #
    # J akan otomatis ditolak.
    #
    # Validasi juga CASE-SENSITIVE.
    #
    # Artinya:
    #
    # A != a
    #
    # jika hanya A yang terdapat dalam BASE,
    # maka a dianggap invalid.
    # ========================================================

    if key and all(c in chars for c in key):

        # Jika semua valid, keluar dari loop.
        break


    # Jika tidak valid, tampilkan alasan.
    print(
        "Key tidak valid!"
        "\n- Karakter harus berasal dari base."
        "\n- Karakter exception tidak boleh digunakan."
        "\n- Huruf besar dan kecil dianggap berbeda."
    )


# ============================================================
# STEP 10 — MEMBUAT URUTAN MATRIX
# ============================================================
#
# Matrix harus dimulai dari KEY.
#
# Setelah semua karakter KEY dimasukkan,
# karakter CHARS yang belum digunakan akan ditambahkan.
#
# Contoh:
#
# KEY:
# MONARCHY
#
# CHARS:
# ABCDEFGHIKLMNOPQRSTUVWXYZ
#
# Maka urutan dimulai:
#
# MONARCHYBDEFGIKLPQSTUVWXZ
#
# Karakter yang sudah terdapat dalam KEY tidak dimasukkan
# kembali.
# ============================================================

urutan = ""


# Gabungkan KEY dan CHARS sehingga KEY diproses terlebih dahulu.
for c in key + chars:

    # Karakter harus berada dalam CHARS.
    #
    # Dan:
    #
    # c not in urutan
    #
    # digunakan agar tidak terjadi duplikasi.
    if c in chars and c not in urutan:

        # Masukkan karakter ke urutan matrix.
        urutan += c


# ============================================================
# STEP 11 — MEMBENTUK MATRIX
# ============================================================
#
# Sekarang string "urutan" dipotong setiap n karakter.
#
# Misalnya:
#
# n = 5
#
# urutan:
#
# MONARCHYBDEFGIKLPQSTUVWXZ
#
# akan dipotong menjadi:
#
# MONAR
# CHYBD
# EFGIK
# LPQST
# UVWXZ
#
# Inilah matrix Playfair.
# ============================================================

matrix = [
    urutan[i:i + n]
    for i in range(0, len(urutan), n)
]


# ============================================================
# STEP 12 — MENAMPILKAN MATRIX
# ============================================================
#
# Tampilkan matrix agar user dapat melihat hasil akhir
# penyusunan KEY + CHARS.
# ============================================================

print("\nMatrix:")


# Ambil setiap baris matrix.
for row in matrix:

    # " ".join(row) memberikan spasi di antara setiap
    # karakter agar matrix mudah dibaca.
    #
    # Contoh:
    #
    # "MONAR"
    #
    # menjadi:
    #
    # M O N A R
    print(" ".join(row))


# ============================================================
# STEP 13 — INPUT FILLER
# ============================================================
#
# Filler digunakan ketika:
#
# 1. Dua karakter yang berurutan sama.
#
#    Contoh:
#    LL
#
#    menjadi:
#    LX
#
# 2. Plaintext memiliki jumlah karakter ganjil.
#
#    Contoh:
#    ABC
#
#    menjadi:
#    AB CX
#
# Filler harus:
#
# - tepat satu karakter
# - berasal dari CHARS
#
# Dengan menggunakan CHARS, karakter exception otomatis
# tidak dapat digunakan sebagai filler.
# ============================================================

while True:

    filler = input("\nMasukkan filler: ")


    # Validasi filler:
    #
    # len(filler) == 1
    # → harus tepat satu karakter.
    #
    # filler in chars
    # → harus terdapat dalam karakter yang valid.
    if len(filler) == 1 and filler in chars:

        # Filler valid.
        break


    print(
        "Filler tidak valid!"
        "\nFiller harus satu karakter "
        "dan tidak boleh merupakan exception."
    )


# ============================================================
# STEP 14 — MENU UTAMA
# ============================================================
#
# Setelah semua konfigurasi selesai:
#
# BASE
# EXCEPTION
# CHARS
# KEY
# MATRIX
# FILLER
#
# program siap digunakan.
# ============================================================

while True:

    print("\n1. Encrypt")
    print("2. Decrypt")
    print("3. Keluar")

    # Baca pilihan user.
    pilihan = input("Pilih: ")


    # ========================================================
    # PILIHAN 1 → ENCRYPT
    # ========================================================

    if pilihan == "1":

        # User memasukkan plaintext.
        text = input("Plaintext: ")


        # ====================================================
        # VALIDASI PLAINTEXT
        # ====================================================
        #
        # Setiap karakter harus:
        #
        # 1. Ada di CHARS
        #
        # ATAU:
        #
        # 2. Berupa spasi.
        #
        # Mengapa spasi diperbolehkan?
        #
        # Karena spasi nantinya akan dihapus oleh
        # buat_pairs().
        #
        # Exception tetap ditolak karena exception
        # tidak terdapat dalam CHARS.
        # ====================================================

        if all(c in chars or c == " " for c in text):


            # =================================================
            # MEMBUAT LETTER PAIRS
            # =================================================
            #
            # Plaintext diproses berdasarkan aturan Playfair.
            #
            # Contoh:
            #
            # HELLO
            #
            # menjadi:
            #
            # HE LX LO
            #
            # Bukan:
            #
            # HE LL O
            #
            # karena LL merupakan pasangan karakter yang sama.
            # =================================================

            pairs = buat_pairs(text, filler)


            # =================================================
            # MENAMPILKAN LETTER PAIRS
            # =================================================
            #
            # pairs:
            #
            # ["HE", "LX", "LO"]
            #
            # " ".join(pairs)
            #
            # menghasilkan:
            #
            # HE LX LO
            #
            # Jadi user dapat melihat bagaimana plaintext
            # dipecah sebelum proses encryption.
            # =================================================

            print(
                "Letter Pairs:",
                " ".join(pairs)
            )


            # =================================================
            # ENCRYPT PLAINTEXT
            # =================================================
            #
            # Setelah pairs ditampilkan, plaintext diteruskan
            # ke function encrypt().
            #
            # encrypt() kemudian:
            #
            # plaintext
            #     ↓
            # buat_pairs()
            #     ↓
            # pasangan
            #     ↓
            # playfair()
            #     ↓
            # ciphertext
            # =================================================

            ciphertext = encrypt(
                text,
                matrix,
                filler
            )


            # Tampilkan hasil akhir encryption.
            print(
                "Ciphertext:",
                ciphertext
            )


        # ====================================================
        # PLAINTEXT TIDAK VALID
        # ====================================================

        else:

            print(
                "Plaintext tidak valid!"
                "\nTerdapat karakter yang tidak ada "
                "di dalam matrix atau merupakan exception."
            )


    # ========================================================
    # PILIHAN 2 → DECRYPT
    # ========================================================

    elif pilihan == "2":

        # User memasukkan ciphertext.
        text = input("Ciphertext: ")


        # ====================================================
        # VALIDASI JUMLAH KARAKTER
        # ====================================================
        #
        # Playfair bekerja menggunakan pasangan.
        #
        # Jadi ciphertext harus memiliki jumlah karakter GENAP.
        #
        # Contoh valid:
        #
        # ABCDEF
        #
        # 6 karakter.
        #
        # Contoh invalid:
        #
        # ABCDE
        #
        # 5 karakter.
        # ====================================================

        if len(text) % 2 == 0:


            # =================================================
            # VALIDASI KARAKTER CIPHERTEXT
            # =================================================
            #
            # Semua karakter ciphertext harus berasal dari
            # CHARS.
            #
            # Dengan demikian:
            #
            # karakter random → ditolak
            # exception       → ditolak
            # =================================================

            if all(c in chars for c in text):


                # =================================================
                # DECRYPT
                # =================================================
                #
                # Ciphertext dikirim ke function decrypt().
                #
                # decrypt() membaca dua karakter sekaligus:
                #
                # AB CD EF
                #
                # Kemudian setiap pasangan diproses menggunakan
                # Playfair dengan mode encrypt=False.
                # =================================================

                print(
                    "Plaintext:",
                    decrypt(text, matrix)
                )


            # =================================================
            # CIPHERTEXT MEMILIKI KARAKTER INVALID
            # =================================================

            else:

                print(
                    "Ciphertext tidak valid!"
                    "\nTerdapat karakter yang tidak ada "
                    "di dalam matrix atau merupakan exception."
                )


        # ====================================================
        # JUMLAH CIPHERTEXT GANJIL
        # ====================================================

        else:

            print(
                "Ciphertext harus memiliki "
                "jumlah karakter genap."
            )


    # ========================================================
    # PILIHAN 3 → KELUAR
    # ========================================================

    elif pilihan == "3":

        # Informasi bahwa program akan dihentikan.
        print("Program selesai.")

        # break menghentikan while True pada menu.
        break


    # ========================================================
    # PILIHAN TIDAK VALID
    # ========================================================

    else:

        # Jika user memasukkan selain:
        #
        # 1
        # 2
        # 3
        #
        # maka tampilkan pesan error dan kembali ke menu.
        print("Pilihan tidak valid.")