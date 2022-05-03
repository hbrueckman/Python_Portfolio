#Assingment 10: Picture
#Haley Brueckman
#4/2/22


#This program allows the user to make their own picture of flowers and a sun
#by pressing the keys F1, F2, F3, s, and t which trigger functions to be called.

#import turtle module
import turtle


# This creates a window and sets the size, color, and title
wn = turtle.Screen()
wn.bgcolor("honeydew")
wn.setup(1000, 800)
wn.title("Sunny Day")


#Turtle set up
brush = turtle.Turtle()

#Function that moves pen to location of click. 
def click(x, y):
    brush.penup()
    brush.goto(x , y)
    brush.pendown()

#Function that draws sun when "s" is typed
def sun():
    #sets up how the sun will look and the colors
    brush.speed(30)
    brush.pensize(2)
    brush.hideturtle()
    brush.begin_fill()
    brush.color("Orange", "Yellow")
    #for loop that sets up how the sun will look
    for i in range(50):
        brush.forward(200)
        brush.left(170)
    brush.end_fill()

#Flower functions
#Turquoise flower by typing F1
def flower1():
    #sets up how the flower will look
    brush.speed(30)
    brush.hideturtle()
    brush.pensize(10)
    brush.color("turquoise2")
    #for loop that creates the flower
    for x in range(20):
        brush.circle(40,70)
        if x %3==0:
            brush.circle(10,90)
    
    turtle.done

#Purple flower by typing F2
def flower2():
    #sets up how the flower will look
    brush.speed(30)
    brush.hideturtle()
    brush.pensize(2)
    brush.color("Purple")
    brush.fillcolor("Purple")
    brush.begin_fill()
    #for loop that creates the flower
    for n in range(3):
        for x in range (8):
            for i in range(2):
                brush.circle(5+n*20,90)
                brush.lt(90)
            brush.lt(45)
    brush.end_fill()

#Red flower by typing F3
def flower3():
    #sets up how the flower will look
    brush.speed(30)
    brush.hideturtle()
    brush.pensize(4)
    brush.color("firebrick2")
    brush.fillcolor("firebrick2")
    brush.begin_fill()
    #for loop that creates the flower.
    for n in range(1):
        for x in range (8):
            for i in range(2):
                brush.circle(30+n*20,90)
                brush.lt(90)
            brush.lt(45)
    brush.end_fill()
  
#Green Stem function by typing t
def stem():
    brush.speed(30)
    brush.hideturtle()
    brush.pensize(7)
    brush.color("Green")
    #sets the angle so the stem goes down. 
    brush.setheading(270)
    brush.forward(200)
    
#These commands make it so when one of the keys F1, F2, F3, s, or t are pressed
#the appropiate function will run.
wn.onclick(click)
wn.onkey(sun, "s")
wn.onkey(flower1, "Up")
wn.onkey(flower2, "Down")
wn.onkey(flower3, "Right")
wn.onkey(stem, "t")

#This allows the window to be waiting for the user to press a key and start an
#event that calls one of the functions. 
wn.listen()
wn.mainloop()



#function to create the circles for the lights
def circle(t, ht, color1, color2):
    t.penup()# Move turtle
    t.forward(40)
    t.left(90)
    t.forward(ht)
    t.shape('circle')  # Set shape to circle
    t.shapesize(3)  # Set size of circle
    t.color(color1, color2) # Fill color in circle
    

circle(green, 40, 'grey', 'grey')
circle(yellow, 100, 'grey', 'grey')
circle(red, 160, 'grey', 'grey')


# This variable holds the current state of the machine
state_num = 0


#function that uses if statements to determine the state and what light should go on for how long. 
def traffic_lights():
    global state_num #Global variable to keep track of states.
    
    if state_num == 0: #If state is 0 then light is green for 5 seconds.
        green.color('green')
        yellow.color('grey')
        red.color('grey')
        wn.ontimer(traffic_lights, 5000) #times function to happen for 5 seconds
        state_num = 1 #changes state to next light
        
    elif state_num == 1: #if state is 1 then light is yellow for 2 seconds
        red.color('grey')
        green.color('grey')
        yellow.color('yellow')
        wn.ontimer(traffic_lights, 2000) ##times function to happen for 2 seconds
        state_num = 2 #changes state to next light
        
    else:               #if state not 1 or 0 than light is red for 5 seconds. 
        yellow.color('grey')
        green.color('grey')
        red.color('red')
        wn.ontimer(traffic_lights, 5000) #times function to happen for 5 seconds
        state_num = 0 #changes state to next light, which starts the cycle again. 
        
traffic_lights(
