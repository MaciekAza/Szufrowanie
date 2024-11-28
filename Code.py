import pygame
import os
import random


# Funkcja szyfrowania
def simple_encrypt(data, password):
    encrypted = []
    for i, char in enumerate(data):
        key = ord(password[i % len(password)])  # Pobieramy kod ASCII z hasła
        encrypted.append((ord(char) + key) % 256)  # Zaszyfrowanie poprzez przesunięcie w ASCII
    return encrypted


# Funkcja deszyfrowania
def simple_decrypt(encrypted_data, password):
    decrypted = []
    for i, encrypted_char in enumerate(encrypted_data):
        key = ord(password[i % len(password)])  # Pobieramy kod ASCII z hasła
        decrypted.append(chr((encrypted_char - key) % 256))  # Odszyfrowanie poprzez cofnięcie przesunięcia
    return "".join(decrypted)  # Zwrócenie odszyfrowanego tekstu


# Funkcja do zapisu zaszyfrowanego klucza
def save_encrypted_key(key, password, filename="key.enc"):
    key_str = str(key)
    encrypted_key = simple_encrypt(key_str, password)
    with open(filename, "w", encoding="utf-8") as key_file:
        key_file.write(" ".join(map(str, encrypted_key)))


# Funkcja do odczytu i odszyfrowania klucza
def load_encrypted_key(password, filename="key.enc"):
    if not os.path.exists(filename):
        print(f"Plik '{filename}' nie istnieje. Tworzymy nowy klucz.")
        key = generate_key()
        save_encrypted_key(key, password)
        return key

    try:
        with open(filename, "r", encoding="utf-8") as key_file:
            encrypted_key = key_file.read().strip().split()
            encrypted_key = list(map(int, encrypted_key))
    except Exception as e:
        print(f"Nie udało się odczytać pliku klucza: {e}")
        return None

    decrypted_key = simple_decrypt(encrypted_key, password)
    key_str = decrypted_key
    key = eval(key_str)  # Konwersja z powrotem na obiekt Python
    return key


# Funkcja do generowania klucza
def generate_key():
    shuffled_alph = list("abcdefghijklmnopqrstuvwxyz")
    random.shuffle(shuffled_alph)
    shift = random.randint(1, 25)
    return {"alphabet": "".join(shuffled_alph), "shift": shift}


# Funkcja tworzenia plików 'odsz.txt' i 'zasz.txt'
def create_initial_files():
    with open("odsz.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open("zasz.txt", "w", encoding="utf-8") as f:
        f.write("")
    print("Utworzono pliki 'odsz.txt' i 'zasz.txt'.")


# Funkcja szyfrowania
def zaszyf(dane, key):
    zaszyfrowane = []
    alphabet = key["alphabet"]
    shift = key["shift"]
    for char in dane:
        if char.isalpha():
            index = alphabet.index(char.lower())
            new_index = (index + shift) % len(alphabet)
            new_char = alphabet[new_index]
            if char.isupper():
                new_char = new_char.upper()
            zaszyfrowane.append(new_char)
        else:
            zaszyfrowane.append(char)
    return "".join(zaszyfrowane)


# Funkcja odszyfrowania
def odszyfr(dane, key):
    odszyfrowane = []
    alphabet = key["alphabet"]
    shift = key["shift"]
    for char in dane:
        if char.isalpha():
            index = alphabet.index(char.lower())
            new_index = (index - shift) % len(alphabet)
            new_char = alphabet[new_index]
            if char.isupper():
                new_char = new_char.upper()
            odszyfrowane.append(new_char)
        else:
            odszyfrowane.append(char)
    return "".join(odszyfrowane)


# Główna funkcja programu
def main():
    pygame.init()

    # Ustawienia okna
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Program Szyfrujący")
    font = pygame.font.SysFont(None, 30)

    # Kolory
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (169, 169, 169)

    # Ustawienia przycisków
    button_width = 200
    button_height = 50
    button_x = (600 - button_width) // 2

    # Przyciski
    encrypt_button = pygame.Rect(button_x, 150, button_width, button_height)
    decrypt_button = pygame.Rect(button_x, 230, button_width, button_height)
    exit_button = pygame.Rect(button_x, 310, button_width, button_height)

    input_box = pygame.Rect(150, 50, 300, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    text_surface = font.render('Wprowadź hasło', True, color)

    # Główna pętla programu
    running = True
    while running:
        screen.fill(WHITE)

        # Rysowanie przycisków
        pygame.draw.rect(screen, GREEN, encrypt_button)
        pygame.draw.rect(screen, BLUE, decrypt_button)
        pygame.draw.rect(screen, RED, exit_button)
        pygame.draw.rect(screen, color, input_box, 2)

        # Rysowanie tekstu na przyciskach
        screen.blit(font.render("Zaszyfruj", True, WHITE), (encrypt_button.x + 50, encrypt_button.y + 10))
        screen.blit(font.render("Odszyfruj", True, WHITE), (decrypt_button.x + 50, decrypt_button.y + 10))
        screen.blit(font.render("Zakończ", True, WHITE), (exit_button.x + 70, exit_button.y + 10))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        password = text
                        key = load_encrypted_key(password)
                        if key:
                            print("Załadowano klucz.")
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    text_surface = font.render(text, True, color)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if encrypt_button.collidepoint(mouse_x, mouse_y):
                    # Zaszyfrowanie danych
                    password = text  # Pobieramy hasło
                    key = load_encrypted_key(password)
                    if key:
                        with open("odsz.txt", "r", encoding="utf-8") as file:
                            data = file.read()
                        encrypted_data = zaszyf(data, key)
                        with open("zasz.txt", "w", encoding="utf-8") as file:
                            file.write(encrypted_data)
                        print("Dane zostały zaszyfrowane!")
                if decrypt_button.collidepoint(mouse_x, mouse_y):
                    # Odszyfrowanie danych
                    password = text  # Pobieramy hasło
                    key = load_encrypted_key(password)
                    if key:
                        with open("zasz.txt", "r", encoding="utf-8") as file:
                            data = file.read()
                        decrypted_data = odszyfr(data, key)
                        with open("odsz.txt", "w", encoding="utf-8") as file:
                            file.write(decrypted_data)
                        print("Dane zostały odszyfrowane!")
                if exit_button.collidepoint(mouse_x, mouse_y):
                    running = False

        pygame.display.flip()

    pygame.quit()


# Uruchomienie programu
if __name__ == "__main__":
    main()
