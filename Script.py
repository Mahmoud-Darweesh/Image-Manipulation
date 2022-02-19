#capture an image
import cv2
import math

density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,"^`                                                                           '

resolutionWidth = 600
resolutionHeight = 200

targetImage = 'target.PNG'

#capture the target image
img = cv2.imread(targetImage, 0)

#set image resolution
img = cv2.resize(img,(resolutionWidth, resolutionHeight))

def convert():
    row = ''
    for y in range(resolutionHeight):
        print(row)
        with open('result.txt', 'a') as f:
            f.write(row + '\n')
        row = ''
        for x in range(resolutionWidth):
            row += density[math.floor((img[y,x]/255)*(len(density)-1))]
            row += ''

convert()

#read each pixel

cv2.imshow('output',img)
cv2.waitKey(0)
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break