#Assignment 5: Fortune
#Haley Brueckman
#2/14/22
#This code takes input and based off that input, returns a
#different fortune outcome by utilizing if statements.

#Intro
print('Hello, you have reached the page of Future for Humans inc.')
print('Here you have the option to find out a bit\nabout your future'
      ' by just answering a few questions.')
future_entry = input('\nIf you wish to hear your future, type yes. If not, type no here: ')

#If input is yes branch
if future_entry == 'yes':
    fortune1 = int(input('\nHow old are you? Type your age here: '))
    
    #If input Under than 26 and above zero age range branch
    if (fortune1 < 26) and (fortune1 > 0):
        print('\nOh Hello fellow Gen Z or younger human. Prepare to hear your future soon...')
        fortune2 = input('Choose bike or car, and type answer here: ')
        
        #Bike input branch
        if fortune2 == 'bike':
            fortune3 = int(input('Pick a number 1-3: '))
            
            #If number is 1 or 2 branch fortune
            if (fortune3 == 1) or (fortune2 == 2):
                print('\nYou will die young saving the earth from\nclimate change,'
                      'but you will only be remembered for your\nspicy and controversial '
                      'love affair with Billie Eilish.')
                
            #If number is 3 branch fortune
            else:
                print('\nYou will discover a way to create a huge\nspace vaccumm '
                      'that will suck co2 from the atmosphere,\nbut you will end up '
                      'getting sucked up with it.')
                
        #Car branch
        elif fortune2 == 'car':
            fortune3 = int(input('Pick a number 1-3: '))
            
            #If number is 1 branch fortune
            if (fortune3 == 1):
                print('\nYou will become old living on a space ship\nplummeting away '
                      'from the polluted uninhabitable earth\nlistening to David Bowie.')
                
            #If number is 2 or 3 branch fortune
            else:
                print('\nYou will find Big Foot in the wild and become dear friends,\nonly '
                      'to later betray him and give away his location to the media\nseeking'
                      ' to be an influencer.')
            
    #If input over 25 age range branch
    elif (fortune1 > 25):
        print('\nOh Hello mature human of older age, prepare to ride\nthe time traveling delorean'
              'to see your future\nafter answering one more question...')
        fortune4 = input('Type your favorite food: ')
        
        #If length of the string input fortune4 is more than 6 fortune
        if len(fortune4)>6:
            print('\nYou will become old surfing facebook to find hot gossip '
                  'about people\nwho never knew your name in high school.')
        
        #If length of the string input fortune4 is less than 6 fortune
        else:
            print('\nYou will marry an elderly Mark Zuckerberg\nand then poison '
                  'him and take over facebook and rule the world')
            
    #If a negative number is inputed into age range        
    else:
        print('\nYou are unborn human, your future is unknown as your paperwork to '
              'join humanity is being prepared.\nPlease wait 9 months to speak with a representitive.')
        
#If input is no branch
else:
    print('\nThank you for your time, you have chosen to live in unknown bliss of your future.')
