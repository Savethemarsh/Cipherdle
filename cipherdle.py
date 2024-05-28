import random
import string
import os

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

def generate_cipher():
    cipher = {}
    plainAlphabet = list(string.ascii_lowercase)
    cipherAlphabet = list(string.ascii_lowercase)
    for letterChoice in plainAlphabet:
        cipherChoice = random.choice(cipherAlphabet)
        cipherAlphabet.remove(cipherChoice)
        cipher[letterChoice] = cipherChoice
    return cipher

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

def guess_print(guess, answer):
    solvedLetters = []
    for n in range(wordSize):
        if cipher[guess[n]] == answer[n]:
            solvedLetters.append(n)
            print(colors.GREEN + guess[n] + colors.RESET, end="")
            greenLetters.append(guess[n])
        else:
            yellowPrint = False
            for m in range(wordSize):
                if cipher[guess[n]] == answer[m] and not m in solvedLetters:
                    solvedLetters.append(m)
                    yellowPrint = True
                    break
            if yellowPrint:
                print(colors.YELLOW + guess[n] + colors.RESET, end="")
                yellowLetters.append(guess[n])
            else:
                grayLetters.append(guess[n])
                print(guess[n], end="")
    print("")
    
def print_board():
    if not len(guessHistory) == 0:
        print("Your guess history is:")
        for guess in guessHistory:
            guess_print(guess, puzzleWord)   
    # print("The answer is " + puzzleWord)
    clear_console()
    print("Your cipher is:")
    print_cipher_nicely(cipher)
    if not len(guessHistory) == 0:
        print("Your guess history is:")
        for guess in guessHistory:
            guess_print(guess, puzzleWord)        

    
    
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


gameRunning = True
programRunning = True
wordSize = 5
lives = 6
guessableWords = read_words_from_file("guessablewords.txt")
puzzleWords = read_words_from_file("puzzleWords.txt")
puzzleWord = random.choice(puzzleWords)
grayLetters = []
yellowLetters = []
greenLetters = []
cipher = generate_cipher()
print_cipher_nicely(cipher)
guessHistory = []


while(programRunning):
    if gameRunning == False:
        if input("Type \"exit\" to exit, type anything else to play a new game:") == "exit":
            programRunning = False
        else: 
            gameRunning = True
            guessHistory = []  
            puzzleWord = random.choice(puzzleWords)
            cipher = generate_cipher()
            grayLetters = []
            yellowLetters = []
            greenLetters = []
            lives = 6
    while(gameRunning):
        print_board()
        user_input = input(f"You have {lives} guesses left."+" Type your guess (or type \"exit\" to quit):\n" )
        if user_input == "exit": 
            gameRunning = False
            programRunning = False
            break
        if is_guess_valid(user_input):
            guessHistory.append(user_input)
            lives = lives - 1
            if user_input == puzzleWord:
                print_board()
                print("YOU WIN! The word was " + puzzleWord)
                gameRunning = False
            elif lives == 0:
                print_board()
                print("GAME OVER! The words was " + puzzleWord)
                gameRunning = False
        else:
            print("invalid guess!")
        