#Assingment 8: Dice
#Haley Brueckman
#3/9/22

#This program simulates rolling two dices 100 times and keeps track of the total
#It then prints how many times each total was generated symbolized by a star
#in a histogram.


#Import the random module to then generate random numbers
import random

#created list to keep track of how many times a total is rolled
star_list = [0,0,0,0,0,0,0,0,0,0,0]

#a list for each row in the histogram
row = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


#determined length of the list row to be used for indexing later
star_long = len(row)


#For loop that generates two random dice number 1-6 and then totals them.
#It does this 100 times. 
for num in range(0, 100):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1 ,6)
    total = dice1 + dice2
    num += 1
    
    #Finds the index of the total in row list. At the same index in star_list it
    #adds 1
    occurance = row.index(total)
    star_list[occurance] += 1
        

#For each index of star_list a for loop runs    
for index in range(star_long):

    #if the number at the index is more than zero it moves on to print the row
    #and a then starts while loop.
    if star_list[index] > 0:
        print(row[index], end = '')
        print(':', end = '')
        n = 1

        #A while loop begins to count how many times a total occured at an index
        #and print a star for each time.  
        while star_list[index] > n:
            print(' *', end = '')
            n += 1
        print(' *')
        
    #if the number at an index in star_list is zero, meaning that total was never
    #rolled, it still prints the row number, but with no stars. 
    else:
        print(row[index], end = '')
        print(':')
    
    

