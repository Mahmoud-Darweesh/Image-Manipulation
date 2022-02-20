import cv2
import glob
import numpy as np
import random
import math
import sys

#Basic settings
###############################################################################
#Used to increase resolution
quality = 1

#Changes the transparency of an image
alpha = 0.3

#sets the resolution of the sub images
sizeOfImageHeight = 60
sizeOfImageWidth = 60

#sets the resolution of the image
resolutionWidth = 1080 * quality
resolutionHeight = 1920 * quality

#Stores the paths of the images to be easly changed if needed
targetImagePath = 'target.jpg'
imagesFolderPath = "images/*.jpg"
outputImagePath = 'output.jpg'
###############################################################################

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
if not query_yes_no("Do you want to use the default settings?"):
	imagesFolderPath = input("Enter the path to the folder containing the images Ex:(images/*.jpg): ")
	targetImagePath = input("Enter the path to the target image Ex:(target.jpg): ")
	outputImagePath = input("Enter the path to the output image Ex:(output.jpg): ")
	alpha = float(input("Enter the transparency of the images Range(0~1): "))
	quality = int(input("Enter the quality of the output image (1-10): "))
	sizeOfImageHeight = int(input("Enter the height of the sub images: "))
	sizeOfImageWidth = int(input("Enter the width of the sub images: "))
	resolutionHeight = int(input("Enter the height of the output image: "))
	resolutionWidth = int(input("Enter the width of the output image: "))
###############################################################################

#Loads the files we need
###############################################################################
#Calculate the amount of sub images needed
amountOfImages = math.ceil(resolutionWidth / sizeOfImageWidth) * math.ceil(resolutionHeight / sizeOfImageHeight)
#amountOfImages = resolutionWidth * resolutionHeight	#amount of images to be generated if generated pixel by pixel
print('Amount of images: ' , amountOfImages)

#Loads the target image
targetImage = cv2.imread(targetImagePath)

#gets all subImages from the images folder
print('Processing...')

images = []
files = glob.glob(imagesFolderPath)
for myFile in files:
    image = cv2.imread(myFile)
    images.append(image)

print('Loaded images: ' , len(images))
###############################################################################

#Creates a collage of the images from the images folder
def processImage():
	proccessed = 0
	h_stack = []
	v_stack = []
	for y in range(0, resolutionHeight, sizeOfImageHeight):
		subH_stack = []
		for x in range(0, resolutionWidth, sizeOfImageWidth):
			img = random.choice(images)
			img = cv2.resize(img, (sizeOfImageWidth , sizeOfImageHeight))
			pImage = img
			subH_stack.append(pImage)

			#show progress
			proccessed += 1
			print(int(proccessed / amountOfImages * 100) , '%')
			print(proccessed ,' / ' , int(amountOfImages))
		#combine horizontal stacks into one
		subH_stack = np.hstack(subH_stack)
		h_stack.append(subH_stack)
	#combine vertical stacks into one
	v_stack = np.vstack(h_stack)

	cv2.imwrite(outputImagePath, v_stack)

#Fixs the sizes before blending them together
###############################################################################
#resize the target image
image = cv2.resize(targetImage,(resolutionWidth, resolutionHeight))

#create a grid of images
processImage()

#resize the target image again to fit the output image made from the processImage function
print('Resizing...')
processedImage = cv2.imread(outputImagePath)
image = cv2.resize(targetImage,(processedImage.shape[1], processedImage.shape[0]))
###############################################################################

#Blend the 2 images together
print('Blending...')
cv2.addWeighted(processedImage, alpha, image, 1 - alpha,0, image)
cv2.imwrite(outputImagePath,image)

#Show the image
cv2.imshow('Result', image)

#Prints info about the image
print('Done', '\n', 'Press any key to exit', '\n', 'Info: ' , '\n', 'resolutionWidth: ' , resolutionWidth , '\n', 'resolutionHeight: ' , resolutionHeight , '\n', 'sizeOfImageWidth: ' , sizeOfImageWidth , '\n', 'sizeOfImageHeight: ' , sizeOfImageHeight , '\n', 'amountOfImages: ' , amountOfImages, '\n', 'alpha: ' , alpha, '\n', 'quality: ' , quality, '\n', 'targetImagePath: ' , targetImagePath, '\n', 'imagesFolderPath: ' , imagesFolderPath, '\n', 'Images Used: ' , len(images)) 

#Wait for key press to exit
cv2.waitKey(0)