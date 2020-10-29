import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('cat_l.jpg')
plt.show( img )

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,72,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


# noise removal
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)


# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=15)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)


# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)


# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
#chat et mure 
img[markers == 1] = [255,255,255]
#cote gauche en dessu du bon
img[markers == 3] = [0,128,0]

img[markers == 2] = [255,0,255]
img[markers == 4] = [125,128,0]

img[markers == 5] = [58,0,0]
plt.show(img)
cv2.imwrite('segmented.jpg',img)
