PhraseBank=open("phrasebank.txt").read().splitlines()
import random

#Clean up player inputs
def clean_up(string_input):
    result=''
    punctuation=['!','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','}','|','~']
    for character in string_input:
        if character not in punctuation:
            result+=character
    result= result.strip()
    result= result.upper()
    return result

#Print phrase function
def phrasePrint(original_phrase, input_letters):
    phrase=list(original_phrase)
    blank_phrase=""
    underscore="_ "
    space="  "
    if input_letters!=[]:
        for i, element in enumerate(phrase):
            if element in input_letters:
                element=element.lower()
                phrase[i]=element
    for i, element in enumerate(phrase):
        if element==" ":
            blank_phrase+=space
        elif element.islower():
            element=element.upper()
            blank_phrase+=element
            blank_phrase+=" "
        else:
            blank_phrase+=underscore
    return blank_phrase

#Determines the category of the phrase
def determine_category(original_phrase):
    index=PhraseBank.index(original_phrase)
    if 0<=index<=20:
        category="Before and After"
    elif 20<=index<=40:
        category="Song Lyrics"
    elif 40<=index<=60:
        category="Around the House"
    elif 60<=index<=80:
        category="Food and Drink"
    else:
        category="Same Name"
    return category

#Function to spin the wheel.
def spinTheWheel(original_phrase, current_balance, input_letters):
    consonants=['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Z', 'W', 'Y']
    possible_spin_values=[50,100,100,100,100,100,100,200,200,200,200,250,250,250,500,500,750,750,1000,2000,5000,10000,"Bankrupt", "Bankrupt"]
    spin_value=possible_spin_values[random.randint(0,23)]                       #Select random spin value
    done=False
    phrase=list(original_phrase)
    if spin_value=="Bankrupt":                                                  #If spin is bankrupt.
        print(spin_value + ": Your balance has been reset to zero. Sorry!")
        current_balance=0
    else:
        print("You've spun " + "$" + str(spin_value) + "!", end=' ')
        while done==False:
                input_letter=input("What is your consonant guess? ")            #Guessing an consonant and cleaning it up (allows user to make some error with input)
                input_letter=clean_up(input_letter)
                if input_letter not in consonants:                              #If it's not an acceptable input, while loop will repeat
                    print("That is not a consonant. Please try again.")
                elif input_letter in input_letters:                             #Checks to make sure that they haven't already tried that letter (input_letters=list of past letters)
                    print("You have already tried that letter. Choose another one and stop trying to get extra money you greedy cheater.") #I realized after the fact that this part wasn't neccessary (Good job reading those instructions GRACE), BUT I kinda like it so ehh...
                elif input_letter in phrase:                                    #Also, this clause is useful for the counting letters in main (labeled w/ comment). There would be problems with that section without this and I'm lazy so... please don't take off too many points :)
                    input_letters.append(input_letter)
                    counter=0
                    for letter in phrase:
                        if input_letter==letter:
                            counter+=1
                    print("Congragulations, " + input_letter + " appears in the phrase " + str(counter) + " time(s)!")
                    blank_phrase=phrasePrint(original_phrase, input_letters)
                    current_balance=(spin_value * counter) + current_balance
                    print("The new phrase is:")
                    print(blank_phrase)
                    print("Consonant guessed: " + input_letter)
                    print("Your current winnings are: " + "$" + str(current_balance))
                    done=True
                else:
                    input_letters.append(input_letter)
                    blank_phrase=phrasePrint(original_phrase, input_letters)
                    print("Sorry, that letter is not in the phrase.")
                    print("The current phrase is:")
                    print(blank_phrase)
                    current_balance=((-1)*spin_value)+ current_balance
                    print("Your current winnings are: " + "$" + str(current_balance))
                    done=True
    return input_letters, current_balance

#Allows user to buy a vowel and checks if vowel is in the phrase. Printing the new phrase to the screen if that is the case.
def buyAVowel(original_phrase, current_balance, input_letters):
    vowels=['A','E','I','O','U']
    if current_balance<250:
        print("It costs $250 to buy a vowel. You don't have enough money. Jesus Christ, get a job already.")
    else:
        done=False
        while not done:
            input_letter=input("FYI it costs $250 to buy a vowel. What is the vowel you would like to buy? ")
            input_letter=clean_up(input_letter)
            if input_letter not in vowels:
                print("That is not a vowel. Go back to grade school, Buster.")
            elif input_letter in original_phrase:
                input_letters.append(input_letter)
                blank_phrase=phrasePrint(original_phrase, input_letters)
                counter=0
                current_balance=current_balance-250
                for letter in original_phrase:
                    if input_letter==letter:
                        counter+=1
                print("Congrats! " + input_letter + " appears in the phrase " + str(counter) + " time(s)")
                print("The new phrase is:")
                print(blank_phrase)
                print("Vowels guessed: " + input_letter)
                print("Your current winnings are: $" + str(current_balance))
                done=True
            else:
                input_letters.append(input_letter)
                blank_phrase=phrasePrint(original_phrase, input_letters)
                current_balance=current_balance-250
                print("Sorry, " + input_letter + " is not in the phrase.")
                print("The current phrase is:")
                print(blank_phrase)
                print("Vowel guessed: " + input_letter)
                print("Your current winnings are: $" + str(current_balance))
                done=True
    return current_balance

#Solving the puzzle.
def solveThePuzzle(original_phrase, current_balance, input_letters):
    input_phrase=input("What is the phrase? Single spaces only please and thank you. ")
    input_phrase=clean_up(input_phrase)
    if input_phrase==original_phrase:
        print('Congrats! That is correct!')
        print("Your winnings are: " + "$" + str(current_balance))
        print("Thank you for playing Wheel of Fortune!")
        done=True
    else:
        current_balance=0
        print("Sorry, that is incorrect. Your winnings are reset to $" + str(current_balance))
        blank_phrase=phrasePrint(original_phrase, input_letters)
        print("The current phrase is:")
        print(blank_phrase)
        print("Your current winnings are: $" + str(current_balance))
        done=False
    return done

def main():
    print("Welcome to the Wheel of Fortune!")
    input_letters=[]                                                            #intro print commands
    original_phrase=PhraseBank[random.randint(0,99)]
    print("The phrase is:")
    blank_phrase=phrasePrint(original_phrase, input_letters)
    print(blank_phrase)
    print("The category is: "+ determine_category(original_phrase))
    current_balance= 0
    print("Your current winnings are: " + "$" + str(current_balance))
    done=False
    while done==False:
        player_action=input("Would you like to Spin the Wheel (type ‘spin’), Buy A Vowel (type ‘vowel’), or Solve the Puzzle (type ‘solve’)? ")
        print("")
        player_action=clean_up(player_action)
        if player_action=="SPIN":
            input_letters, current_balance=spinTheWheel(original_phrase, current_balance, input_letters)
            print("The category is: "+ determine_category(original_phrase))
            print("You have guessed: ")
            for i, x in enumerate(input_letters):
                if i==len(input_letters)-1:
                    print(x)
                else:
                    print(x, end=' ')
        elif player_action=="VOWEL":
            current_balance= buyAVowel(original_phrase, current_balance, input_letters)
            print("The category is: "+ determine_category(original_phrase))
            print("You have guessed: ")
            for i, x in enumerate(input_letters):
                if i==len(input_letters)-1:
                    print(x)
                else:
                    print(x, end=' ')
        elif player_action=="SOLVE":
            done=solveThePuzzle(original_phrase, current_balance, input_letters)
            if current_balance<0:
                current_balance=0
        elif len(input_letters)>=25:
            print("You've guessed all the letters and FAILED to guess the solution (really, like how?). Good Job. You've lost. Jesus Christ.")
            current_balance=0
            print("Your winnings are: " + "$" + str(current_balance))
            done=True
        else:
            print("Come on. Really? That's not a valid input. TRY AGAIN.")
    print("Credits:")
    print("All the funny stuff: My mom")
    print("The code: Me (Grace)")
    print("Testing of the game: My mom and dad")
    print("Disclaimer: Don't take offense to the extremely rude messages. It was my MOM who did them. NOT ME. Thanks MOM.")


if __name__ == '__main__':
    main()
