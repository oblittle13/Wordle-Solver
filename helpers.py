# Importing possible Wordle answers
with open('answers.txt', 'r') as file:
    content = file.read()

content_cleaned = content.strip().strip("[]").replace('"', '')
wordle_list = content_cleaned.split(",")
wordle_list = [word.strip() for word in wordle_list]

# Importing possible guesses
with open('words.txt', 'r') as file:
    content = file.readlines()
    guess_list = [line.strip() for line in content]
    

# 2D list containing the QWERTY keyboard in order
keyboard = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
]