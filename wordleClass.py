import random
import os
import string
from helpers import keyboard, guess_list, wordle_list

class Wordle:
    # Init of wordle object
    def __init__(self, word_list, target_word):
        # Target word
        self.target_word = target_word
        
        # List of guessed letters
        self.guessed_letters = []
        
        # List of unguessed letters
        self.unguessed_letters = list(string.ascii_lowercase)
        
        # List of possible words remaining
        self.possible_words = list(word_list)
        
        # Dictionary containing the (position, letter) of green letters
        self.green_letters = dict()
        
        # Dictionary containing the (position, letter) of yellow letters
        self.yellow_letters = dict()
        
        # Dictionary containing current guess
        self.current_guess = []
        
        # Holds the number of words guessed in the game
        self.guess_count = 0
        
        # Bool holding if game has been finished
        self.game_finished = False
        
        # List of all user guesses, and the letter colours
        self.user_guesses = []
        
    # Function that moves guessed letters over from unguessed list  
    def guessLetter(self, letter): 
        # Ensure letter exists in unguessed letters, and isn't a green or yellow letter
        if (letter in self.unguessed_letters) and ((letter not in self.green_letters) or (letter not in self.yellow_letters)):
            # Move guessed letter over from unguessed list
            self.guessed_letters.append(letter)
            self.unguessed_letters.remove(letter)
            
    # Picks a word at random from the possible list
    def guessWord(self): 
        if len(self.possible_words) == 0:
            self.game_finished = True
            return
        else:
            self.guess_count += 1
            self.current_guess = [letter for letter in random.choice(self.possible_words)]
            
    # Filters out words from possible list with letter  
    def filterOutLetter(self, letter): 
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it does not contain the invalid letter, add it
        for word in self.possible_words:
            if letter not in word:
                temp_list.append(word)
                
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
    
    # Filters out words without green letters
    def filterOutGreen(self, letter, position): 
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it contains letter at position, add it
        for word in self.possible_words:
            if word[position] == letter:
                temp_list.append(word)
                
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
    
    # Filters out words without yellow letters
    def filterOutYellow(self, letter, position): 
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it contains letter not at position, and letter at position isn't already green, add it
        for word in self.possible_words:
            if (letter in word) and (word[position] != letter):
                temp_list.append(word)
        
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
        
    # Determines if target word contains letter as green
    def isLetterGreen(self, letter, position): 
        # If letter is in target word, at the same position return true
        if (letter in self.target_word) and (self.target_word[position] == letter):
            # Determines if a yellow letter has been guessed as green, if so, remove it from yellow list
            if letter in self.yellow_letters.values():
                for key, value in self.yellow_letters.items():
                    if value == letter:
                        del self.yellow_letters[key]
                        break
            return True
        # Otherwise return false
        else:
            return False
        
    # Determines if target word contains letter as yellow
    def isLetterYellow(self, letter, position): 
        # If letter is in target word, not at the same position, and not a green letter return true
        if (letter in self.target_word) and (self.target_word[position] != letter) and (letter not in self.green_letters.values()):
            return True
        # Otherwise return false
        else:
            return False
        
    # Updates green letters with newly determined green letter
    def updateGreen(self, letter, position): 
        self.green_letters.update({position : letter})
        
    # Updates yellow letters with newly determined yellow letter
    def updateYellow(self, letter, position): 
        self.yellow_letters.update({position : letter})
        
    # Clears green and yellow lists
    def clear(self):
        self.yellow_letters = dict()
        self.green_letters = dict()
        
    # Determins if the game is finished - 5 green letters or a guess count of 5
    def isFinished(self):
        if (len(self.green_letters) == 5) or (self.guess_count == 5):
            self.game_finished = True
            
    # Displays guessed to the command line
    def display(self, word):
        for letter in word:
            if letter in self.green_letters.values():
                print('\033[92m' + letter + '\033[0m', end=' ')
            elif letter in self.yellow_letters.values():
                print('\033[93m' + letter + '\033[0m', end=' ')
            else:
                print(f"{letter} ", end='')
        print('\n')
        
    def displayUser(self):
        # Clear the screen
        self.clearScreen()
        
        # Display current board
        print("Current Wordle Board:")
        print("---------------------")
        for word in self.user_guesses:
            self.display(word)
        
        #Display remaining letters, coloured and formatted
        print("Letters remaining:")
        print("---------------------")
        for row in keyboard:
            for letter in row:
                # Green letter
                if letter in self.green_letters.values():
                    print('\033[92m' + letter + '\033[0m', end=' ')
                # Yellow letter
                elif letter in self.yellow_letters.values():
                    print('\033[93m' + letter + '\033[0m', end=' ')
                # Guessed letter not in word
                elif letter in self.guessed_letters:
                    print('\033[91m' + letter + '\033[0m', end=' ')
                # Unused letter
                else:
                    print(letter, end=' ')
            print('\n')
            
    # Function that clears the command line
    def clearScreen(self):
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For Unix/Linux/MacOS
        else:
            os.system('clear')
            
    # Gets user input
    def getUserInput(self):
        self.current_guess = input("Enter word: ")
        
    # Promt user if they want to play, or have the computer solve
    def userOrSolver(self):
        user_input = input("Please select one of the following: \n 1) I want to play \n 2) I want the computer to solve \n 3) Exit \nPress 1, 2 or 3.\n")
        return user_input
    
    # Function that logs user guess
    def logInput(self):
        self.user_guesses.append(self.current_guess)
        
    # Increment guess count by 1
    def incrementGuess(self):
        self.guess_count += 1
        
    # Determines if guess is valid or not
    def isValidGuess(self):
        if self.current_guess not in self.possible_words:
            return False
        
    # Main game loop
    def gameLoop(self):
        # While condition indicating game hasn't been won yet
        while not self.game_finished:
            # Clear yellow and green lists
            self.clear()
            
            # Guess a new word
            self.guessWord()

            # For loop for each letter in the guess
            for position in range(len(self.current_guess)):
                # If letter is green, update it in the list
                if self.isLetterGreen(self.current_guess[position], position):
                    self.updateGreen(self.current_guess[position], position)
                    self.filterOutGreen(self.current_guess[position], position)

                # Elif letter is yellow, update it in the list
                elif self.isLetterYellow(self.current_guess[position], position):
                    self.updateYellow(self.current_guess[position], position)
                    self.filterOutYellow(self.current_guess[position], position)

                # Else, letter is not in target, remove it from possible list
                # Elif condition protects against removing letters that have a green letter position already
                elif (self.current_guess[position] not in self.target_word):
                    self.filterOutLetter(self.current_guess[position]) 
            # Visually display guess
            self.display(self.current_guess)
            
            # Check win condition
            self.isFinished()
        
        # Check win/loss condition
        if len(self.green_letters) == 5:
            print(f"Congradulations! You have won!")
            print("The word was: " + '\033[92m' + self.target_word + '\033[0m' + f" and you got it in {self.guess_count} guesses!")
        else:
            print(f"Unfortunetly, you have lost.")
            print("The word was " + '\033[91m' + self.target_word + '\033[0m' + " Please try again!")
        
    # Game loop for a user game, simulates doing the actual Wordle    
    def userGame(self):
        # Increase possible word list
        self.possible_words += guess_list

        # While condition indicating game hasn't been won yet
        while not self.game_finished:
            # Get input from user
            self.getUserInput()
            
            # If user enters a word not in the valid list, informs them, and reprompt them
            if self.isValidGuess() == False:
                print('\033[91m' + "Not a valid word." + '\033[0m')
                continue
            
            # Increment guess count and log input
            self.incrementGuess()
            self.logInput()
            
            # For loop for each letter in the guess
            # In a user game, we do not filter out the possible list
            for position in range(len(self.current_guess)):

                # If letter is green, update it in the list
                if self.isLetterGreen(self.current_guess[position], position):
                    self.updateGreen(self.current_guess[position], position)

                # Elif letter is yellow, update it in the list
                elif self.isLetterYellow(self.current_guess[position], position):
                    self.updateYellow(self.current_guess[position], position)
                    
                # Guess the letter, remove it from unguessed list, if required
                self.guessLetter(self.current_guess[position])
                    
            # Visually display guess
            self.displayUser()
            
            # Check win condition
            self.isFinished()
        
        # Check win/loss condition
        if len(self.green_letters) == 5:
            print(f"Congradulations! You have won!")
            print("The word was: " + '\033[92m' + self.target_word + '\033[0m' + f" and you got it in {self.guess_count} guesses!")
        else:
            print(f"Unfortunetly, you have lost.")
            print("The word was " + '\033[91m' + self.target_word + '\033[0m' + " Please try again!")
            