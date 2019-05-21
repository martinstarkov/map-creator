import math as m
import os
from pathlib import Path
import cv2
import pyperclip
import xlrd
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = str(Path.home())

#used for converting numbers into their corresponding hex letter
hexDictionary = {
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F",
}

#if a value is above 9, turn it into a hex character
def hexify(number):
    if number > 9:
        return hexDictionary.get(number)
    else:
        return str(int(number))

#find the hex value of an individual (r,g,b) value
def makeHex(number):
    return hexify(m.floor(number / 16)) + hexify((number / 16 - m.floor(number / 16)) * 16)    

#stitch the (r,g,b) hex values into one hex code
def rgbToHex(rgbTuple):
    return "#{0:2}{1:2}{2:2}".format(makeHex(rgbTuple[2]), makeHex(rgbTuple[1]), makeHex(rgbTuple[0]))

#find and return the number corresponding to the hex code from the excel sheet
def hexToTexture(hexValue, dictionary):
    return dictionary.get(hexValue, "Unknown Hex Texture: " + hexValue)

#read the excel sheet and populate the texture dictionary
def setTextureDictionary(excel):
    dictionary = {}
    workbook = xlrd.open_workbook(excel)
    sheet = workbook.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        dictionary[sheet.cell_value(i, 2)] = int(sheet.cell_value(i, 1))
    return dictionary

#loop through the pixels of the image and return an array containing the corresponding numbers to each hex code
def generateData(image, excel):
    dictionary = setTextureDictionary(excel)
    print("Texture dictionary processed: " + str(dictionary))
    data = cv2.imread(image)
    height, width = data.shape[:2]
    pixelMap = []
    for row in range(height):
        pixelMap.append([])
        for column in range(width):
            hexColor = rgbToHex(data[row, column])
            pixelMap[row].append(hexToTexture(hexColor, dictionary))
    return pixelMap

#create / write and clear the data to a file that is readable by the C++ side of my map interpreter 
def writeToFile(path, data):
    f = open(path, "w+")
    for row in range(len(data)):
        for column in range(len(data[row])):
            if not column == len(data[row]) - 1:
                f.write(str(data[row][column]) + " ")
            else:
                f.write(str(data[row][column]))
        if not row == len(data) - 1:
            f.write("\n")
    f.close()

def runProgram(file_, folder_, image_, dictionary_):

    if ("." in file_ and ".txt" not in file_) or "/" in file_ or "\\" in file_:
        print("File name invalid. Please do not include file type such as "".docx"" in the end.")
        runProgram(input("Enter a name for the output file: "), "", "", "")
    
    if ".txt" not in file_:
        file_ += ".txt"

    if folder_ == "":
        runProgram(file_, input("Enter a location for the output file: "), "", "")

    if "/" in folder_:
        folder_.replace("/", "\\")
    if folder_[-1] != "\\":
        folder_ += "\\"

    if not os.access(folder_, os.W_OK) and not os.access(HOME_DIR + "\\" + folder_, os.W_OK):
        if "." in folder_:
            print("Folder path invalid. Please do not include the file name in the end.")
            runProgram(file_, "", "", "")
        else:
            #ask the user if they would like to create a new folder using input()[-1] to confirm
            if input("Would you like to generate a folder called \"" + folder_[:-1] + "\" in \"" + HOME_DIR + "\\\"? (y/n): ")[-1] == "y":
                print("Created \"" + HOME_DIR + "\\" + folder_ + "\" folder")
                folder_ = HOME_DIR + "\\" + folder_
                os.mkdir(folder_)
            else:
                print("Folder path invalid.")
                runProgram(file_, "", "", "")
    
    #if path is in home dir, add that to the start, but not if is in the root
    if HOME_DIR not in folder_ and ROOT_DIR not in folder_:
        folder_ = HOME_DIR + "\\" + folder_

    if image_ == "":
        runProgram(file_, folder_, input("Enter an image file path to read pixel data from: "), "")
    if not ".png" in image_ or not Path(image_.replace("/", "\\")).is_file():
        print("Image path invalid. Please give a valid "".png"" image file path.")
        runProgram(file_, folder_, "", "")

    if dictionary_ == "":
        runProgram(file_, folder_, image_, input("Enter an excel file path to read color values from: "))
    if not ".xlsm" in dictionary_ or not Path(dictionary_.replace("/", "\\")).is_file():
        print("Excel file path invalid. Please give a valid "".xlsm"" excel file path.")
        runProgram(file_, folder_, image_, "")

    data = generateData(image_, dictionary_)
    pyperclip.copy(str(data).replace("[", "{").replace("]", "}")) #convert python array to c++ form array with curly brackets
    print("Data copied to clipboard.")
    writeToFile(folder_ + file_, data)
    print("File generated at " + folder_ + file_)
    print("Thank you for using Martin and Nicole's Map Array Creator! :)")
    runProgram(input("Enter a name for the output file: "), "", "", "")

runProgram(input("Enter a name for the output file: "), "", "", "")