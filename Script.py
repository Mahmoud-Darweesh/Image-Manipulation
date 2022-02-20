#capture an image
import cv2
import math
import sys

#Remove spaces to the string if you want more of the background to be visible
density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,"^`                                                                           '

#The size of the image
resolutionWidth = 200
resolutionHeight = 200

#Path of the image
targetImagePath = 'target.jpg'


#User Interface
###############################################################################
#Thanks to https://stackoverflow.com/a/3041990
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

#Lets user choose if they want to change the default settings
if not query_yes_no("Do you want to change the default settings?"):
    resolutionWidth = int(input("Enter the resolution width: "))
    resolutionHeight = int(input("Enter the resolution height: "))
    targetImagePath = input("Enter the path to the target image Ex:(target.jpg): ")
###############################################################################

#Load the image
targetImage = cv2.imread(targetImagePath, 0)

#Resize the image
targetImage = cv2.resize(targetImage,(resolutionWidth, resolutionHeight))

#Convert every pixel to a character from the density string and save it in a txt file
def convert():
    row = ''
    for y in range(resolutionHeight):
        print(row)
        with open('result.txt', 'a') as f:
            f.write(row + '\n')
        row = ''
        for x in range(resolutionWidth):
            row += density[math.floor((targetImage[y,x]/255)*(len(density)-1))]
            row += ''

convert()

#read each pixel

cv2.imshow('Target',targetImage)
cv2.waitKey(0)
cv2.destroyAllWindows()