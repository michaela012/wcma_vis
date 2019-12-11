import csv

total_brightness = 0
count = 0

with open("color_details.csv", "r") as file:
  readCSV = csv.reader(file, delimiter = ',')
  for row in readCSV:
    if count == 0:
      count += 1
      continue
    total_brightness += float(row[4])
    count += 1

average_brightness = total_brightness/count
print(average_brightness)

brightness_range = [average_brightness-.1, average_brightness+.1]

avg_bright_images = []
with open("color_details.csv", "r") as file:
  readCSV = csv.reader(file, delimiter = ',')
  first = True
  for row in readCSV:
    if first:
      first = False
      continue
    if float(row[4]) > brightness_range[0] and float(row[4]) < brightness_range[1]:
    #if round(float(row[4])) == round(average_brightness):
      avg_bright_images.append(row[0])

print(avg_bright_images)
print(len(avg_bright_images))
