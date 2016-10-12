import cv2
import numpy as np
import math


#Liews Wuttipat
#Developer1 Jettanan Homchanthanakul --> Differentiate between Rectangle & Square
#Input Image

#Image Enchancement
# -- Sharp, Blur

#Image Morphological Processing
# -- Erod

#Image Segmentation
# --

#Feature Extraction
# -- Properties of Shape, Area, Length
# -- SIFT Feature
# -- HOG Feature

#Classification
# -- SVM Support Vector Machine
# -- Neuron Network
# -- AdaBoost

#Output Image

img = cv2.imread('image.png')
img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
thresh = cv2.bitwise_not(cv2.threshold(img_grey, 127, 255, 0)[1])

#cv2.CHAIN_APPROX_NONE   ### Draw all of contour
#cv2.CHAIN_APPROX_SIMPLE ### Draw only critical point

_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
num = 0
for cnt in contours:
    #Find moments and find center of mass
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01']/M['m00'])

    #Approximation shape from arclength 3%
    epsilon = 0.03 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    font = cv2.FONT_HERSHEY_SIMPLEX

    #Draw approx
    for i in approx:
        cv2.circle(img, (i[0][0], i[0][1]), 3, (255, 0, 0), -1)
    #Draw center of mass
    cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)

    #Draw text on Image

    cv2.putText(img, '('+str(cx)+', '+str(cy)+')', (cx-20, cy+35), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
    txt = ''
    if len(approx)==3:
        txt = 'Triangle'
    elif len(approx)==4:
        point1x = 2000
        point1y = 2000
        point2x = 2000
        point2y = 2000
        point3x = 2000
        point3y = 2000
        p1 = 0
        p2 = 0
        p3 = 0
        for j in range(0,4):
            if point1x > approx[j][0][0] :
                    point1x = approx[j][0][0]
                    point1y = approx[j][0][1]
                    p1 = j
            elif point1x == approx[j][0][0]:
                if(point1y > approx[j][0][1]):
                    point1x = approx[j][0][0]
                    point1y = approx[j][0][1]
                    p1 = j
        for k in range(0,4):
            if (point2x > approx[k][0][0]) & (p1 != k):
                    point2x = approx[k][0][0]
                    point2y = approx[k][0][1]
                    p2 = k
            elif point2x == approx[k][0][0]:
                if (point2y > approx[k][0][1]):
                    point2x = approx[k][0][0]
                    point2y = approx[k][0][1]
                    p2 = k
        for l in range(0,4):
            if (point3x > approx[l][0][0]) & (p2 != l) & (p1 != l):
                    point3x = approx[l][0][0]
                    point3y = approx[l][0][1]
                    p3 = l
            elif point3x == approx[l][0][0]:
                if (point3y > approx[l][0][1]):
                    point3x = approx[l][0][0]
                    point3y = approx[l][0][1]
                    p3 = l
        print point1x ,point1y , p1
        print point2x, point2y, p2
        print point3x, point3y, p3
        ref1 = math.sqrt(((point1x-point2x)**2)+((point1y-point2y)**2))
        ref2 = math.sqrt(((point1x-point3x)**2)+((point1y-point3y)**2))
        print ref1
        print ref2
        if(ref1-ref2 < 1) & (ref1-ref2 > -1) :
            txt = 'Square'
        else :
            txt = 'Rectangle'
        num += 1
    elif len(approx)==8:
        txt = 'Circle'
    cv2.putText(img, txt, (cx - 20, cy + 55), font, 0.4, (0, 0, 255), 1,cv2.LINE_AA)

cv2.imshow('Output',img)
cv2.waitKey(0)
cv2.destroyAllWindows()