#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
guessnumber.py — Juego de consola "Adivina el número" en un único archivo .py

- Sin dependencias externas (solo librería estándar).
- Compatible con Windows/macOS/Linux.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import textwrap
import time
from typing import Dict, Tuple, Optional


VERSION = "1.0.0"


# ----------------------------- i18n (ES/EN) -----------------------------
ES_STRINGS: Dict[str, str] = {
    "title": "Juego: Adivina el Número",
    "intro": "He pensado un número entero entre {min} y {max}. Tienes {attempts} intentos.",
    "try_label": "Intento",
    "enter_int": "Introduce un número entero: ",
    "invalid_int": "Debes introducir un número entero. Inténtalo de nuevo.",
    "out_of_range": "El número está fuera del rango [{min}..{max}]. Inténtalo otra vez.",
    "too_low": "Mi número es mayor.",
    "too_high": "Mi número es menor.",
    "very_hot": "muy caliente",
    "hot": "caliente",
    "warm": "templado",
    "cold": "frío",
    "remaining": "Intentos restantes: {n}",
    "win": "¡Correcto! 🎉 Lo adivinaste en {used} intento{suffix}.",
    "lose": "Se acabaron los intentos. El número era: {secret}",
    "score": "Tu puntuación: {score}",
    "new_record": "¡Nuevo récord! 🏆 Antes: {prev}, ahora: {now}",
    "play_again": "¿Quieres jugar otra vez? [Y/n]: ",
    "goodbye": "¡Hasta luego!",
    "help_proximity": "Pistas de proximidad activadas (caliente/frío).",
    "help_quiet": "Modo silencioso: solo pistas y resultado final.",
    "config_error_range": "Error: el rango debe contener al menos 2 números (min < max).",
    "config_error_attempts": "Error: el número de intentos debe ser >= 1.",
    "aborted": "Interrumpido por el usuario.",
    "eof": "Entrada finalizada.",
    "version": "Versión del programa: {version}",
}

EN_STRINGS: Dict[str, str] = {
    "title": "Game: Guess the Number",
    "intro": "I'm thinking of an integer between {min} and {max}. You have {attempts} attempts.",
    "try_label": "Attempt",
    "enter_int": "Enter an integer: ",
    "invalid_int": "An integer is required. Try again.",
    "out_of_range": "Number is out of range [{min}..{max}]. Try again.",
    "too_low": "My number is higher.",
    "too_high": "My number is lower.",
    "very_hot": "very hot",
    "hot": "hot",
    "warm": "warm",
    "cold": "cold",
    "remaining": "Attempts left: {n}",
    "win": "Correct! 🎉 You guessed it in {used} attempt{suffix}.",
    "lose": "No attempts left. The secret number was: {secret}",
    "score": "Your score: {score}",
    "new_record": "New high score! 🏆 Was: {prev}, now: {now}",
    "play_again": "Play again? [Y/n]: ",
    "goodbye": "See you!",
    "help_proximity": "Proximity hints enabled (hot/cold).",
    "help_quiet": "Quiet mode: hints and final result only.",
    "config_error_range": "Error: range must contain at least 2 numbers (min < max).",
    "config_error_attempts": "Error: number of attempts must be >= 1.",
    "aborted": "Aborted by user.",
    "eof": "Input ended.",
    "version": "Program version: {version}",
}

LANG_MAP = {
    "es": ES_STRINGS,
    "en": EN_STRINGS,
}

YES_CHARS = {
    "es": set("sSyYsíSÍ"),
    "en": set("yY"),
}
NO_CHARS = {
    "es": set("nNnoNO"),
    "en": set("nN"),
}


# ----------------------------- Utilidad de color ANSI -----------------------------
def supports_color(stream) -> bool:
    """Detecta si el stream soporta colores ANSI."""
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    if os.name == "nt":
        return True
    return True


def paint(text: str, style: str, enable: bool) -> str:
    """Devuelve texto coloreado si enable=True; de lo contrario, texto plano."""
    if not enable:
        return text
    styles = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }
    return f"{styles.get(style, '')}{text}{styles['reset']}"


# ----------------------------- Argumentos CLI -----------------------------
def parse_args() -> argparse.Namespace:
    """Parses de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="guessnumber.py",
        description="Juego de consola: adivina el número (un solo archivo).",
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "normal", "hard"],
        default="normal",
        help="Preajustes de dificultad (afecta rango y/o intentos).",
    )
    parser.add_argument(
        "--min", dest="min_v", type=int, default=None, help="Límite inferior del rango."
    )
    parser.add_argument(
        "--max", dest="max_v", type=int, default=None, help="Límite superior del rango."
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=None,
        help="Número fijo de intentos (sobrescribe dificultad).",
    )
    parser.add_argument(
        "--proximity",
        action="store_true",
        help="Activa pistas de proximidad (caliente/frío).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Fija la semilla del generador aleatorio (para pruebas).",
    )
    parser.add_argument(
        "--no-score",
        action="store_true",
        help="Desactiva la puntuación y el guardado de récord local.",
    )
    parser.add_argument(
        "--lang",
        choices=list(LANG_MAP.keys()),
        default="es",
        help="Idioma de la interfaz (es/en).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desactiva color ANSI.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Modo silencioso: sólo pistas y resultado final.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Muestra la versión y sale.",
    )

    args = parser.parse_args()

    if args.min_v is None or args.max_v is None:
        if args.difficulty == "easy":
            args.min_v, args.max_v = 1, 50
        elif args.difficulty == "normal":
            args.min_v, args.max_v = 1, 100
        else:
            args.min_v, args.max_v = 1, 1000

    return args


# ----------------------------- Lógica de intentos -----------------------------
def compute_attempts(
    min_v: int, max_v: int, difficulty: str, attempts_override: Optional[int]
) -> int:
    """Calcula el número de intentos según rango/dificultad o sobrescribe."""
    if attempts_override is not None:
        return max(1, int(attempts_override))
    R = max_v - min_v + 1
    base = math.ceil(math.log2(R))
    if difficulty == "easy":
        return base + 2
    if difficulty == "normal":
        return base + 1
    return base


# ----------------------------- Generación y pistas -----------------------------
def pick_secret(min_v: int, max_v: int, rng: random.Random) -> int:
    """Elige el número secreto en [min_v, max_v]."""
    return rng.randint(min_v, max_v)


def proximity_label(guess: int, secret: int, min_v: int, max_v: int, strings: Dict[str, str]) -> str:
    """Devuelve una etiqueta de proximidad (muy caliente/caliente/templado/frío)."""
    R = max_v - min_v + 1
    d = abs(guess - secret)
    if d <= max(1, int(0.01 * R)):
        return strings["very_hot"]
    if d <= max(1, int(0.03 * R)):
        return strings["hot"]
    if d <= max(1, int(0.07 * R)):
        return strings["warm"]
    return strings["cold"]


# ----------------------------- Entrada robusta -----------------------------
def read_int(prompt: str, min_v: int, max_v: int, strings: Dict[str, str]) -> int:
    """Lee un entero válido del usuario, sin consumir intento en caso de error."""
    while True:
        try:
            raw = input(prompt)
        except KeyboardInterrupt:
            raise
        except EOFError:
            raise
        if not raw.strip():
            print(strings["invalid_int"])
            continue
        try:
            val = int(raw.strip())
        except ValueError:
            print(strings["invalid_int"])
            continue
        if val < min_v or val > max_v:
            print(strings["out_of_range"].format(min=min_v, max=max_v))
            continue
        return val


# ----------------------------- Puntuación y récord -----------------------------
def score_formula(attempts_total: int, attempts_used: int) -> int:
    base = 100
    remaining = max(0, attempts_total - attempts_used)
    bonus = 10 * remaining
    return base + bonus


def score_file_path() -> str:
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, ".guessnumber_score.json")


def load_score(path: str) -> Optional[dict]:
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_score(path: str, obj: dict) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def update_and_store_score(
    score_path: str,
    new_score: int,
    min_v: int,
    max_v: int,
) -> Tuple[bool, Optional[int], int]:
    prev_obj = load_score(score_path) or {}
    prev_best = prev_obj.get("best_score")
    is_record = prev_best is None or new_score > int(prev_best)

    if is_record:
        obj = {
            "best_score": int(new_score),
            "best_range": [min_v, max_v],
            "timestamp": int(time.time()),
        }
        save_score(score_path, obj)
        return True, prev_best, new_score
    return False, prev_best, int(prev_best)


# ----------------------------- S/N genérico -----------------------------
def ask_yes_no(prompt: str, default_yes: bool, lang: str) -> bool:
    yes_set = YES_CHARS.get(lang, YES_CHARS["en"])
    no_set = NO_CHARS.get(lang, NO_CHARS["en"])
    while True:
        try:
            resp = input(prompt)
        except KeyboardInterrupt:
            return False
        except EOFError:
            return False
        s = resp.strip()
        if not s:
            return default_yes
        ch = s[0]
        if ch in yes_set:
            return True
        if ch in no_set:
            return False


# ----------------------------- Juego: una ronda -----------------------------
def play_round(
    cfg: argparse.Namespace,
    strings: Dict[str, str],
    color_on: bool,
    rng: random.Random,
) -> Tuple[bool, int, int]:
    secret = pick_secret(cfg.min_v, cfg.max_v, rng)
    attempts_total = compute_attempts(cfg.min_v, cfg.max_v, cfg.difficulty, cfg.attempts)

    if not cfg.quiet:
        print(paint(strings["title"], "bold", color_on))
        intro = strings["intro"].format(min=cfg.min_v, max=cfg.max_v, attempts=attempts_total)
        print(textwrap.fill(intro, width=88))
        if cfg.proximity:
            print(paint(strings["help_proximity"], "blue", color_on))
        if cfg.quiet:
            print(strings["help_quiet"])

    used = 0
    won = False

    while used < attempts_total:
        try_prompt = f"{strings['try_label']} {used + 1}: "
        try:
            guess = read_int(try_prompt, cfg.min_v, cfg.max_v, strings)
        except KeyboardInterrupt:
            raise
        except EOFError:
            raise

        if guess == secret:
            won = True
            break

        if guess < secret:
            print(paint(strings["too_low"], "yellow", color_on))
        else:
            print(paint(strings["too_high"], "yellow", color_on))

        if cfg.proximity:
            prox = proximity_label(guess, secret, cfg.min_v, cfg.max_v, strings)
            print(f"({prox})")

        used += 1
        remaining = attempts_total - used
        print(strings["remaining"].format(n=remaining))

    score = 0
    if won:
        suffix = "" if used == 1 else "s"
        msg = strings["win"].format(used=used if used else 1, suffix=suffix)
        print(paint(msg, "green", color_on))
        score = score_formula(attempts_total, used if used else 1)
    else:
        print(paint(strings["lose"].format(secret=secret), "red", color_on))

    return won, used if used else (0 if not won else 1), score


# ----------------------------- main -----------------------------
def main() -> int:
    args = parse_args()
    strings = LANG_MAP[args.lang]

    if args.version:
        print(strings["version"].format(version=VERSION))
        return 0

    if not (args.min_v < args.max_v):
        print(strings["config_error_range"], file=sys.stderr)
        return 2
    attempts = compute_attempts(args.min_v, args.max_v, args.difficulty, args.attempts)
    if attempts < 1:
        print(strings["config_error_attempts"], file=sys.stderr)
        return 2

    color_on = supports_color(sys.stdout) and (not args.no_color) and (not args.quiet)

    rng = random.Random(args.seed) if args.seed is not None else random.Random()

    score_path = score_file_path()
    try:
        while True:
            try:
                won, used, score = play_round(args, strings, color_on, rng)
            except KeyboardInterrupt:
                print(paint(strings["aborted"], "red", color_on))
                return 130
            except EOFError:
                print(paint(strings["eof"], "red", color_on))
                return 1

            if won and not args.no_score:
                print(strings["score"].format(score=score))
                is_record, prev, now = update_and_store_score(
                    score_path, score, args.min_v, args.max_v
                )
                if is_record:
                    prev_display = "-" if prev is None else str(prev)
                    print(paint(strings["new_record"].format(prev=prev_display, now=now), "blue", color_on))

            if not ask_yes_no(strings["play_again"], default_yes=True, lang=args.lang):
                if not args.quiet:
                    print(strings["goodbye"])
                break
    except Exception as ex:
        print(f"Unexpected error: {ex}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())