import csv

brightness_total = 0
count = 0
with open("color_details.csv", "r", newline='') as f:
  reader = csv.reader(f)
  for row in reader:
    if row[0] == "image_id":
      continue
    brightness = float(row[4])
    brightness_total+=brightness
    count+=1

print(brightness_total/count)

