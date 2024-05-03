# Python Turtle - Morphing Algorithm - www.101computing.net/python-turtle-morphing-algorithm/
import turtle
import random
from time import sleep

myPen = turtle.Turtle()
myPen.hideturtle()
myPen.tracer(0)
myPen.speed(0)
window = turtle.Screen()
window.bgcolor("#000000")
myPen.pensize(4)


def morphing(letter1, letter2, t, fontSize, color, x, y):
    myPen.color(color)
    letter1 = letter1.upper()
    letter2 = letter2.upper()
    myPen.penup()
    myPen.goto(x, y)
    myPen.pendown()

    # Check that the characters belong to the Alphabet
    if shape1 in circles and shape2 in circles:
        letter1Coordinates = alphabet[letter1]
        letter2Coordinates = alphabet[letter2]

        dots = []

        # Some letters have more nodes than others. We need to ensure they have the same number of nodes
        if len(letter1Coordinates) > len(letter2Coordinates):
            lastDot = letter2Coordinates[len(letter2Coordinates) - 1]
            for i in range(0, len(letter1Coordinates) - len(letter2Coordinates)):
                letter2Coordinates.append(lastDot)
        elif len(letter1Coordinates) < len(letter2Coordinates):
            lastDot = letter1Coordinates[len(letter1Coordinates) - 1]
            for i in range(0, len(letter2Coordinates) - len(letter1Coordinates)):
                letter1Coordinates.append(lastDot)

        numberOfDots = len(letter1Coordinates)

        # Morphing Calculations
        # Calculate the new interim coordinates of each node
        for i in range(0, numberOfDots):
            dotx = letter1Coordinates[i][0] + (letter2Coordinates[i][0] - letter1Coordinates[i][0]) * t / 10
            doty = letter1Coordinates[i][1] + (letter2Coordinates[i][1] - letter1Coordinates[i][1]) * t / 10
            dots.append([dotx, doty])

        # Draw the resulting morphed charcater
        myPen.penup()
        for dot in dots:
            myPen.goto(x + dot[0] * fontSize, y + dot[1] * fontSize)
            myPen.pendown()


# Main Program Starts Here
fontSize = 200
fontColor = "#FF00FF"

letter1 = "A"
letter2 = "Z"
while True:
    # From A to Z in 10 steps
    for t in range(0, 11):
        myPen.clear()
        morphing(letter1, letter2, t, fontSize, fontColor, -100, -100)
        sleep(0.05)
        myPen.getscreen().update()

    sleep(0.5)

    # From Z to A in 10 steps
    for t in range(0, 11):
        myPen.clear()
        morphing(letter2, letter1, t, fontSize, fontColor, -100, -100)
        sleep(0.05)
        myPen.getscreen().update()

    sleep(0.5)