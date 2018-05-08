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


def getSpine(file):
    spineStr = ""
    openBraces = 0
    for line in file:
        if "{" in line:
            spineStr += line
            openBraces += 1
        elif "}" in line:
            if openBraces == 0:
                spineStr += "}"
                break
            else:
                spineStr += line
                openBraces -= 1
        else:
            spineStr += line

    return spineStr


def clean(inputPath, outputPath):
    print "*** Cleaning VRML File"
    inputFile = open(inputPath)

    for line in inputFile:
        if "{" in line:
            break

    spines = []
    for line in inputFile:
        if "FilamentSegment7" in line or "ColorSwitch_cColorClass" in line:
            spine = getSpine(inputFile)
            spineAux = line + spine
            spines.append(spineAux)

    inputFile.close()
    outputFile = open(outputPath, "w")
    outputFile.write("#VRML V2.0 utf8\n#Inventor V2.1 ascii\n\nGroup {\nchildren[\n")

    for i in range(0, len(spines) - 1):
        spine = spines[i]
        outputFile.write(spine)
        outputFile.write(",")

    outputFile.write(spines[len(spines) - 1])
    outputFile.write("]\n")
    outputFile.write("}")
    outputFile.close()


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
