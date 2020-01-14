# wcma_vis

-- View the project [**here**](https://michaela012.github.io/wcma_vis/final_vis/)! --

### languages and libraries
The visualization itself was made using javascript (d3.js), HTML, and CSS. The underlying color analysis was done in python, using openCV. 

### about
 The goal of this project is to provide a unique, engaging way of exploring the entire collection at the Williams College Museum of Art (WCMA). 

Ordinarily, visitors will have little to no exposure to objects in the collection that are not on display at the time of their visit. Not only can objects in a current exhibit be seen in the physical museum space, but they are often the most prominently displayed on the museum webpage for digital visitors. This leads to many "hidden" pieces going unnoticed for long periods, and is compounded by the fact that more recognizable collection pieces tend to be part of exhibits more frequently than their lesser-known counterparts.

If a digital experience of the museum's collection is not arranged in relation to featured works, what else could it be based on? WCMA's search functionality already allows pieces to be found based on metadata, but this, like many such organizational schemes, requires the user already have some idea of what they are looking for. This is good for searching, but not so great for *exploring*, i.e. discovering new objects in the collection. 

Color, by contrast, lends itself well to exploration. By selecting a color and brightness classification, users can see all pieces that belong to that type. This makes every piece visible to the user and promotes no piece over another. From here, users can see detailed information by selecting any of the individual pieces.

Since the purpose of the color classifications is to aid user experience, the bounds of the color categories are set loosely, so as to encourage a more even distribution of pieces. The three dominant colors in each collection image are isolated using k-means clustering. All pieces were grouped according to the most dominant color with the exception of sepia, as there is a large body of sepia images (1224, whereas the next largest category has 601). Images are only classified as sepia if the top three dominant color values are in this category, otherwise the piece is categorized based on the top non-sepia color. 


Made for an independent study, Fall 2019, with advisors Iris Howley (CSCI) and Beth Fischer (WCMA).
