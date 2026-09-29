"""Implementasi Playfair Cipher dengan matriks 3x3, 5x5, atau 6x6.

Mode yang tersedia:
* huruf A-Z (5x5), dengan satu huruf yang dikecualikan;
* angka 0-9 (3x3), dengan satu angka yang dikecualikan; dan
* angka 0-9 lalu huruf A-Z, atau huruf A-Z lalu angka 0-9 (6x6),
  tanpa pengecualian.

Program ini ditujukan untuk pembelajaran, bukan untuk melindungi data modern.
"""

from __future__ import annotations

import math
from operator import truediv
import string


class PlayfairCipher:
    """Enkripsi dan dekripsi teks dengan konfigurasi matriks Playfair."""

    _MODE_SYMBOLS = {
        "letters": string.ascii_uppercase,
        "digits": string.digits,
        "alphanumeric": string.digits + string.ascii_uppercase,
        "alphanumeric_letters_first": string.ascii_uppercase + string.digits,
    }
    _DEFAULT_EXCEPTION = {"letters": "J", "digits": "0"}

    def __init__(
        self,
        key: str,
        mode: str = "letters",
        exception: str | None = None,
    ) -> None:
        """Buat cipher dengan salah satu mode matriks yang tersedia.

        Mode ``letters`` dan ``digits`` membutuhkan satu simbol pengecualian.
        Bila tidak diberikan, masing-masing memakai J dan 0 agar pemakaian API
        lama ``PlayfairCipher(key)`` tetap menghasilkan matriks 5x5 klasik.
        Mode ``alphanumeric`` dan ``alphanumeric_letters_first`` selalu memakai
        36 simbol, sehingga pengecualian tidak diperbolehkan.
        """
        mode = mode.lower()
        if mode not in self._MODE_SYMBOLS:
            raise ValueError(
                "Mode harus: letters, digits, alphanumeric, atau "
                "alphanumeric_letters_first."
            )

        self.mode = mode
        available_symbols = self._MODE_SYMBOLS[mode]

        if mode.startswith("alphanumeric"):
            if exception is not None:
                raise ValueError(
                    "Mode huruf dan angka memakai matriks 6x6, "
                    "jadi tidak boleh ada simbol pengecualian."
                )
            self.exception = None
            self.symbols = available_symbols
        else:
            exception = self._DEFAULT_EXCEPTION[mode] if exception is None else exception
            exception = exception.upper() if mode == "letters" else exception
            if len(exception) != 1 or exception not in available_symbols:
                symbol_kind = "huruf A-Z" if mode == "letters" else "angka 0-9"
                raise ValueError(f"Pengecualian harus tepat satu {symbol_kind}.")
            self.exception = exception
            self.symbols = available_symbols.replace(exception, "")

        self.size = math.isqrt(len(self.symbols))
        if self.size * self.size != len(self.symbols):
            raise ValueError("Jumlah simbol harus membentuk matriks persegi.")

        self.matrix = self._build_matrix(key)
        self.positions = {
            symbol: (row, column)
            for row, row_values in enumerate(self.matrix)
            for column, symbol in enumerate(row_values)
        }

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalisasi 5x5 klasik; dipertahankan untuk kompatibilitas lama."""
        return "".join(
            character if character != "J" else "I"
            for character in text.upper()
            if character in string.ascii_uppercase
        )

    @staticmethod
    def _clean_text(text: str, allowed_symbols: str) -> str:
        """Ambil simbol yang diizinkan dan tolak alfanumerik di luar matriks."""
        cleaned: list[str] = []
        invalid: list[str] = []

        for raw_character in text:
            character = raw_character.upper()
            if len(character) == 1 and character in allowed_symbols:
                cleaned.append(character)
            elif raw_character.isalnum():
                invalid.append(raw_character)

        if invalid:
            invalid_symbols = ", ".join(sorted(set(invalid)))
            raise ValueError(
                f"Simbol tidak ada dalam matriks: {invalid_symbols}. "
                f"Gunakan hanya: {allowed_symbols}."
            )
        return "".join(cleaned)

    def normalize(self, text: str) -> str:
        """Normalisasi teks sesuai simbol yang dipakai matriks ini."""
        return self._clean_text(text, self.symbols)

    def _build_matrix(self, key: str) -> list[list[str]]:
        symbols: list[str] = []
        for character in self.normalize(key) + self.symbols:
            if character not in symbols:
                symbols.append(character)
        return [
            symbols[index : index + self.size]
            for index in range(0, len(self.symbols), self.size)
        ]

    def _filler_for(self, first: str) -> str:
        """Pilih penyisip yang tersedia dan berbeda dari simbol pertama."""
        for candidate in "XQ" + self.symbols:
            if candidate in self.positions and candidate != first:
                return candidate
        raise ValueError("Matriks tidak memiliki simbol penyisip yang valid.")

    def _prepare_pairs(self, plaintext: str) -> list[tuple[str, str]]:
        """Bagi plaintext menjadi pasangan dan sisipkan simbol bila diperlukan."""
        text = self.normalize(plaintext)
        pairs: list[tuple[str, str]] = []
        index = 0

        while index < len(text):
            first = text[index]
            second = text[index + 1] if index + 1 < len(text) else self._filler_for(first)

            if first == second:
                pairs.append((first, self._filler_for(first)))
                index += 1
            else:
                pairs.append((first, second))
                index += 2

        return pairs

    def _transform_pair(self, first: str, second: str, direction: int) -> str:
        first_row, first_column = self.positions[first]
        second_row, second_column = self.positions[second]

        if first_row == second_row:
            return (
                self.matrix[first_row][(first_column + direction) % self.size]
                + self.matrix[second_row][(second_column + direction) % self.size]
            )

        if first_column == second_column:
            return (
                self.matrix[(first_row + direction) % self.size][first_column]
                + self.matrix[(second_row + direction) % self.size][second_column]
            )

        return self.matrix[first_row][second_column] + self.matrix[second_row][first_column]

    def encrypt(self, plaintext: str) -> str:
        """Enkripsi plaintext dan kembalikan ciphertext tanpa pemisah."""
        return "".join(
            self._transform_pair(first, second, direction=1)
            for first, second in self._prepare_pairs(plaintext)
        )

    def decrypt(self, ciphertext: str) -> str:
        """Dekripsi ciphertext yang panjangnya genap."""
        text = self.normalize(ciphertext)
        if len(text) % 2 != 0:
            raise ValueError("Ciphertext harus memiliki jumlah simbol genap.")

        return "".join(
            self._transform_pair(text[index], text[index + 1], direction=-1)
            for index in range(0, len(text), 2)
        )

    def print_matrix(self) -> None:
        """Tampilkan matriks kunci dalam format yang mudah dibaca."""
        horizontal = "─" * 3
        print("┌" + "┬".join([horizontal] * self.size) + "┐")
        for row_index, row in enumerate(self.matrix):
            print("│ " + " │ ".join(row) + " │")
            if row_index < self.size - 1:
                print("├" + "┼".join([horizontal] * self.size) + "┤")
        print("└" + "┴".join([horizontal] * self.size) + "┘")


def get_input(label: str, allowed_symbols: str) -> str:
    """Minta input sampai terdapat simbol yang berlaku untuk matriks."""
    while True:
        value = input(label).strip()
        try:
            normalized = PlayfairCipher._clean_text(value, allowed_symbols)
        except ValueError as error:
            print(f"{error} Silakan coba lagi.\n")
            continue
        if normalized:
            return normalized
        print(f"Input harus mengandung minimal satu simbol dari: {allowed_symbols}.\n")


def get_configuration() -> tuple[str, str | None]:
    """Minta pengguna memilih himpunan simbol dan pengecualian yang sesuai."""
    print("Pilih jenis matriks:")
    print("1. Huruf A-Z (5x5, pilih satu huruf yang tidak dipakai)")
    print("2. Angka 0-9 (3x3, pilih satu angka yang tidak dipakai)")
    print("3. Angka 0-9 + huruf A-Z (6x6, tanpa pengecualian)")
    print("4. Huruf A-Z + angka 0-9 (6x6, tanpa pengecualian)")

    while True:
        choice = input("Pilihan [1/2/3/4] : ").strip()
        if choice == "1":
            while True:
                exception = input("Huruf yang tidak diikutkan [contoh J] : ").strip().upper()
                if len(exception) == 1 and exception in string.ascii_uppercase:
                    return "letters", exception
                print("Masukkan tepat satu huruf A-Z. Silakan coba lagi.\n")
        elif choice == "2":
            while True:
                exception = input("Angka yang tidak diikutkan [contoh 0] : ").strip()
                if len(exception) == 1 and exception in string.digits:
                    return "digits", exception
                print("Masukkan tepat satu angka 0-9. Silakan coba lagi.\n")
        elif choice == "3":
            return "alphanumeric", None
        elif choice == "4":
            return "alphanumeric_letters_first", None
        else:
            print("Pilihan harus 1, 2, 3, atau 4. Silakan coba lagi.\n")


def main() -> None:
    """Jalankan program Playfair Cipher interaktif."""
    print("=" * 54)
    print("             PROGRAM PLAYFAIR CIPHER")
    print("=" * 54)

    mode, exception = get_configuration()
    cipher = PlayfairCipher("", mode=mode, exception=exception)
    key = get_input("Masukkan kata kunci : ", cipher.symbols)
    plaintext = get_input("Masukkan plaintext  : ", cipher.symbols)

    # Buat ulang setelah kunci tervalidasi agar matriks memasukkan kata kunci.
    cipher = PlayfairCipher(key, mode=mode, exception=exception)
    ciphertext = cipher.encrypt(plaintext)
    decrypted_text = cipher.decrypt(ciphertext)

    print("\n" + "-" * 54)
    print("HASIL")
    print("-" * 54)
    print(f"Jenis matriks : {cipher.size}x{cipher.size}")
    print(f"Pengecualian  : {cipher.exception if cipher.exception is not None else '-'}")
    print(f"Kata kunci    : {key}")
    cipher.print_matrix()
    print(f"Plaintext     : {plaintext}")
    print(f"Dekripsi      : {decrypted_text}")
    print(f"Ciphertext    : {ciphertext}")


if __name__ == "__main__":
    main()
