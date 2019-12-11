import csv

OUTPUT = "final_less_info.csv"

with open("basic_visualizations/less_info_pieces.csv", "r") as file:
  reader = csv.reader(file, delimiter = ',')
  with open(OUTPUT, "w", newline='') as outfile:
    wr = csv.writer(outfile)
    
    for row in reader:
      if ("Anonymous" in row[3] or "?" in row[3]):
        print(row[3])
        wr.writerows([row])
        