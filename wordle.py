from wordleClass import *
              
# Main    
def main():
    while 1:
        # Init game
        target_word = random.choice(wordle_list)
        game = Wordle(wordle_list, target_word)
    
        # Get user choice
        choice = game.userOrSolver()
        if choice == '1':
            game.clearScreen()
            game.userGame()
        elif choice == '2':
            game.clearScreen()
            game.gameLoop()
        elif choice == '3':
            break
       
if __name__ == '__main__':
    main()
            