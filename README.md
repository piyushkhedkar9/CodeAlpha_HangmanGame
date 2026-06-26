This project is a simplified yet polished implementation of the classic word-guessing game Hangman. The player guesses letters one at a time to reveal a hidden word before running out of attempts. The game is built entirely with Python's standard library — no external packages, files, or APIs required.


✨ Features


🎨 Blue-themed console UI using ANSI escape codes
🪢 7-stage ASCII hangman that animates as wrong guesses pile up
📊 Scoring system — points based on word length, wrong guesses, and difficulty
🎯 3 difficulty levels — Easy (hint shown), Normal (hint costs points), Hard (no hints)
❤️ Lives bar with heart icons showing remaining attempts
🔁 Replay loop — play multiple rounds with a running score
⭐ Star rating summary at the end based on your win rate
📚 10 predefined words with hints, no file or API needed



🧠 Key Concepts Used

ConceptWhere it's usedrandomPicking a random word from the word bank each roundwhile loopsMain guessing loop, replay loopif-elseWin/loss checks, input validation, difficulty branchingStringsWord display, formatting, ANSI color codesLists / SetsWord bank, tracking guessed and wrong letters


🖥️ Requirements


Python 3.6 or higher
No external libraries — uses only random, os, and time from the standard library


Check your Python version:

bashpython --version


🚀 How to Run

1. Clone or download this repository

bashgit clone https://github.com/YOUR_USERNAME/hangman-game.git
cd hangman-game

2. Run the game

bashpython hangman.py

(On macOS/Linux you may need python3 hangman.py instead.)

3. Play!


Pick a difficulty (Easy / Normal / Hard)
Guess one letter at a time
You have 6 incorrect guesses before the game ends
Type ? during Normal mode to reveal a hint (costs 5 points)
Type quit anytime to exit the current round



💡 Windows users: if colors appear as garbled text, use Windows Terminal instead of the classic Command Prompt, or run chcp 65001 first.




🎯 How to Play


A secret word is chosen at random from the word bank.
You see blank spaces representing each letter of the word.
Guess a letter — if it's correct, it's revealed in the word. If wrong, a part of the hangman is drawn and you lose a life.
Win by revealing the whole word before making 6 wrong guesses.
Lose if the hangman is fully drawn before you guess the word.
Play multiple rounds — your score accumulates across the session!



📋 Word Bank

The game includes 10 predefined words, each with a hint:

WordHintpythonA popular programming languagegalaxyA massive system of stars in spacerhythmA strong regular beat in musicquantumRelated to the smallest discrete unit of energyzephyrA soft gentle breezelabyrinthA complicated network of passageseclipseWhen one celestial body blocks anothermatrixA rectangular array of numbers or symbolsphantomA ghost or apparitioncrystalA solid material with a highly ordered structure


🧩 Scoring System

Score = (word length × 10) − (wrong guesses × 5) − (5 if hint used) + difficulty bonus

DifficultyBonusHintsEasy+0Always shownNormal+10Available on request (−5 pts)Hard+25Not available


📁 Project Structure

hangman-game/
│
├── hangman.py       # Main game file — all logic, UI, and word bank
└── README.md        # This file


🛠️ Customization Ideas

Want to extend the game? Here are a few easy additions:


Add more words to the WORD_BANK list in hangman.py
Group words into categories (animals, tech, geography, etc.)
Add a timer per guess for extra challenge
Save high scores to a local text file
Add sound effects using the playsound or pygame library



📝 License

This project is open source and available under the MIT License. Feel free to use, modify, and share it.


🙌 Acknowledgements

Built as a learning project to practice Python fundamentals: control flow, string manipulation, randomization, and basic terminal UI design.
