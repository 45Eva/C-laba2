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

LETTER_FREQUENCES = {
    'а': 0.0697201,
    'б': 0.0172286,
    'в': 0.056724,
    'г': 0.0213469,
    'д': 0.0324454,
    'е': 0.0858417,
    'ж': 0.00986348,
    'з': 0.0162057,
    'и': 0.0879848,
    'й': 0.0114292,
    'к': 0.0311624,
    'л': 0.0499457,
    'м': 0.0361014,
    'н': 0.0651102,
    'о': 0.104177,
    'п': 0.0195504,
    'р': 0.0443487,
    'с': 0.0633102,
    'т': 0.0510155,
    'у': 0.0256018,
    'ф': 0.000955243,
    'х': 0.0115707,
    'ц': 0.00528456,
    'ч': 0.00954003,
    'ш': 0.00566461,
    'щ': 0.00225927,
    'ъ': 0.000411046,
    'ы': 0.0182337,
    'ь': 0.0155054,
    'э': 0.000103772,
    'ю': 0.00895783,
    'я': 0.0224008
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
def find_key_length(ciphertext, maxKeyLength=20):
    possible_candidates = {}
    for r in range(2, maxKeyLength):
        d = 0
        for i in range(len(ciphertext) - r):
            d += ciphertext[i] == ciphertext[i + r]
        possible_candidates[r] = d
    result = max(possible_candidates, key=possible_candidates.get)
    return result, possible_candidates


# Функція для знаходження ключа
def find_key(ciphertext, key_length):
    blocks = [''.join(ciphertext[i::key_length]) for i in range(key_length)]
    key = ''
    most_frequent_in_lang = MOST_FREQUENT_LETTERS[0]
    for block in blocks:
        freq = {char: block.count(char) for char in ALPHABET}
        most_frequent_in_block = max(freq, key=freq.get)

        key += ALPHABET[
            (ALPHABET.index(most_frequent_in_block) - ALPHABET.index(most_frequent_in_lang)) % ALPHABET_SIZE]

    return key


def find_key_exact(ciphertext, key_length):
    blocks = [''.join(ciphertext[i::key_length]) for i in range(key_length)]
    res_key = ""
    for block in blocks:
        m_list = {}
        for g in ALPHABET:
            m_g = 0
            for t in ALPHABET:
                freq = {char: block.count(char) for char in ALPHABET}
                m_g += LETTER_FREQUENCES[t] * freq[ALPHABET[(ALPHABET.index(t) + ALPHABET.index(g)) % ALPHABET_SIZE]]
            m_list[g] = m_g

        res_key += max(m_list, key=m_list.get)

    return res_key


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
        ciphertext = ciphertext.replace('\n', '')
        key_length, estimated_key_lengths = find_key_length(ciphertext)
        if key_length:
            print(f"Знайдені довжини ключів та їхні індекси відповідності: {estimated_key_lengths}")
            print(f"Знайдена довжина ключа: {key_length}")
            key = find_key(ciphertext, key_length)
            print(f"Знайдений ключ першим способом: {key}")
            key = find_key_exact(ciphertext, key_length)
            print(f"Знайдений ключ другим способом: {key}")
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
