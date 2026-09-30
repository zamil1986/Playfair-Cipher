# Playfair Cipher — Python

Implementasi **Playfair Cipher menggunakan Python** dengan alfabet yang dapat ditentukan secara fleksibel oleh user.

Program ini tidak terbatas pada alfabet `A-Z`. User dapat menentukan sendiri karakter yang ingin digunakan, termasuk **huruf, angka, simbol, maupun kombinasi semuanya**.

## ✨ Features

* Custom base character.
* Mendukung huruf, angka, simbol, dan kombinasi karakter.
* Ukuran matrix ditentukan secara otomatis berdasarkan jumlah karakter base.
* Custom exception character.
* Exception otomatis disesuaikan dengan kapasitas matrix `n × n`.
* Validasi karakter duplikat pada base.
* Validasi exception.
* Exception tidak dapat digunakan kembali pada:

  * Key
  * Filler
  * Plaintext
  * Ciphertext
* Validasi bersifat **case-sensitive**.
* Custom key.
* Custom filler.
* Menampilkan **Letter Pairs** sebelum encryption.
* Penanganan duplicate letters sesuai aturan Playfair Cipher.
* Penanganan plaintext dengan jumlah karakter ganjil menggunakan filler.
* Mendukung encryption dan decryption.
* Source code tersedia dalam dua versi:

  * versi dengan komentar detail
  * versi dengan komentar minimal

---

# 📁 Project Structure

```text
Playfair-Cipher/
│
├── default.py
├── comment.py
└── README.md
```

## `default.py`

`default.py` merupakan **versi utama** dari program.

File ini memiliki komentar yang minimal sehingga source code lebih bersih dan mudah digunakan untuk menjalankan program.

File ini cocok digunakan jika tujuan utamanya adalah:

* menjalankan program,
* membaca implementasi secara ringkas,
* mempelajari struktur program tanpa terlalu banyak komentar.

---

## `comment.py`

`comment.py` merupakan versi **pembelajaran** dari program.

Logika programnya sama dengan `default.py`, tetapi setiap bagian diberikan komentar yang lebih detail untuk menjelaskan:

* fungsi setiap function,
* tujuan setiap variable,
* proses validasi,
* pembentukan matrix,
* pembentukan letter pairs,
* aturan Playfair Cipher,
* proses encryption,
* proses decryption,
* dan flow program secara keseluruhan.

File ini cocok digunakan untuk **mempelajari dan memahami source code**.

### Perbedaan kedua file

| File         | Tujuan           | Komentar |
| ------------ | ---------------- | -------- |
| `default.py` | Penggunaan utama | Minimal  |
| `comment.py` | Pembelajaran     | Detail   |

Kedua file menggunakan **algoritma dan fitur yang sama**. Perbedaannya hanya pada tingkat dokumentasi di dalam source code.

---

# ⚙️ Requirements

Program hanya membutuhkan:

* Python 3.x

Tidak ada external library yang diperlukan.

Program hanya menggunakan fitur bawaan Python seperti:

* `input()`
* `print()`
* `set()`
* `len()`
* `enumerate()`
* `range()`
* string operation
* list comprehension

---

# 🚀 Setup

## 1. Clone Repository

Clone repository ke komputer:

```bash
git clone https://github.com/zamil1986/Playfair-Cipher.git
```

Masuk ke directory project:

```bash
cd Playfair-Cipher
```

---

## 2. Cek Python

Pastikan Python sudah terinstall:

```bash
python3 --version
```

Contoh:

```text
Python 3.13.7
```

Versi Python 3.x dapat digunakan.

---

# ▶️ Running the Program

## Menggunakan `default.py`

Untuk menjalankan versi utama:

```bash
python3 default.py
```

atau jika sistem menggunakan command `python`:

```bash
python default.py
```

---

## Menggunakan `comment.py`

Untuk menjalankan versi dengan komentar detail:

```bash
python3 comment.py
```

atau:

```bash
python comment.py
```

Kedua file menghasilkan perilaku program yang sama.

---

# 🧩 Program Flow

Secara umum, program bekerja dengan alur:

```text
Base Character
      ↓
Validasi Base
      ↓
Hitung Ukuran Matrix
      ↓
Hitung Jumlah Exception
      ↓
Input Exception
      ↓
Validasi Exception
      ↓
Hapus Exception
      ↓
Chars
      ↓
Input Key
      ↓
Validasi Key
      ↓
Susun Key + Chars
      ↓
Buat Matrix
      ↓
Input Filler
      ↓
Menu
   ↙     ↘
Encrypt  Decrypt
```

---

# 🔤 1. Custom Base Character

User menentukan sendiri karakter yang ingin digunakan.

Contoh:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

atau:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ012
```

atau:

```text
ABC123!@#
```

Program tidak mengharuskan base berupa alfabet A-Z.

Namun, setiap karakter dalam base harus **unik**.

Contoh valid:

```text
ABC123!@#
```

Contoh tidak valid:

```text
AABC123
```

karena `A` muncul lebih dari satu kali.

---

# 🔢 2. Automatic Matrix Size

Ukuran matrix ditentukan berdasarkan jumlah karakter base.

Program mencari nilai:

```text
n = floor(√jumlah karakter)
```

Kemudian matrix dibuat menjadi:

```text
n × n
```

Contoh:

```text
29 karakter
```

Maka:

```text
√29 ≈ 5.38
```

Program mengambil:

```text
n = 5
```

Sehingga:

```text
5 × 5 = 25
```

Karena base memiliki 29 karakter sedangkan matrix hanya dapat menampung 25 karakter, maka:

```text
29 - 25 = 4
```

Artinya user harus menentukan **4 exception**.

---

# 🚫 3. Exception

Exception adalah karakter dari base yang tidak akan dimasukkan ke dalam matrix.

Contoh:

```text
Base:
ABCDEFGHIJKLMNOPQRSTUVWXYZ012
```

Jumlah:

```text
29
```

Matrix:

```text
5 × 5
```

Maka diperlukan:

```text
4 exception
```

Misalnya:

```text
JQ12
```

Setelah exception dikeluarkan, karakter yang dapat digunakan menjadi:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ012
         ↓
       - JQ12
         ↓
characters yang tersisa
```

Karakter exception tidak dapat digunakan lagi dalam:

* Key
* Filler
* Plaintext
* Ciphertext

---

# 🔑 4. Key

Setelah exception ditentukan, user memasukkan key.

Contoh:

```text
MONARCHY
```

Key akan ditempatkan terlebih dahulu ketika matrix dibuat.

Karakter yang belum digunakan dari base kemudian ditambahkan setelah key.

Duplikasi karakter dalam key tidak akan dimasukkan dua kali ke matrix.

---

# 🔲 5. Matrix

Contoh hasil matrix:

```text
M O N A R
C H Y B D
E F G I K
L P S T U
V W X Z 0
```

Matrix inilah yang digunakan dalam proses encryption dan decryption.

---

# ✏️ 6. Filler

Filler digunakan ketika plaintext memiliki kondisi tertentu.

## Duplicate Character

Contoh plaintext:

```text
HELLO
```

Jika filler:

```text
X
```

maka:

```text
HE LL O
```

tidak dapat langsung digunakan karena `LL` merupakan karakter yang sama.

Program mengubahnya menjadi:

```text
HE LX LO
```

Perhatikan bahwa `L` kedua tetap diproses pada pasangan berikutnya.

---

## Odd Length Plaintext

Jika plaintext memiliki jumlah karakter ganjil:

```text
ABC
```

maka:

```text
AB CX
```

dengan filler `X`.

---

# 🔤 7. Letter Pairs

Sebelum proses encryption, program menampilkan pasangan karakter yang telah dibuat.

Contoh:

```text
Plaintext: HELLO
Letter Pairs: HE LX LO
```

Output ini membantu melihat bagaimana plaintext diproses sebelum masuk ke algoritma Playfair.

---

# 🔐 8. Encryption Rules

Playfair Cipher menggunakan tiga aturan utama.

## Same Row

Jika kedua karakter berada pada baris yang sama:

```text
→ geser ke kanan
```

Untuk decryption:

```text
→ geser ke kiri
```

---

## Same Column

Jika kedua karakter berada pada kolom yang sama:

```text
→ geser ke bawah
```

Untuk decryption:

```text
→ geser ke atas
```

---

## Rectangle

Jika kedua karakter tidak berada pada baris maupun kolom yang sama:

```text
→ bentuk rectangle
→ masing-masing karakter mengambil kolom karakter lainnya
```

---

# 🔓 9. Decryption

Ciphertext diproses dua karakter sekaligus.

Contoh:

```text
ABCDXY
```

akan dibaca sebagai:

```text
AB
CD
XY
```

Setiap pasangan kemudian diproses menggunakan aturan Playfair dalam mode decryption.

Ciphertext harus memiliki jumlah karakter **genap**.

---

# 🛡️ Input Validation

Program memiliki beberapa validasi.

### Base

* Tidak boleh memiliki karakter duplikat.

### Exception

* Jumlah harus sesuai.
* Harus berasal dari base.
* Tidak boleh duplikat.

### Key

* Tidak boleh kosong.
* Semua karakter harus berasal dari karakter yang tersedia.
* Exception tidak diperbolehkan.
* Case-sensitive.

### Filler

* Harus tepat satu karakter.
* Harus berasal dari karakter yang tersedia.
* Exception tidak diperbolehkan.

### Plaintext

* Karakter harus berasal dari matrix.
* Spasi diperbolehkan.
* Exception tidak diperbolehkan.

### Ciphertext

* Harus memiliki jumlah karakter genap.
* Semua karakter harus berasal dari matrix.
* Exception tidak diperbolehkan.

---

# 🧪 Example

Contoh penggunaan:

```text
Masukkan base karakter: ABCDEFGHIJKLMNOPQRSTUVWXYZ012

Jumlah karakter : 29
Matrix          : 5 x 5
Exception       : 4 karakter

Masukkan 4 karakter exception: JQ12
Masukkan key: MONARCHY

Matrix:
M O N A R
C H Y B D
E F G I K
L P S T U
V W X Z 0

Masukkan filler: X

1. Encrypt
2. Decrypt
3. Keluar

Pilih: 1

Plaintext: HELLO

Letter Pairs: HE LX LO

Ciphertext: ...
```

Hasil ciphertext bergantung pada matrix, key, exception, dan filler yang diberikan user.

---

# 📚 Educational Version

Jika tujuanmu adalah memahami bagaimana program bekerja, gunakan:

```bash
python3 comment.py
```

File ini memiliki komentar yang menjelaskan bagian-bagian seperti:

```text
Base
 ↓
Exception
 ↓
Chars
 ↓
Key
 ↓
Matrix
 ↓
Filler
 ↓
Letter Pairs
 ↓
Playfair Rules
 ↓
Encryption / Decryption
```

Jika tujuanmu hanya menjalankan atau membaca source code dengan lebih ringkas, gunakan:

```bash
python3 default.py
```

---

# 📌 Notes

Program ini dibuat sebagai implementasi pembelajaran **Playfair Cipher** menggunakan Python.

Playfair Cipher merupakan cipher klasik untuk pembelajaran konsep kriptografi dan **bukan algoritma enkripsi modern yang sesuai untuk melindungi data sensitif**.

Repository ini berfokus pada pemahaman:

* substitution/transformation berbasis pasangan karakter,
* matrix-based cipher,
* key scheduling sederhana,
* plaintext preprocessing,
* filler character,
* encryption/decryption flow,
* dan input validation menggunakan Python.
