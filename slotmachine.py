#Assingment 7: Slot Machine
#Haley Brueckman
#3/4/21

#This program simulates a slot machine by generating 3 random numbers between 0-9
#If two numbers are the same it prints match
#If three numbers are the same it prints jackpot


print('Try your hand at luck! Press y to play and see if you get a match\n'
      '...or a jackpot! Press any key besides y to quit')


#import the random module to be able to generate random numbers.
import random

#Take in input from user and if it is 'y' then it runs a while loop
#And generates 3 random numbers
user_input=input()
while user_input == 'y':
    rand_num1 = random.randint(0, 9)
    rand_num2 = random.randint(0, 9)
    rand_num3 = random.randint(0, 9)
    #creates list of the random numbers
    slot_nums = [rand_num1, rand_num2, rand_num3]
    #prints the three random numbers and title
    print('Python Slot Machine')
    print(rand_num1, rand_num2, rand_num3)
    #Begins if statements to deciphers if there is a match, jackpot, or no match.
    if slot_nums[0] == slot_nums[1]:
        if slot_nums[1] == slot_nums[2]:
            print('Jack Pot!')
        else:
            print('Matched 2!')
    elif slot_nums[0] == slot_nums[2]:
        if slot_nums[1] == slot_nums[2]:
            print('Jack Pot!')
        else:
            print('Matched 2!')
    elif slot_nums[1] == slot_nums[2]:
        if slot_nums[1] == slot_nums[0]:
            print('Jack Pot!')
        else:
            print('Matched 2!')
        
    else:
        print('Sorry you lost! No Match.')
            
    
    #Asks user to play again and input y or other character to end.
    user_input=input('Play Again?(y):\n')
    

print('Good Game')
    
