import string
import random

# Importing possible Wordle answers
with open('answers.txt', 'r') as file:
    content = file.read()

content_cleaned = content.strip().strip("[]").replace('"', '')
wordle_list = content_cleaned.split(",")
wordle_list = [word.strip() for word in wordle_list]

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
      
    # Function that moves guessed letters over from unguessed list  
    def guessLetter(self, letter): # VALIDATED
        # Ensure letter exists in unguessed letters
        if letter in self.unguessed_letters:
            # Move guessed letter over from unguessed list
            self.guessed_letters.append(letter)
            self.unguessed_letters.remove(letter)
      
    # Filters out words from possible list with letter  
    def filterOutLetter(self, letter): # VALIDATED
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it does not contain the invalid letter, add it
        for word in self.possible_words:
            if letter not in word:
                temp_list.append(word)
                
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
        
    # Updates green letters with newly determined green letter
    def updateGreen(self, letter, position): # VALIDATED
        self.green_letters.update({position : letter})
        
    # Updates yellow letters with newly determined yellow letter
    def updateYellow(self, letter, position): # VALIDATED
        self.yellow_letters.update({position : letter})
        
    # Determines if target word contains letter as green
    def isLetterGreen(self, letter, position): # VALIDATED
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
    def isLetterYellow(self, letter, position): # VALIDATED
        # If letter is in target word, not at the same position, and not a green letter return true
        if (letter in self.target_word) and (self.target_word[position] != letter) and (letter not in self.green_letters.values()):
            return True
        # Otherwise return false
        else:
            return False
    
    # Filters out words without green letters
    def filterOutGreen(self, letter, position): # VALIDATED
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it contains letter at position, add it
        for word in self.possible_words:
            if word[position] == letter:
                temp_list.append(word)
                
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
    
    # Filters out words without yellow letters
    def filterOutYellow(self, letter, position): # VALIDATED
        # Temp list to store valid words
        temp_list = []
        
        # For loop through possible words, if it contains letter not at position, and letter at position isn't already green, add it
        for word in self.possible_words:
            if (letter in word) and (word[position] != letter):
                temp_list.append(word)
        
        # Set temp_list to be the new possible word list
        self.possible_words = temp_list
        
    # Picks a word at random from the possible list
    def guessWord(self): # VALIDATED
        if len(self.possible_words) == 0:
            self.game_finished = True
            return
        else:
            self.guess_count += 1
            self.current_guess = [letter for letter in random.choice(self.possible_words)]
        
    # Clears green and yellow lists
    def clear(self):
        self.yellow_letters = dict()
        self.green_letters = dict()
        
    # Determins if the game is finished    
    def isFinished(self):
        if (len(self.green_letters) == 5) or (self.guess_count == 5):
            self.game_finished = True
    
    # GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    # END = '\033[0m'
    # Displays guessed to the command line
    def display(self):
        for letter in self.current_guess:
            if letter in self.green_letters.values():
                print('\033[92m' + letter + '\033[0m', end=' ')
            elif letter in self.yellow_letters.values():
                print('\033[93m' + letter + '\033[0m', end=' ')
            else:
                print(f"{letter} ", end='')
        print('\n')
    
    def gameLoop(self):
        # While condition indicating game hasn't been won yet
        while not self.game_finished:
            # Clear yellow and green lists
            self.clear()
            
            # Guess a new word
            self.guessWord()

            # For loop for each letter in the guess
            for position in range(len(self.current_guess)):
                # Guess the letter, remove it from unguessed list
                self.guessLetter(self.current_guess[position])

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
            self.display()
            
            # Check win condition
            self.isFinished()
        
        # Check win/loss condition
        if len(self.green_letters) == 5:
            print(f"Congradulations! You have won!")
            print("The word was: " + '\033[92m' + self.target_word + '\033[0m' + f" and you got it in {self.guess_count} guesses!")
        else:
            print(f"Unfortunetly, you have lost.")
            print("The word was " + '\033[91m' + self.target_word + '\033[0m' + " Please try again!")
             
# Main    
def main():
    target_word = random.choice(wordle_list)
    game = Wordle(wordle_list, "pizza")
    
    game.gameLoop()
       
if __name__ == '__main__':
    main()
            