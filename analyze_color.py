import csv
import math
import colorsys
import json

from pprint import pprint

'''
find color ranges
so many collection images: view them all by color using collapsible force layout. JSON structure:

 {"name":"WCMA Collection",
  "img": <img>,
  "children": [
    {
      "name": "reds"
      "children": [
        {
          "name": "light"
          "children": [
            { "title": <art title>,
              "maker": <maker>
              "medium": <medium>
              "creation date": <date>
              "accession date": <date>
              "img": <thumbnail image>,
              "size": 40000
              "color":<hex val of color>
              "brightness":<brightness--not displayed but use to sort>
            },
            <repeat for other light images>
          ]
          <repeat for dark reds>
        }
        <repeat for other light images>
      ]
    }
    { <repeat for all color families>
    }
  ]
 }

--notes--
clicking on a node collapses it. can they start collapsed? so the user can see the color label and 
  expand what they want?
need more differentiation. Sort by color, also light/dark (find brightness threshold -- my brightness 
  ~equates to combining s&v parameters)
'''


#boundaries for color identification based on hue:
#   red: 350 - 359, 0-13
#   orange: 14-40
#   yellow: 41-64
#   green: 65-159
#   cyan: 160-183
#   blue: 184-259
#   purple: 260-299
#   magenta: 300-349
###specials- check these first
#   black: value<15
#   white: saturation<5, value>95
#   !!sepia: hue in orange range, value<70
##################################################################################


#return list of hsv values from rgb input
def get_hsv(r,g,b):
  h,s,v = colorsys.rgb_to_hsv(r,g,b)
  #saturation,value used for special identification
  return (h*359)//1,s*100//1,v*100//1


def get_color_classification(r,g,b):
  color_class_dict = {"red":[0, 13], "red2":[350,359], "orange":[14,36], "yellow":[37,64], "green":[65,159], "cyan":[160,183], "blue":[184,259], "purple":[260,299], "magenta":[300,349]}

  #get hsv values
  h,s,v = get_hsv(r/255,g/255,b/255)

  #first check for black and white
  if v < 15:
    return "black"
  if s < 5 and v > 95:
    return "white"

#check main colors and sepia
  for color in color_class_dict:
    col_range = color_class_dict[color]
    if h in range(col_range[0], col_range[1]+1):
      #handle special cases, else return color
      if color == "red2":
        return "red"
      if (color == "orange" and (s<40 or v<30)) or (color == "yellow" and s < 40):
        return "sepia"
      return color


#return list of [img_id, color_classification, dom_color_hex, brightness]
def relevant_image_color_data(image_colors):
  img_id = image_colors[0]

  first_dom = image_colors[1]
  second_dom = image_colors[2]
  third_dom = image_colors[3]

  first_color_class = ""

  for dom_color in [first_dom, second_dom, third_dom]:
    r = dom_color[0]
    g = dom_color[1]
    b = dom_color[2]

    hex_color = hex(int((str(r) + str(g) + str(b))))
    color_classification = get_color_classification(r,g,b)

    if dom_color == first_dom:
      first_color_class = color_classification

    if color_classification in ["sepia"]:
      continue

    return [img_id, color_classification, image_colors[4]]

  #only executed if all colors are either white or sepia
  return [img_id, first_color_class, hex_color, image_colors[4]]



def write_to_json(JSON_FILENAME, data):
  with open(JSON_FILENAME, "w") as outfile:
    json.dump(data, outfile)


def clean_extra_space(lst):
  if len(lst) == 3:
    return [int(i) for i in lst]
  while "" in lst:
    lst.remove("")
  return [int(i) for i in lst]


def run(COLOR_DETAILS_FILENAME, PIECE_INFO_FILENAME):
  #storage for json org
  all_piece_info = {}

  color_children = {
    "red" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "orange" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "yellow" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "green" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "cyan" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "blue" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "purple" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "magenta" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "black" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "white" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }],
    "sepia" : [{"name":"light", "img":"label_images/light.jpg", "children":[] } , {"name":"dark", "img":"label_images/dark.jpg", "children":[] }]
  }

  with open(PIECE_INFO_FILENAME, "r", newline='') as info_f:
    reader = csv.reader(info_f)
    for row in reader:
      if row[0].isalpha():
        continue
      # acc_num: [accession_date,title,maker,medium,description,classification,creation_date_avg]
      all_piece_info[row[1]] = [row[2], row[3], row[4], row[5], row[6], row[7], row[8]]

  with open(COLOR_DETAILS_FILENAME, "r", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == "image_id":
        continue

      img_id = row[0]
      color1 = clean_extra_space([i for i in row[1][1:-1].split(" ")])
      color2 = clean_extra_space([i for i in row[2][1:-1].split(" ")])
      color3 = clean_extra_space([i for i in row[3][1:-1].split(" ")])

      brightness = float(row[4])
      
      color_data = relevant_image_color_data([img_id, color1, color2, color3, brightness])

      #needed info pieces
      img_id = img_id.replace("_",".")
      try: acc_date = all_piece_info[img_id][0]
      except:
        continue
      title = all_piece_info[img_id][1]
      maker = all_piece_info[img_id][2]
      medium = all_piece_info[img_id][3]
      classification = all_piece_info[img_id][5]
      creation_date = all_piece_info[img_id][6]

      used_img_data = {"title":title, "maker":maker, "medium":medium, "creation_date":creation_date, 
        "classification": classification, "accession_date": acc_date, "img": "thumbnail_images/"+img_id.replace(".","_")+".jpg", "size":30000}

      if brightness > 149:
        #save to color's light children
        color_children[color_data[1]][0]["children"].append(used_img_data)
      else:
        color_children[color_data[1]][1]["children"].append(used_img_data)

  for i in color_children:
    for j in [0,1]:
      print(i + " " +color_children[i][j]["name"] + ": " + str(len(color_children[i][j]["children"])))


  #final json structure
  json_data = {
    "name":"WCMA collection", "img":"label_images/complete_collection.jpg", "children":[
      {"name":"red", "img":"label_images/red.jpg", "children": color_children["red"]},
      {"name":"orange", "img":"label_images/orange.jpg", "children": color_children["orange"]},
      {"name":"yellow", "img":"label_images/yellow.jpg", "children": color_children["yellow"]},
      {"name":"green", "img":"label_images/green.jpg", "children": color_children["green"]},
      {"name":"cyan", "img":"label_images/cyan.jpg", "children": color_children["cyan"]},
      {"name":"blue", "img":"label_images/blue.jpg", "children": color_children["blue"]},
      {"name":"purple", "img":"label_images/purple.jpg", "children": color_children["purple"]},
      {"name":"magenta", "img":"label_images/magenta.jpg", "children": color_children["magenta"]},
      {"name":"black", "img":"label_images/black.jpg", "children": color_children["black"]},
      {"name":"white", "img":"label_images/white.jpg", "children": color_children["white"]},
      {"name":"sepia", "img":"label_images/sepia.jpg", "children": color_children["sepia"]},
    ]
  }

  #pprint(json_data)
  #write_to_json(JSON_FILENAME, json_data)
  #test = {"name": "red", "img":"label_images/red.jpg", "children": color_children["red"]}
  write_to_json("final_vis/red.json", json_data["children"][0])
  write_to_json("final_vis/orange.json", json_data["children"][1])
  write_to_json("final_vis/yellow.json", json_data["children"][2])
  write_to_json("final_vis/green.json", json_data["children"][3])
  write_to_json("final_vis/cyan.json", json_data["children"][4])
  write_to_json("final_vis/blue.json", json_data["children"][5])
  write_to_json("final_vis/purple.json", json_data["children"][6])
  write_to_json("final_vis/magenta.json", json_data["children"][7])
  write_to_json("final_vis/black.json", json_data["children"][8])
  write_to_json("final_vis/white.json", json_data["children"][9])
  write_to_json("final_vis/sepia.json", json_data["children"][10])







if __name__ == "__main__":
  COLOR_DETAILS_FILENAME = "color_details.csv"
  PIECE_INFO_FILENAME = "cleaned_collection_data.csv"
  JSON_FILENAME = "display_data.json"

  run(COLOR_DETAILS_FILENAME, PIECE_INFO_FILENAME)
  

  

    

