import os

# Алфавіт російських малих літер без літери ё
ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = ALPHABET.replace("ё", "")  # Виключаємо літеру ё
ALPHABET_SIZE = len(ALPHABET)

# Ключі різної довжини
KEYS = {
    2: "да",
    3: "нет",
    4: "дома",
    5: "парус",
    10: "яушладомой",
    20: "нетянеушладомойкотик"
}


# Функція для шифрування тексту
def vigenere_encrypt(plaintext, key):
    ciphertext = []
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_index = ALPHABET.index(key[i % key_length])
            cipher_index = (char_index + key_index) % ALPHABET_SIZE
            ciphertext.append(ALPHABET[cipher_index])
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)


# Функція для обчислення індексу відповідності
def calculate_index_of_coincidence(text):
    n = len(text)
    frequencies = {char: text.count(char) for char in ALPHABET}
    index_of_coincidence = sum(f * (f - 1) for f in frequencies.values())
    index_of_coincidence /= n * (n - 1) if n > 1 else 1
    return index_of_coincidence


# Функція для читання тексту з файлу
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()


# Функція для запису тексту у файл
def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


# Основна функція
def main():
    input_filename = input("Введіть назву вхідного файлу (з розширенням .txt): ")
    if not os.path.exists(input_filename):
        print("Файл не знайдено!")
        return

    action = input("Оберіть дію: 1 - зашифрувати, 2 - розшифрувати: ")

    if action == '1':
        plaintext = read_file(input_filename)
        result = []

        for key_length, key in KEYS.items():
            encrypted_text = vigenere_encrypt(plaintext, key)
            index_of_coincidence = calculate_index_of_coincidence(encrypted_text)
            result.append(f"Ключ {key_length} ({key}):\n{encrypted_text}\n")
            print(f"На ключі довжини {key_length} ({key}) індекс відповідності між ВТ та ШТ: {index_of_coincidence:.6f}")

        write_file("Ш.txt", '\n'.join(result))
        print("Текст зашифровано. Результат записано у файл Ш.txt.")
    else:
        print("Наразі підтримується лише шифрування.")


if __name__ == "__main__":
    main()
