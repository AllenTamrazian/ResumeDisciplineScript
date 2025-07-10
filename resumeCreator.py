from collections import defaultdict
import re

# where is the file
filePath = "main.tex"
# open the file
with open(filePath) as f:
    # Reads all lines into a list of strings.
    lines = f.readlines()
# read to check if this is the correct file
# print(file.read())

# create a new file
templateFile = open("templateFile.tex","w+")
# make a list to store the lines where a template starts/ends
templateIndexes = []
# go through each line
for i, line in enumerate(lines):
    # if we have reached a new section or finished a section
    if "% TEMPLATE SECTION" in line:
        # add the index to the list
        templateIndexes.append(i+1)
# [1, 49, 68, 107, 255, 257]

# we want to view where each section starts/ends
# so we want 0&1, 2&3, 4&5

i = 0
# make sure that the end of the window doesn't go beyond the list
while 2*(i)+1 < len(templateIndexes):
    # section start
    start = templateIndexes[2 * i]
    # section end
    end = templateIndexes[2 * i + 1]
    # go through the window and add the lines that have to do with the template
    for j in range(start, end):
        # .strip removes the whitespace
        templateFile.write(lines[j].strip())
        # new line because it is not there by default
        templateFile.write("\n")
    i += 1


# project types: % PROJECTS - WEB DEVELOPMENT, % PROJECTS - IT, % PROJECTS - AI/DATA/SIMULATION
projectTypeHashmap = {0:"% PROJECTS - WEB DEVELOPMENT\n",1:"% PROJECTS - IT\n", 2:"% PROJECTS - AI/DATA/SIMULATION\n"}
# w+ means that we can read and write while being able to overwrite the file
projectFileHashmap = {"% PROJECTS - WEB DEVELOPMENT\n":open("WebDevelopment.tex","w+"),"% PROJECTS - IT\n":open("IT.tex","w+"), "% PROJECTS - AI/DATA/SIMULATION\n":open("AI.tex","w+")}

# go through all of the lines until we find the first line with a section for a project
i = 0
for j in range(len(lines)):
    if "% PROJECTS - " in lines[i]:
        i = j

# make start and end global variables and to not reset them each time
start, end = 0, 0
# fix off by one error
projectNum = -1
# while we are in bounds and we have not reached the bottom template section (Relevant skills)
while i < len(lines) and ("textbf{Relevant Skills}" not in lines[end]):
    # if we have found a new project section
    if "% PROJECTS - " in lines[i]:
        # projectNum represents what project section we are on
        projectNum += 1
        # shift the start and end points
        start = i-1
        end = i+1
        # extend end (expand the window)
        while end < len(lines) and "% PROJECTS - " not in lines[end] and ("textbf{Relevant Skills}" not in lines[end]):
            end += 1
    
    # OLD CODE - not needed because: we expand the window, but leave i where it is
    # while start < i < end:

        # what is the type of project we are working on?
        project = projectTypeHashmap[projectNum]
        # what is the file we are working on
        projectFile = projectFileHashmap[project]
        # go through each line in the window
        for j in range(start, end):
            projectFile.write(lines[j].strip() + "\n")
        # we are done with this window, so move i at the end to continue
        i = end
    # 
    else:
        i += 1

# go through each project
with open("templateFile.tex","w+") as templateFile:
    templateFileLines = templateFile.readlines()

templateFileLinesBeforeInsert = (templateFileLines[:-3])
templateFileLinesAfterInsert = (templateFileLines[-3:])


for project in projectFileHashmap:
    # what file do we need to open
    filePath = str(projectFileHashmap[project].name)[:-4] + "fullProjectFile.tex"
    with open(filePath, "w+") as fullFile:
        # add all of the lines
        for line in templateFileLinesBeforeInsert:
            fullFile.write(line)
    
        # what file are we going to write to?
        file = projectFileHashmap[project]
        file.seek(0)  # move to the beginning of the file
        lines = file.readlines()
        for line in lines:
            fullFile.write(line)
        
        relevantSkillsHeader = [r"% RELEVEANT SKILLS", r"\textbf{Relevant Skills}", r"\vspace{-10pt}", r"\newline", r"\rule{\textwidth}{0.4pt}"]
        for relevantSkillLine in relevantSkillsHeader:
            fullFile.write(str(relevantSkillLine)+"\n")

# pattern that lets us remove punctation
pattern = r'[^a-zA-Z0-9\s/]'

# make a hashmap with each file
# for file in projectFileHashmap.values()

def collectSkills(curFile):
    skillSections = {
        ("LANGUAGE",r"\textbf{Languages}: "):set(), 
        ("FRAMEWORK",r"\textbf{Frameworks}: "):set(), 
        ("TOOL",r"\textbf{Tools}: "):set(), 
        ("LIBRARIES/APIS",r"\textbf{Libraries/APIs}: "):set()
    }
    with open(curFile, "r+") as f:
        lines = f.readlines()

    # go through each line
    for i,line in enumerate(lines):
        # if we come across a language
        if r"% LANGUAGE" in line:
            # get the next line
            nextLine = lines[i+1]
            # clean the line by removing any punctation
            cleanedNextLine = re.sub(pattern, '', nextLine).strip()
            skillSections[("LANGUAGE",r"\textbf{Languages}: ")].add(cleanedNextLine)
        # if we come across a framework
        elif r"% FRAMEWORK" in line:
            nextLine = lines[i+1]
            cleanedNextLine = re.sub(pattern, '', nextLine).strip()
            skillSections[("FRAMEWORK",r"\textbf{Frameworks}: ")].add(cleanedNextLine)
        # if we come across a tool
        elif r"% TOOL" in line:
            nextLine = lines[i+1]
            cleanedNextLine = re.sub(pattern, '', nextLine).strip()
            skillSections[("TOOL",r"\textbf{Tools}: ")].add(cleanedNextLine)
        # if we come across a library/api
        elif r"% LIBRARIES/APIS" in line:
            nextLine = lines[i+1]
            cleanedNextLine = re.sub(pattern, '', nextLine).strip()
            skillSections[("LIBRARIES/APIS",r"\textbf{Libraries/APIs}: ")].add(cleanedNextLine)
    return skillSections

for file in projectFileHashmap.values():
    # hashmap to store elements for 4 sections of relevant skills
    filePath = str(file.name)[:-4] + "fullProjectFile.tex"
    skillSections = collectSkills(filePath)
    

    filePath = str(file.name)[:-4] + "fullProjectFile.tex"
    with open(filePath, "a+") as fullFile:
        for skill in skillSections:
            fullFile.write(skill[1])
            for values in skillSections[skill]:
                fullFile.write(str(values) + ", ")
            fullFile.write("\n")

        # add last 3 lines to close document
        for line in templateFileLinesAfterInsert:
            fullFile.write(line)