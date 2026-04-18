#!/usr/bin/env python3
"""
wordgen — Human-pattern Wordlist Generator
Zero external dependencies. Python 3.8+
"""

import os
import sys
import itertools
from datetime import datetime

os.system("clear")

# ─────────────────────────────────────────────
#  ANSI Colors
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GREEN   = "\033[38;5;82m"
    RED     = "\033[38;5;196m"
    YELLOW  = "\033[38;5;220m"
    CYAN    = "\033[38;5;51m"
    GRAY    = "\033[38;5;240m"
    WHITE   = "\033[38;5;255m"
    ORANGE  = "\033[38;5;208m"
    MAGENTA = "\033[38;5;213m"


# ─────────────────────────────────────────────
#  Banner
# ─────────────────────────────────────────────
def print_banner():
    print(f"""
{C.MAGENTA}{C.BOLD}\
  ██╗    ██╗ ██████╗ ██████╗ ██████╗  ██████╗ ███████╗███╗   ██╗
  ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║
  ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║  ███╗█████╗  ██╔██╗ ██║
  ██║███╗██║██║   ██║██╔══██╗██║  ██║██║   ██║██╔══╝  ██║╚██╗██║
  ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝███████╗██║ ╚████║
   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝
{C.RESET}{C.GRAY}  Human-Pattern Wordlist Generator{C.RESET}
""")


def sep():
    print(f"{C.GRAY}{'─' * 62}{C.RESET}")


def ask(prompt, example=""):
    ex = f" {C.GRAY}(ex: {example}){C.RESET}" if example else ""
    val = input(f"  {C.CYAN}?{C.RESET} {C.WHITE}{prompt}{C.RESET}{ex}: ").strip()
    return val if val else None


def ask_list(prompt, example=""):
    val = ask(prompt, example)
    if not val:
        return []
    return [v.strip() for v in val.replace(",", " ").split() if v.strip()]


def ask_bool(prompt):
    val = input(f"  {C.CYAN}?{C.RESET} {C.WHITE}{prompt}{C.RESET} {C.GRAY}[s/N]{C.RESET}: ").strip().lower()
    return val in ("s", "y", "sim", "yes")


# ─────────────────────────────────────────────
#  Leet substitutions
# ─────────────────────────────────────────────
LEET_MAP = {
    'a': '@', 'e': '3', 'i': '1', 'o': '0',
    's': '$', 't': '7', 'l': '1', 'b': '8',
}

def leet(word: str) -> str:
    return "".join(LEET_MAP.get(c.lower(), c) for c in word)

def capitalizations(word: str) -> list:
    variants = set()
    variants.add(word.lower())
    variants.add(word.upper())
    variants.add(word.capitalize())
    variants.add(word.title())
    # camelCase style se tiver espaço
    if " " in word:
        parts = word.split()
        variants.add(parts[0].lower() + "".join(p.capitalize() for p in parts[1:]))
    return list(variants)


# ─────────────────────────────────────────────
#  Sufixos / Prefixos comuns
# ─────────────────────────────────────────────
COMMON_SUFFIXES = [
    "!", "@", "#", "$", "%", "¨", "&", "*", "()", "_",
    "+", "-", ".", ",", ";", ":", "123", "1234", "12345",
    "!", "!!", "123!", "1", "2", "01", "007",
]

COMMON_PREFIXES = [
    "!", "@", "#", "$", "123", "1", "the", "my", "eu",
]


# ─────────────────────────────────────────────
#  Generators
# ─────────────────────────────────────────────
def gen_years(start: int, end: int) -> list:
    years = []
    for y in range(start, end + 1):
        years.append(str(y))          # 1985
        years.append(str(y)[2:])      # 85
    return years


def gen_numeric(years: list, use_years: bool, min_len: int, max_len: int) -> set:
    """Gera combinações puramente numéricas."""
    results = set()

    # PINs de 4 a max_len dígitos
    for length in range(max(4, min_len), min(max_len + 1, 9)):
        # sequências comuns
        results.add("0" * length)
        results.add("1" * length)
        seq = "".join(str(i % 10) for i in range(length))
        results.add(seq)
        results.add(seq[::-1])

    # anos e combinações
    if use_years:
        for y in years:
            results.add(y)
            results.add(y + "0")
            results.add(y + "1")
            results.add("0" + y)
            results.add(y + y[-2:])

    # datas comuns
    for day in range(1, 32):
        for month in range(1, 13):
            d = f"{day:02d}{month:02d}"
            if min_len <= len(d) <= max_len:
                results.add(d)
            if use_years:
                for y in years:
                    full = f"{day:02d}{month:02d}{y}"
                    if min_len <= len(full) <= max_len:
                        results.add(full)

    return results


def permutate_word(word: str, years: list, use_years: bool,
                   use_leet: bool, use_symbols: bool,
                   min_len: int, max_len: int) -> set:
    results = set()

    caps = capitalizations(word)
    base_forms = list(caps)

    if use_leet:
        for c in caps:
            base_forms.append(leet(c))
            base_forms.append(leet(c).capitalize())

    for form in base_forms:
        # forma pura
        if min_len <= len(form) <= max_len:
            results.add(form)

        # sufixos comuns
        if use_symbols:
            for suf in COMMON_SUFFIXES:
                w = form + suf
                if min_len <= len(w) <= max_len:
                    results.add(w)
            for pre in COMMON_PREFIXES:
                w = pre + form
                if min_len <= len(w) <= max_len:
                    results.add(w)

        # combinações com anos
        if use_years:
            for y in years:
                for combo in [form + y, y + form, form + y + "!", form + y + "@"]:
                    if min_len <= len(combo) <= max_len:
                        results.add(combo)

    # repetição da palavra
    doubled = word.lower() + word.lower()
    if min_len <= len(doubled) <= max_len:
        results.add(doubled)

    return results


def combine_words(words: list, years: list, use_years: bool,
                  use_symbols: bool, min_len: int, max_len: int) -> set:
    """Combina pares de palavras fornecidas."""
    results = set()
    if len(words) < 2:
        return results

    for a, b in itertools.permutations(words, 2):
        for ca in capitalizations(a):
            for cb in capitalizations(b):
                combo = ca + cb
                if min_len <= len(combo) <= max_len:
                    results.add(combo)
                combo2 = ca + "_" + cb
                if min_len <= len(combo2) <= max_len:
                    results.add(combo2)
                if use_years:
                    for y in years:
                        w = ca + cb + y
                        if min_len <= len(w) <= max_len:
                            results.add(w)
                if use_symbols:
                    for suf in ["!", "@", "123", "#1"]:
                        w = ca + cb + suf
                        if min_len <= len(w) <= max_len:
                            results.add(w)
    return results


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    print_banner()
    sep()
    print(f"  {C.GRAY}Pressione ENTER para pular qualquer campo.{C.RESET}")
    sep()
    print()

    # ── Coleta de dados ───────────────────────────────────────────────────
    print(f"  {C.YELLOW}[ PALAVRAS-CHAVE ]{C.RESET}")
    words = ask_list("Palavras-chave", "joao, empresa, flamengo, cachorro")
    print()

    print(f"  {C.YELLOW}[ ANOS ]{C.RESET}")
    current_year = datetime.now().year
    use_years = ask_bool("Incluir anos (1940 até hoje)?")
    year_start = 1940
    if use_years:
        y_input = ask("Ano inicial", "1940")
        if y_input and y_input.isdigit():
            year_start = int(y_input)
    print()

    print(f"  {C.YELLOW}[ MODO ]{C.RESET}")
    only_numeric = ask_bool("Gerar apenas números (PINs, datas)?")
    print()

    if not only_numeric:
        print(f"  {C.YELLOW}[ PERMUTAÇÕES ]{C.RESET}")
        use_leet    = ask_bool("Aplicar substituições leet (@, 3, 1, 0, $...)?")
        use_symbols = ask_bool("Adicionar símbolos e sufixos (!@#$%...)?")
        use_combos  = ask_bool("Combinar pares de palavras entre si?")
        print()

    print(f"  {C.YELLOW}[ COMPRIMENTO ]{C.RESET}")
    min_input = ask("Comprimento mínimo", "6")
    max_input = ask("Comprimento máximo", "20")
    min_len = int(min_input) if min_input and min_input.isdigit() else 6
    max_len = int(max_input) if max_input and max_input.isdigit() else 20
    print()

    print(f"  {C.YELLOW}[ SAÍDA ]{C.RESET}")
    out_name = ask("Nome do arquivo de saída (sem .txt)", "wordlist")
    out_file = (out_name if out_name else "wordlist") + ".txt"
    print()

    # ── Geração ───────────────────────────────────────────────────────────
    sep()
    print(f"\n  {C.GRAY}[*] Gerando wordlist...{C.RESET}\n")

    years = gen_years(year_start, current_year) if use_years else []
    wordlist: set = set()

    if only_numeric:
        wordlist |= gen_numeric(years, use_years, min_len, max_len)
    else:
        # Permutações por palavra
        for w in words:
            wordlist |= permutate_word(
                w, years, use_years, use_leet, use_symbols, min_len, max_len
            )

        # Combinações de pares
        if use_combos and len(words) >= 2:
            wordlist |= combine_words(words, years, use_years, use_symbols, min_len, max_len)

        # Anos sozinhos como palavras
        if use_years:
            for y in years:
                if min_len <= len(y) <= max_len:
                    wordlist.add(y)
                if use_symbols:
                    for suf in ["!", "@", "#", "!"]:
                        w = y + suf
                        if min_len <= len(w) <= max_len:
                            wordlist.add(w)

    # Filtro final de comprimento (garantia)
    wordlist = {w for w in wordlist if min_len <= len(w) <= max_len}

    # ── Escrita ───────────────────────────────────────────────────────────
    with open(out_file, "w", encoding="utf-8") as f:
        for entry in sorted(wordlist):
            f.write(entry + "\n")

    sep()
    print(f"\n  {C.GREEN}{C.BOLD}[✓] Wordlist gerada com sucesso!{C.RESET}")
    print(f"  {C.GRAY}Arquivo  {C.RESET}: {C.WHITE}{out_file}{C.RESET}")
    print(f"  {C.GRAY}Entradas {C.RESET}: {C.GREEN}{len(wordlist):,}{C.RESET}")
    print(f"  {C.GRAY}Tamanho  {C.RESET}: {C.WHITE}{os.path.getsize(out_file) / 1024:.1f} KB{C.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}[!] Interrompido.{C.RESET}\n")
        sys.exit(0)
