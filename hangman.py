"""
╔══════════════════════════════════════════════════════════╗
║           H A N G M A N   —   Python Edition             ║
║          Advanced Console Game  |  Blue Theme            ║
╚══════════════════════════════════════════════════════════╝
"""

import random
import os
import time

# ── ANSI Color Codes (Blue Theme) ────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# Blues
B_DARK  = "\033[34m"       # Dark Blue
B_MED   = "\033[94m"       # Bright Blue
B_LIGHT = "\033[96m"       # Cyan/Light Blue

# Accents
WHITE   = "\033[97m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
GREEN   = "\033[92m"
GRAY    = "\033[90m"

# ── Word Bank ─────────────────────────────────────────────
WORD_BANK = [
    {"word": "python",    "hint": "A popular programming language 🐍"},
    {"word": "galaxy",    "hint": "A massive system of stars in space 🌌"},
    {"word": "rhythm",    "hint": "A strong regular beat in music 🎵"},
    {"word": "quantum",   "hint": "Related to the smallest discrete unit of energy ⚛️"},
    {"word": "zephyr",    "hint": "A soft gentle breeze 🌬️"},
    {"word": "labyrinth", "hint": "A complicated network of passages 🌀"},
    {"word": "eclipse",   "hint": "When one celestial body blocks another 🌑"},
    {"word": "matrix",    "hint": "A rectangular array of numbers or symbols 🔢"},
    {"word": "phantom",   "hint": "A ghost or apparition 👻"},
    {"word": "crystal",   "hint": "A solid material with a highly ordered structure 💎"},
]

MAX_WRONG = 6

# ── Hangman ASCII Art Stages ──────────────────────────────
HANGMAN_STAGES = [
    # Stage 0 — Empty gallows
    f"""{B_DARK}
   ┌──────┐
   │      │
   │
   │
   │
   │
═══╧═══════{RESET}""",

    # Stage 1 — Head
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {B_MED}( ){B_DARK}
   │
   │
   │
═══╧═══════{RESET}""",

    # Stage 2 — Head + Body
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {B_MED}( ){B_DARK}
   │     {B_MED}│{B_DARK}
   │
   │
═══╧═══════{RESET}""",

    # Stage 3 — Head + Body + Left Arm
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {B_MED}( ){B_DARK}
   │    {B_MED}/│{B_DARK}
   │
   │
═══╧═══════{RESET}""",

    # Stage 4 — Head + Body + Both Arms
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {B_MED}( ){B_DARK}
   │    {B_MED}/│\\{B_DARK}
   │
   │
═══╧═══════{RESET}""",

    # Stage 5 — Head + Body + Arms + Left Leg
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {RED}( ){B_DARK}
   │    {RED}/│\\{B_DARK}
   │    {RED}/{B_DARK}
   │
═══╧═══════{RESET}""",

    # Stage 6 — Full Hangman (DEAD)
    f"""{B_DARK}
   ┌──────┐
   │      │
   │    {RED}(x){B_DARK}
   │    {RED}/│\\{B_DARK}
   │    {RED}/ \\{B_DARK}
   │
═══╧═══════{RESET}""",
]

# ── Utility Functions ─────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    """Print text character by character for dramatic effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def print_banner():
    banner = f"""
{B_MED}╔══════════════════════════════════════════════════════╗
║                                                      ║
║   {WHITE}{BOLD}  H ── A ── N ── G ── M ── A ── N  {RESET}{B_MED}                ║
║                                                      ║
║   {B_LIGHT}  Guess the word. Save the figure. Beat the game.{B_MED}  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def print_divider(char="─", width=54):
    print(f"{B_DARK}{char * width}{RESET}")

def display_word(word, guessed_letters):
    """Show word with correctly guessed letters revealed."""
    display = ""
    for i, letter in enumerate(word):
        if letter in guessed_letters:
            display += f"{GREEN}{BOLD}{letter}{RESET}"
        else:
            display += f"{B_MED}_{RESET}"
        if i < len(word) - 1:
            display += "  "
    return display

def display_guessed(guessed_letters):
    """Show all guessed letters, colored by correctness."""
    if not guessed_letters:
        return f"{GRAY}None yet{RESET}"
    return "  ".join([f"{B_LIGHT}{BOLD}{l.upper()}{RESET}" for l in sorted(guessed_letters)])

def display_wrong(wrong_letters):
    """Show wrong letters in red."""
    if not wrong_letters:
        return f"{GRAY}None yet{RESET}"
    return "  ".join([f"{RED}{BOLD}{l.upper()}{RESET}" for l in sorted(wrong_letters)])

def choose_difficulty():
    """Let the player pick difficulty."""
    print(f"\n{B_MED}  Select Difficulty:{RESET}")
    print(f"  {B_LIGHT}[1]{RESET} Easy    — Hints shown, longer words only")
    print(f"  {B_LIGHT}[2]{RESET} Normal  — Hint on request")
    print(f"  {B_LIGHT}[3]{RESET} Hard    — No hints, shorter time to think\n")

    while True:
        choice = input(f"  {B_LIGHT}›{RESET} Enter choice (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print(f"  {RED}Please enter 1, 2, or 3.{RESET}")

def render_game_screen(word, guessed_letters, wrong_letters, hint, difficulty, score):
    """Render the full game screen."""
    clear_screen()
    print_banner()

    wrong_count = len(wrong_letters)
    lives_left   = MAX_WRONG - wrong_count

    # ── Left: Hangman + Stats ──
    print(HANGMAN_STAGES[wrong_count])
    print_divider()

    # Lives bar
    life_bar = f"{GREEN}{'♥ ' * lives_left}{RESET}{RED}{'♡ ' * wrong_count}{RESET}"
    print(f"  Lives: {life_bar}   {B_LIGHT}Score: {YELLOW}{score}{RESET}")
    print_divider()

    # Word display
    print(f"\n  Word:  {display_word(word, guessed_letters)}")
    print(f"         {B_DARK}({len(word)} letters){RESET}\n")

    # Hint
    if difficulty == 1:
        print(f"  {B_LIGHT}Hint ►{RESET}  {hint}")
    elif difficulty == 2:
        print(f"  {GRAY}Type '?' during guessing to reveal hint (−5 pts){RESET}")
    else:
        print(f"  {GRAY}Hard mode — no hints!{RESET}")

    print_divider()

    # Letters
    print(f"  {B_LIGHT}Correct:{RESET}  {display_guessed(guessed_letters - set(c for c in guessed_letters if c not in word))}")
    print(f"  {RED}Wrong:{RESET}    {display_wrong(wrong_letters)}")
    print_divider()

def get_player_guess(guessed_all, difficulty, hint_used):
    """Get a valid single letter from the player."""
    while True:
        raw = input(f"\n  {B_LIGHT}›{RESET} Guess a letter: ").strip().lower()

        if raw == "?" and difficulty == 2 and not hint_used:
            return "?"
        if raw == "quit":
            return "quit"
        if len(raw) != 1:
            print(f"  {RED}Please enter a single letter.{RESET}")
            continue
        if not raw.isalpha():
            print(f"  {RED}Only alphabetic characters allowed.{RESET}")
            continue
        if raw in guessed_all:
            print(f"  {YELLOW}You already guessed '{raw.upper()}'. Try a different letter!{RESET}")
            continue
        return raw

def calculate_score(word_len, wrong_count, difficulty, hint_used):
    """Calculate score for this round."""
    base        = word_len * 10
    wrong_pen   = wrong_count * 5
    hint_pen    = 5 if hint_used else 0
    diff_bonus  = {1: 0, 2: 10, 3: 25}[difficulty]
    return max(0, base - wrong_pen - hint_pen + diff_bonus)

def play_round(difficulty, total_score):
    """Play a single round. Returns updated score."""
    entry   = random.choice(WORD_BANK)
    word    = entry["word"]
    hint    = entry["hint"]

    guessed_letters = set()   # all letters guessed
    wrong_letters   = set()   # incorrect guesses only
    hint_used       = False

    while True:
        # Show wrong letters too in the right guessed set
        render_game_screen(word, guessed_letters, wrong_letters, hint, difficulty, total_score)

        # Win / Lose check
        if all(l in guessed_letters for l in word):
            pts = calculate_score(len(word), len(wrong_letters), difficulty, hint_used)
            total_score += pts
            clear_screen()
            print_banner()
            print(HANGMAN_STAGES[len(wrong_letters)])
            slow_print(f"\n  {GREEN}{BOLD}🎉  You saved the figure!{RESET}", delay=0.04)
            slow_print(f"  {B_LIGHT}The word was: {WHITE}{BOLD}{word.upper()}{RESET}", delay=0.04)
            slow_print(f"  {YELLOW}+{pts} points  →  Total: {total_score}{RESET}", delay=0.04)
            return total_score, True

        if len(wrong_letters) >= MAX_WRONG:
            clear_screen()
            print_banner()
            print(HANGMAN_STAGES[MAX_WRONG])
            slow_print(f"\n  {RED}{BOLD}💀  The figure has fallen!{RESET}", delay=0.04)
            slow_print(f"  {B_LIGHT}The word was: {WHITE}{BOLD}{word.upper()}{RESET}", delay=0.04)
            slow_print(f"  {GRAY}No points this round.{RESET}", delay=0.04)
            return total_score, False

        guess = get_player_guess(guessed_letters | wrong_letters, difficulty, hint_used)

        if guess == "quit":
            slow_print(f"\n  {YELLOW}Quitting round...{RESET}")
            return total_score, False

        if guess == "?":
            hint_used = True
            print(f"\n  {B_LIGHT}Hint ►{RESET}  {hint}  {RED}(−5 pts){RESET}")
            time.sleep(2)
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"\n  {GREEN}✔  '{guess.upper()}' is in the word!{RESET}")
            time.sleep(0.8)
        else:
            wrong_letters.add(guess)
            print(f"\n  {RED}✘  '{guess.upper()}' is NOT in the word!{RESET}")
            time.sleep(0.8)

def show_final_score(score, wins, rounds):
    """Show end-game summary."""
    clear_screen()
    print_banner()
    print_divider("═")
    print(f"\n  {B_MED}{BOLD}  GAME OVER — Final Summary{RESET}")
    print_divider()
    print(f"  {B_LIGHT}Rounds played:{RESET}  {rounds}")
    print(f"  {GREEN}Rounds won:{RESET}     {wins}")
    print(f"  {RED}Rounds lost:{RESET}    {rounds - wins}")
    print(f"  {YELLOW}Total score:{RESET}    {score}")
    print_divider("═")

    # Star rating
    if rounds > 0:
        ratio = wins / rounds
        if ratio == 1.0:
            rating = f"{YELLOW}★★★★★  Perfect!{RESET}"
        elif ratio >= 0.75:
            rating = f"{YELLOW}★★★★☆  Excellent!{RESET}"
        elif ratio >= 0.5:
            rating = f"{YELLOW}★★★☆☆  Good game!{RESET}"
        else:
            rating = f"{YELLOW}★★☆☆☆  Keep practising!{RESET}"
        print(f"\n  {rating}\n")

# ── Main Entry Point ──────────────────────────────────────

def main():
    clear_screen()
    print_banner()
    slow_print(f"  {B_LIGHT}Welcome to Hangman — the word-guessing challenge!{RESET}", 0.03)
    time.sleep(0.5)

    difficulty  = choose_difficulty()
    total_score = 0
    wins        = 0
    rounds      = 0

    while True:
        total_score, won = play_round(difficulty, total_score)
        rounds += 1
        if won:
            wins += 1

        print()
        print_divider()
        again = input(f"  {B_LIGHT}›{RESET} Play another round? (y/n): ").strip().lower()
        if again != "y":
            break

    show_final_score(total_score, wins, rounds)
    slow_print(f"\n  {B_MED}Thanks for playing! See you next time. 👋{RESET}\n", 0.04)


if __name__ == "__main__":
    main()