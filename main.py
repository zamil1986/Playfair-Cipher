"""Contoh implementasi Playfair Cipher 5 x 5.

Playfair menggabungkan I/J dalam satu sel sehingga alfabet yang dipakai
berjumlah 25 huruf. Program ini hanya ditujukan untuk pembelajaran,
bukan untuk melindungi data modern.
"""

from __future__ import annotations

import string


class PlayfairCipher:
    """Enkripsi dan dekripsi teks dengan kunci Playfair."""

    def __init__(self, key: str) -> None:
        self.matrix = self._build_matrix(key)
        self.positions = {
            letter: (row, column)
            for row, row_values in enumerate(self.matrix)
            for column, letter in enumerate(row_values)
        }

    @staticmethod
    def _normalize(text: str) -> str:
        """Ambil huruf A-Z saja dan satukan J menjadi I."""
        return "".join(
            character if character != "J" else "I"
            for character in text.upper()
            if character in string.ascii_uppercase
        )

    def _build_matrix(self, key: str) -> list[list[str]]:
        alphabet = string.ascii_uppercase.replace("J", "")
        letters: list[str] = []

        for character in self._normalize(key) + alphabet:
            if character not in letters:
                letters.append(character)

        return [letters[index : index + 5] for index in range(0, 25, 5)]

    def _prepare_pairs(self, plaintext: str) -> list[tuple[str, str]]:
        """Bagi plaintext menjadi pasangan dan sisipkan X bila diperlukan."""
        text = self._normalize(plaintext)
        pairs: list[tuple[str, str]] = []
        index = 0

        while index < len(text):
            first = text[index]
            second = text[index + 1] if index + 1 < len(text) else "X"

            if first == second:
                # Q dipakai jika huruf ganda adalah X agar pasangan tetap berbeda.
                pairs.append((first, "Q" if first == "X" else "X"))
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
                self.matrix[first_row][(first_column + direction) % 5]
                + self.matrix[second_row][(second_column + direction) % 5]
            )

        if first_column == second_column:
            return (
                self.matrix[(first_row + direction) % 5][first_column]
                + self.matrix[(second_row + direction) % 5][second_column]
            )

        return self.matrix[first_row][second_column] + self.matrix[second_row][first_column]

    def encrypt(self, plaintext: str) -> str:
        """Enkripsi plaintext dan kembalikan ciphertext tanpa spasi."""
        return "".join(
            self._transform_pair(first, second, direction=1)
            for first, second in self._prepare_pairs(plaintext)
        )

    def decrypt(self, ciphertext: str) -> str:
        """Dekripsi ciphertext valid yang panjangnya genap."""
        text = self._normalize(ciphertext)
        if len(text) % 2 != 0:
            raise ValueError("Ciphertext harus memiliki jumlah huruf genap.")

        return "".join(
            self._transform_pair(text[index], text[index + 1], direction=-1)
            for index in range(0, len(text), 2)
        )

    def print_matrix(self) -> None:
        """Tampilkan matriks kunci dalam format yang mudah dibaca."""
        border = "├───┼───┼───┼───┼───┤"
        print("┌───┬───┬───┬───┬───┐")
        for row in self.matrix:
            print("│ " + " │ ".join(row) + " │")
            if row != self.matrix[-1]:
                print(border)
        print("└───┴───┴───┴───┴───┘")


def get_input(label: str) -> str:
    """Minta input sampai pengguna menulis setidaknya satu huruf."""
    while True:
        value = input(label).strip()
        if PlayfairCipher._normalize(value):
            return value
        print("Input harus mengandung minimal satu huruf A-Z. Silakan coba lagi.\n")


def main() -> None:
    """Jalankan program Playfair Cipher interaktif."""
    print("=" * 46)
    print("          PROGRAM PLAYFAIR CIPHER")
    print("=" * 46)
    print("Catatan: huruf J akan diproses sebagai I.\n")

    key = get_input("Masukkan kata kunci : ")
    plaintext = get_input("Masukkan plaintext  : ")

    cipher = PlayfairCipher(key)
    ciphertext = cipher.encrypt(plaintext)
    decrypted_text = cipher.decrypt(ciphertext)

    print("\n" + "-" * 46)
    print("HASIL")
    print("-" * 46)
    print(f"Kata kunci : {PlayfairCipher._normalize(key)}")
    cipher.print_matrix()
    print(f"Plaintext  : {PlayfairCipher._normalize(plaintext)}")
    print(f"Ciphertext : {ciphertext}")
    print(f"Dekripsi   : {decrypted_text}")


if __name__ == "__main__":
    main()
