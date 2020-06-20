# 2D Geometric shapes generator

A generator of 2D geometric shape data set, this data set is composed of a set of 
images stored in `png` files. Each image contains one of the following shapes : 
Square, Traingle, Circle, Star, Polygon, Heptagone, Hexagone, Octagone and Nonagon.

Each image is generated within the following parameters : 

- A fixed size of 200x200 pixel

- A random background colour
- A random filling colour of each shape
- A random rotation angle between -180° and 180°
- A random position inside of the containing image
- A random perimeter

**All the parameters described above are generated for each sample independently 
and identically.** 


## Installation

Clone the source code with : 

```
clone https://github.com/elkorchi/2DGeometricShapesGenerator.git
```

Install project requirements specified in `requirements.txt` : 

```
pip install - r requirements.txt 
```
 
 Run the data set generation with :
 
```
python shape_generator.py generate-shapes --size=1000 --destination=/storage/directory
```

The generation command may accept the following option : 

- `--size` (required): The number of generated images per each shape
- `--destination` (required): The path of the folder where the generated images 
will be stored.
- `--show-animation` (optional): If specified the drawing animation of each image, 
will be activated. **Note that if this option is activated, the generation process will be very slow.**