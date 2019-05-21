# map-creator
Turn your .png files into tilemap data arrays that can be used for easy 2D platformer level creation!

# How to compile
In order to use the program, it must first be compiled using pyinstaller. Here is a step-by-step guide for beginners:
#### Step 1
 - [Download](https://www.python.org/downloads/) and install Python (if you haven't yet)
#### Step 2
 - Once python is installed, open command prompt and type ```python -m pip install pyinstaller``` to install the pyinstaller executible compilation module.
#### Step 3
 - In command prompt, navigate to the folder where you have saved the ```pixelMapper.py``` file and type ```pyinstaller pixelMapper.py``` or whatever you may have renamed the file to. This will take a moment and generate a few folders.
#### Step 4
 - Navigate into the newly generated ```dist``` folder and then into ```pixelMapper```. Inside this folder you will find an executable called ```pixelMapper.exe```, opening this file will run the program.
#### Step 5 (optional)
 - To skip repeating step 4 each time you would like to use the program, you can right-click the executable, select ```send to``` and pick ```Desktop (create shortcut)```, this will create a desktop shortcut for the executable. Enjoy!

# How to use
After compiling and running the pixel mapper, it will ask you for some information:
- File name for your tilemap data
- Location to place this file
- Path to your readable ".png" image
- Path to your ".xlsm" excel texture dictionary

## Example image
![exampleImage](https://user-images.githubusercontent.com/5933654/58112556-736cdc80-7bfc-11e9-8af4-5f3211076717.png)

It is important that the hex codes used in the image match the texture dictionary values

## Example dictionary
![exampleDictionary](https://user-images.githubusercontent.com/5933654/58112555-736cdc80-7bfc-11e9-842d-909c40c64fd2.png)

The crucial part in the texture dictionary is that it contains numbers in the second column and hex codes in the third column, everything else in the image is optional (names and rgbs). The number column tells the program to replace the corresponding pixels with those integers. 

The example_dictionary.xlsm provided in this repository contains a macro that will color the background of the hex cells with the appropriate color, make sure to run the macro every time a color is added if you would like the cells to update color.

## Example output file
![exampleSmall](https://user-images.githubusercontent.com/5933654/58112557-736cdc80-7bfc-11e9-9225-4daacf5f23b6.png)

### Example output file zoomed in
![exampleBig](https://user-images.githubusercontent.com/5933654/58112554-736cdc80-7bfc-11e9-8c1f-b3f02b3772f5.png)

As seen above, the program has done its job in converting the image into an array of numbers that can be processed by a game's tilemap code. 
