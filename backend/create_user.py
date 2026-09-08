"""Crea un utente.

Uso:  python create_user.py <username> <nome_visual> <password|RANDOM>
Con RANDOM genera una password forte e la stampa (da consegnare all'utente).
"""
import secrets
import sys

import auth


def main() -> None:
    if len(sys.argv) != 4:
        print("Uso: python create_user.py <username> <nome_visual> <password|RANDOM>")
        return
    username, display, password = sys.argv[1], sys.argv[2], sys.argv[3]
    generated = None
    if password == "RANDOM":
        password = secrets.token_urlsafe(12)
        generated = password
    auth.create_user(username, display, password)
    print(f"Utente '{username}' creato.")
    if generated:
        print(f"Password generata: {generated}")


if __name__ == "__main__":
    main()
