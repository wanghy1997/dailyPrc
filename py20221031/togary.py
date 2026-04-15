from comFile import *
import cv2
import os

imgfile = 'E:\Codes\dailyPrc\images\img\ISIC_0015496.jpg'
grayfile = 'E:\Codes\dailyPrc\images\gray\ISIC_0015496.jpg'
img = cv2.imread(imgfile)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(grayfile, gray_img)
