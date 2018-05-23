def convert(inFile, outFile):
    input = open(inFile, "r")
    output = open(outFile, "w")

    output.write("#VRML V2.0 utf8\n#Inventor V2.1 ascii\n\nGroup {\nchildren")
    for line in input:
        if "{" in line:
            break

    for line in input:
        if "FilamentSegment6" in line:
            skipSegment(inFile)
        else:
            output.write(line.replace("VRML", ""))

    input.close()
    output.close()


def isVRML1(inFile):
    input = open(inFile, "r")
    line = input.readline()
    return "V1.0" in line


def getSpine(line,file):
    spineLines = []
    spineLines.append(line)
    openBraces = 0
    for line in file:
        if "{" in line:
            spineLines.append(line)
            openBraces += 1
        elif "}" in line:
            if openBraces == 0:
                spineLines.append( "}")
                break
            else:
                spineLines.append(line)
                openBraces -= 1
        else:
            spineLines.append(line)

    return spineLines


def clean(inputPath, outputPath,segments):
    print "*** Cleaning VRML File"
    inputFile = open(inputPath)

    for line in inputFile:
        if "{" in line:
            break


    spines = []
    for line in inputFile:
        if "FilamentSegment7" in line or "ColorSwitch_cColorClass" in line or "bpColorSwitchSetInventor" in line or (segments and "FilamentSegment6" in line):
            spine = getSpine(line,inputFile)
            spines.append(spine)

    inputFile.close()
    outputFile = open(outputPath, "w")
    outputFile.write("#VRML V2.0 utf8\n#Inventor V2.1 ascii\n\nGroup {\nchildren[\n")

    for i in range(0, len(spines) - 1):
        spine = spines[i]
        for line in spine:
            outputFile.write(line)
        outputFile.write(",")

    for line in spines[len(spines) - 1]:
        outputFile.write(line)

    outputFile.write("]\n")
    outputFile.write("}")
    outputFile.close()
    print "*** Cleaning Finish"


def skipSegment(inFile):
    openBraces = 0
    for line in inFile:
        if "{" in line:
            openBraces += 1
        elif "}" in line:
            if openBraces == 0:
                break
            else:
                openBraces -= 1
