import cv2
import glob
import numpy as np
import random
import math

quality = 1

sizeOfImage = 20 * quality

resolutionWidth = 1920 * quality
resolutionHeight = 1080 * quality


imageResHeight = 100
imageResWidth = 100

amountOfImages = math.ceil(resolutionWidth / sizeOfImage) * math.ceil(resolutionHeight / sizeOfImage)
#amountOfImages = resolutionWidth * resolutionHeight


targetImagePath = 'target.PNG'

targetImage = cv2.imread(targetImagePath)

#gets all subImages from the images folder
images = []
files = glob.glob("images/*.PNG")
for myFile in files:
    image = cv2.imread(myFile)
    images.append(image)

def imageConvert(Blue,Green,Red):
	img = random.choice(images)

	img = cv2.resize(img, (sizeOfImage , sizeOfImage))

	for y in range(sizeOfImage):
		for x in range(sizeOfImage):
			b,g,r = (img[y, x])
			img[y, x] = int((Blue * b)/255), int((Green * g)/255), int((Red * r)/255)

	return img


def processImage(image):
	proccessed = 0
	h_stack = []
	v_stack = []
	for y in range(0, resolutionHeight, sizeOfImage):
		subH_stack = []
		for x in range(0, resolutionWidth, sizeOfImage):
			#convert image to a hue of the targeted pixel
			b,g,r = (image[y, x])
			pImage = imageConvert(int(b),int(g),int(r))
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

	cv2.imwrite('output.png', v_stack)


image = cv2.resize(targetImage,(resolutionWidth, resolutionHeight))
processImage(image)
print('done')

cv2.waitKey(0)