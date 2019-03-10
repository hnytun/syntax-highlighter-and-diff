import re
import sys


def getColoredText(text, code=92):
    """makes a colored text depending on code which is defaulted to 92, slightly stripped version of the method in
    https://github.com/UiO-INF3331/student-resources-16/blob/master/assignment5_files/coloring_example.py"""
    start_code = "\033[{}m".format(code)
    end_code = "\033[0m"
    text=start_code + text + end_code
    return text


def colorizePattern(color):
    """function that is wrapped around a function, returns the wrapped function colorizeObject
    this is necessary because re.sub does not take functions with arguments,
    but can take this colorizeObject function that is returned
    by the colorizePattern function
    """
    def colorizeObject(ob):
        """Used in re.sub() to colorize all items """
        return getColoredText(ob.group(0),color)
    return colorizeObject


def getPatternDictionary(filename):
    """function that takes a filename with elements and patterns and returns a dict with elements and the regex to fetch the element"""
    patternDict = {}
    #open syntaxfile and add syntaxes to map
    with open(filename) as f:
        #go through every syntax declaration (tells what pattern to use to find each element)
        for line in f:
            #add name of pattern to dict (for example comment), this is last word on each line, we can be sure of this hopefully, also
            #we strip the endline at the end, which is made by atom for some reason(i think)
            element = line.split(" ")[-1].strip()
            #fetch wwwthe pattern that is between the apostrophes in the syntax file by using a regex(yes, we use a regex to get a regex)
            patternInFileForElement = re.match(r"^.*\"(.*)\".*$",line)
            patternForElement = patternInFileForElement.group(1)
            patternDict.update({element:patternForElement})
    return patternDict

def getColorDictionary(filename):
    """function that takes a filename with elements and colors and returns a dict with elements and the color of the element
    my print color function takes in an integer between 0 and 110 so i strip the 0;xx to make it easier to pass in the function"""
    colorDict = {}
    with open(filename) as f:
        #go through every line(element: color)
        for line in f:
            #first fetch the element
            element = line.split(" ")[0].replace(':','')
            #then fetch the color
            color = line.split(" ")[-1].strip().split(";")[-1]
            #map color to element
            colorDict.update({element:color})
    return colorDict

def printColorizedFileText(syntax,theme,fileCode):
    """function that takes in syntaxfile, themefile, and a file to read, and prints colorized output"""
    patternsOfElements = getPatternDictionary(syntax)
    colorsOfElements = getColorDictionary(theme)
    codefile = open(fileCode,"r")
    str = codefile.read()

    #print out colorized version of all elements in the syntaxfile, which we do
    #by getting a pattern for every element, then substitute the pattern in the file with
    #the respective color of the pattern-element by looking in the theme-file
    for element in patternsOfElements.keys():
            elementPattern = re.compile(patternsOfElements[element],re.MULTILINE)
            str = re.sub(elementPattern,colorizePattern(colorsOfElements[element]),str)
    #str = re.sub(elementPattern,colorizePattern(patternsOfElements["comment"]),str)
    print(str)


printColorizedFileText(sys.argv[1],sys.argv[2],sys.argv[3])
