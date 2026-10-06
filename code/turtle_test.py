import turtle

def drawSquare(t, sz):
    for i in range(4):
        t.forward(sz)
        t.left(90)
        
def some_function():
    print('Output')

def main():                      # Define the main function
    wn = turtle.Screen()         # Set up the window and its attributes
    alex = turtle.Turtle()       # create alex
    drawSquare(alex, 200)        # Call the function to draw the square
    wn.exitonclick()

if __name__=='__main__':
    print(__name__)
    main()                           # Invoke the main function
