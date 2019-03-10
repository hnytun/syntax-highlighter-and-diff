import sys

def getListOfLines(filename):
    """function that takes a filename and returns the contents in lines of text in a list"""
    return open(filename,"r").read().split("\n")

def getDiff(original,modified,output):
    """function that takes original file, modified file and an outputfile and
    writes the diff of the two files into the output file"""
    actionList=list()
    currentOriginalLine=0
    currentModFileLine=0
    outputFile = open(output,"w")
    originalListOfLines=getListOfLines(original)
    modifiedListOfLines=getListOfLines(modified)

    while(True):

        #if we hit the last line of the first file, we mark the rest of the elements of the second
        #as additions(+) and break the while-loop
        if currentOriginalLine == len(originalListOfLines)-1:
            for i in range(currentModFileLine,len(modifiedListOfLines)):
                actionList.append("+ " + modifiedListOfLines[i])
            break

        #if we hit the last line of the second file, we mark the remaining lines of the first
        #file as removals(-) since they never was found in the second file
        if currentModFileLine == len(modifiedListOfLines)-1:
            for i in range(currentOriginalLine,len(originalListOfLines)):
                actionList.append("- " + originalListOfLines[i])
            break

        #if the lines are the same, we tag the line with a "0"
        if originalListOfLines[currentOriginalLine] == modifiedListOfLines[currentModFileLine]:
            actionList.append("0 " + originalListOfLines[currentOriginalLine])
            currentOriginalLine +=1
            currentModFileLine +=1
        #else if we find out that there has been added some lines between two elements that exist in the original and the
        #modified version, then we just mark these lines between as additions, since they are not modifications
        #for example:
        #1          #1      #0 1
        #4   DIFF   #3   =  #+ 4          Since 4 is an addition between 1 and 3, not modification
        #3                  #0 3          of 3
        #slice the list in order to look at everything before the currentModFIleLine index in the list
        elif originalListOfLines[currentOriginalLine] in modifiedListOfLines[currentModFileLine:]:
            actionList.append("+ " + modifiedListOfLines[currentModFileLine])
            currentModFileLine+=1
        #then we do the same for removals between elements, in such an order that when you
        #diff 1 2 3 with 1 3 you get a removal of 2 in the diff, not modification of 2 to 3
        elif originalListOfLines[currentOriginalLine] not in modifiedListOfLines[:currentModFileLine]:
            actionList.append("- " + originalListOfLines[currentOriginalLine])
            currentOriginalLine+=1
        #else if we see that a line has been modified(aka when the elif above isnt true)
        #we mark the removed line as a removal(-) and the added line as an addition (+)
        else:
            actionList.append("- " + originalListOfLines[currentOriginalLine])
            actionList.append("+ " + modifiedListOfLines[currentModFileLine])
            currentOriginalLine+=1
            currentModFileLine+=1

    outputstr=""
    for line in actionList:
        outputFile.write(line + "\n")
        outputstr += line + "\n"
    outputFile.close()
    print(outputstr)



#function takes diff and puts it into the output-file, and also prints it for user
getDiff(sys.argv[1],sys.argv[2],"diff_output.txt")
