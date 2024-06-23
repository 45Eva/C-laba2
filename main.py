import os

# Алфавіт російських малих літер без літери ё
ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = ALPHABET.replace("ё", "")  # Виключаємо літеру ё
ALPHABET_SIZE = len(ALPHABET)
# Найімовірніші літери у російській мові (список)
MOST_FREQUENT_LETTERS = ['о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л']

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


# Функція для розшифрування тексту
def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_index = ALPHABET.index(key[i % key_length])
            plain_index = (char_index - key_index) % ALPHABET_SIZE
            plaintext.append(ALPHABET[plain_index])
        else:
            plaintext.append(char)
    return ''.join(plaintext)


# Функція для обчислення індексу відповідності
def calculate_index_of_coincidence(text):
    n = len(text)
    frequencies = {char: text.count(char) for char in ALPHABET}
    index_of_coincidence = sum(f * (f - 1) for f in frequencies.values())
    index_of_coincidence /= n * (n - 1) if n > 1 else 1
    return index_of_coincidence


# Функція для знаходження довжини ключа
def find_key_length(ciphertext):
    estimated_key_lengths = []
    for r in range(2, 21):  # Перевіримо довжини ключа від 2 до 20
        blocks = [''.join(ciphertext[i::r]) for i in range(r)]
        ic_values = [calculate_index_of_coincidence(block) for block in blocks]
        avg_ic = sum(ic_values) / r
        if avg_ic > 0.055:  # Порогове значення для вибору довжини ключа
            estimated_key_lengths.append((r, avg_ic))

    # Додатковий алгоритм для великих значень r
    for r in range(2, 21):
        blocks = [''.join(ciphertext[i::r]) for i in range(r)]
        ic_values = [calculate_index_of_coincidence(block) for block in blocks]
        avg_ic = sum(ic_values) / r
        if abs(avg_ic - 1 / ALPHABET_SIZE) > 0.01:  # Теоретичне значення I для даної мови
            estimated_key_lengths.append((r, avg_ic))

    if estimated_key_lengths:
        best_guess = max(estimated_key_lengths, key=lambda x: x[1])
        return best_guess[0], estimated_key_lengths
    return None, []


# Функція для знаходження ключа
def find_key(ciphertext, key_length):
    blocks = [''.join(ciphertext[i::key_length]) for i in range(key_length)]
    key = ''
    for block in blocks:
        freq = {char: block.count(char) for char in ALPHABET}
        most_frequent_in_block = max(freq, key=freq.get)
        for letter in MOST_FREQUENT_LETTERS:
            key_char_index = (ALPHABET.index(most_frequent_in_block) - ALPHABET.index(letter)) % ALPHABET_SIZE
            potential_key_char = ALPHABET[key_char_index]
            if potential_key_char in ALPHABET:
                key += potential_key_char
                break
    return key


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
            print(
                f"На ключі довжини {key_length} ({key}) індекс відповідності між ВТ та ШТ: {index_of_coincidence:.6f}")

        write_file("Ш.txt", '\n'.join(result))
        print("Текст зашифровано. Результат записано у файл Ш.txt.")

    elif action == '2':
        ciphertext = read_file(input_filename)
        key_length, estimated_key_lengths = find_key_length(ciphertext)
        if key_length:
            print(f"Знайдені довжини ключів та їхні індекси відповідності: {estimated_key_lengths}")
            key = find_key(ciphertext, key_length)
            print(f"Знайдена довжина ключа: {key_length}")
            print(f"Знайдений ключ: {key}")
            decrypted_text = vigenere_decrypt(ciphertext, key)
            write_file("R.txt", decrypted_text)
            print(f"Текст розшифровано. Ключ: {key}. Результат записано у файл R.txt.")
        else:
            print("Не вдалося визначити довжину ключа.")
            print(f"Розглянуті довжини ключів та їхні індекси відповідності: {estimated_key_lengths}")
    else:
        print("Неправильна дія!")


if __name__ == "__main__":
    main()
