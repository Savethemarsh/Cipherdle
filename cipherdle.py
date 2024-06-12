import random
import string
import os
from datetime import datetime, timedelta, date

def clear_console():
    # Clear console screen for Windows
    if os.name == 'nt':
        _ = os.system('cls')

    # Clear console screen for Unix/Linux/MacOS
    else:
        _ = os.system('clear')

def read_words_from_file(file_path):
    words_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespaces, and add the word to the list
            word = line.strip()
            words_list.append(word)
    return words_list

def generate_cipher(seed):
    random.seed(seed)
    cipher = {}
    plainAlphabet = list(string.ascii_lowercase)
    cipherAlphabet = list(string.ascii_lowercase)
    for letterChoice in plainAlphabet:
        cipherChoice = random.choice(cipherAlphabet)
        cipherAlphabet.remove(cipherChoice)
        cipher[letterChoice] = cipherChoice
    return cipher

def generate_word(seed):
    random.seed(seed)
    return random.choice(puzzleWords)

def print_cipher_nicely(cipher):
    for letter, cipher in cipher.items():
        if letter in greenLetters:
            print(colors.GREEN + f"{letter}: {cipher}" + colors.RESET)
        elif letter in yellowLetters:
            print(colors.YELLOW + f"{letter}: {cipher}" + colors.RESET)
        elif letter in grayLetters:
            print(colors.GRAY + f"{letter}: {cipher}" + colors.RESET)
        else:
            print(f"{letter}: {cipher}" )    

def is_guess_valid(guess):
    return guess in guessableWords

def guess_print(guess, answer, spoiler): # THIS IS THE WORST FUNCTION I HAVE EVER WRITTEN
    green = []
    yellow = []
    yellowTwo = []
    for n in range(wordSize):
        if cipher[guess[n]] == answer[n]:
            green.append(n)
    for n in range(wordSize):
        for m in range(wordSize):
            if cipher[guess[n]] == answer[m] and not n in green and not m in green and not n in yellow and not m in yellowTwo:
                yellow.append(n)
                yellowTwo.append(m)
    for n in range(wordSize):
        if n in green:
            print(colors.GREEN + guess[n] + colors.RESET, end="") if not spoiler else print(colors.GREEN + "🟩" + colors.RESET, end="")
            greenLetters.append(guess[n])
        elif n in yellow:
            print(colors.YELLOW + guess[n] + colors.RESET, end="") if not spoiler else print(colors.YELLOW + "🟨" + colors.RESET, end="")
            yellowLetters.append(guess[n])            
        else:
            print(guess[n], end="") if not spoiler else print("⬜", end="")
            grayLetters.append(guess[n])   
    print("")
    
def print_board():
    if not len(guessHistory) == 0:
        print("Your guess history is:")
        for guess in guessHistory:
            guess_print(guess, puzzleWord, False)   
    clear_console()
    # print("The answer is " + puzzleWord)
    print("Your cipher is:")
    print_cipher_nicely(cipher)
    if not len(guessHistory) == 0:
        print("Your guess history is:")
        for guess in guessHistory:
            guess_print(guess, puzzleWord, False)        
            
def reset_game(): # This function is pretty bad too
    global grayLetters
    global yellowLetters
    global greenLetters
    global lives   
    global gameRunning 
    global guessHistory
    global dailyGame
    grayLetters = []
    yellowLetters = []
    greenLetters = []
    lives = 7   
    gameRunning = True
    guessHistory = []  
    dailyGame = False    

   
def get_daily_seed(current_date):
    epoch_date = date(1970, 1, 1)
    difference = current_date - epoch_date
    # print(difference)
    return difference.days
    
def spoiler_guess_history_print():
    for guess in guessHistory:
        guess_print(guess, puzzleWord, True)
        

class colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'


gameRunning = False
guessValid = True
programRunning = True
dailyGame = False
wordSize = 5
lives = 7
guessableWords = read_words_from_file("guessablewords.txt")
puzzleWords = read_words_from_file("puzzleWords.txt")
grayLetters = []
yellowLetters = []
greenLetters = []
puzzleWord = generate_word(1)
cipher = generate_cipher(1)
print_cipher_nicely(cipher)
guessHistory = []

clear_console()
while(programRunning):
    if gameRunning == False:
        userInput = input("Type \"exit\" to exit, type 1 to play the daily game, type 2 to free-play:")
        if userInput == "exit":
            programRunning = False
        elif userInput == "1":
            current_date = datetime.now().date()
            seed = get_daily_seed(current_date)
            puzzleWord = generate_word(seed)
            cipher = generate_cipher(seed)   
            reset_game()
            dailyGame = True
        elif userInput == "2": 
            puzzleWord = generate_word(random.random())
            cipher = generate_cipher(random.random())
            reset_game()
    while(gameRunning):
        print_board()
        if not guessValid:
            print("invalid guess!")
        user_input = input(f"You have {lives} guesses left."+" Type your guess (or type \"exit\" to quit):\n" )
        if user_input == "exit": 
            gameRunning = False
            programRunning = True
            break
        if is_guess_valid(user_input):
            guessValid = True
            guessHistory.append(user_input)
            lives = lives - 1
            print_board()
            if user_input == puzzleWord:
                print("YOU WIN! The word was " + puzzleWord)
                if dailyGame:
                    print("Cipherdle", current_date.strftime("%Y-%m-%d"))
                    spoiler_guess_history_print()
                gameRunning = False
            elif lives == 0:
                print("GAME OVER! The words was " + puzzleWord)
                gameRunning = False
        else:
            guessValid = False
        
