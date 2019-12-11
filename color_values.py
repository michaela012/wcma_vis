'''
Script to get color and brightness details from collection images and write results to csv.
Output format: object id, dominant k colors (separate columns), brightness
'''

import cv2
import os
from sklearn.cluster import KMeans
import numpy as np
import csv


#specify inputs and parameters
IMAGE_DIR = "thumbnail_images/"
OUTPUT = "color_details.csv"
N_CLUSTERS = 3

#initialize list to hold all image details with header names (written for 3 clusters)
color_details_list = [["image_id","first_dominant","second_dominant","third_dominant","brightness"]]


#iterate through all .jpg image files
for file in os.listdir(IMAGE_DIR):
  filename = os.fsdecode(file)
  if filename.endswith(".jpg"):
    file_id = filename[:-4]
    print(file_id)
    working_image = os.path.join(IMAGE_DIR, filename)
  else:
    continue

  #read image
  working_image = cv2.imread(working_image)


  ##get dominant colors

  #convert from BGR to RGB
  img_colors = cv2.cvtColor(working_image, cv2.COLOR_BGR2RGB)

  #list of pixels
  img_colors = img_colors.reshape((img_colors.shape[0]*img_colors.shape[1], 3))

  #specify clusters
  kmeans = KMeans(n_clusters = N_CLUSTERS)
  kmeans.fit(img_colors)

  #save dominant colors (clusters), convert vals to integers
  colors = kmeans.cluster_centers_
  colors = colors.astype(int)

  img_info = [file_id]
  for color in colors:
    img_info.append(color)

  
  ##get brightness
  img_grayscale = cv2.cvtColor(working_image, cv2.COLOR_BGR2GRAY)
  brightness = f"{img_grayscale.mean():.2f}"

  img_info.append(brightness)


  ##store img_info
  color_details_list.append(img_info)


###save color details to csv
with open(OUTPUT, "w", newline='') as details:
  wr = csv.writer(details)
  wr.writerows(color_details_list)


