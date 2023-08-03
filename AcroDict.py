### Acronym Lookup Tool ###
# Python 3.11.4 #

# Modules
from classes import acroDict
import os
import re

# Contstants
nameFmt = re.compile(r"^#\s*name\s*:\s*\w{1}[\w\-_—\+\=\%\*\#!¡@;\~\'\"\$\^&*\(\)\{\}\[\€\s]{0,99}$", re.IGNORECASE) # '# name : <name for acronym-dictionary>' specifying name for new acroDict inside the acro-list file. 'r' makes python treat the RE string as raw, preventing thus errors.
descFmt = re.compile(r"^#\s*description\s*:\s*[\w\W]+.*$", re.IGNORECASE) # '# description : <description for acronym-dictionary>' specifying name for new acroDict inside the acro-list file
acropairFmt = re.compile(r"^\s*[\w\/\\\-_!\&]+\s*:\s*\w+[\s\w\/\\\-\_!\'\,\.;\(\)\[\]\{\}\&]*$", re.IGNORECASE) # '# <key name> : <value pair>' accepted format for the acronym-meaning key-value pair; where key- and name must be comprised alphanumerical characters with possible spaces and a few exceptions for special characters. 
acroDictionaries = {}

# Functions

def exitProgram(err = '', msg = ''):
    if msg: print(f"\n¡Custom error received!\n{msg}")
    if err:
        print(f"\n¡Interpreter error received!")
        raise err
    quit(999)                                                       # will apply when only 'msg' was given, since 'raise' will quit anyhow

def exitNicely():
    print ("\nThanks for using AcroDict!\n")
    quit(0)

def setUpDirs():
    scriptPath = os.path.abspath(__file__)
    scriptDir = os.path.dirname(__file__)
    origWD = os.getcwd()
    try:
        os.chdir(scriptDir) # change directories to the py-script's parent dir
    except Exception as e:
        exitProgram(e, f"Failed to change directories to '{scriptDir}'")
    WD = os.getcwd()
    global acroDir
    acroDir = os.path.join(WD, 'acroDir')
    #print (f'\norigWD: {origWD}\ncurWD: {WD}\nacroDir: {acroDir}\nscriptPath: {scriptPath}\n')

def findDictFiles():
    # find acronym-list files in the acronym directory
    global acroDir
    try:
        acroFiles = os.scandir(acroDir)
    except NotADirectoryError and FileNotFoundError as e:
        exitProgram(e, f"'{acroDir}' is not a valid directory.")
    except Exception as e:
        exitProgram(e)

    # parse found files
    for acroFile in acroFiles:
        name = acroFile.name; size = acroFile.stat().st_size
        if acroFile.is_file() and size > 0 and name.endswith('txt'):
            createDictObject(acroFile)

def createDictObject(file):
    # open file for reading and prepare for parsing 
    with open(file.path, 'r') as txt:                                          # 'with' automatically closes the opened file once block is done – even if there's been an exception. Another longer way would be a try block, with a 'finally:' statement at the end where a file.close() would make sure to close the file.
        settledName = False
        settledDesc = False
        tmpList = []

        # parse lines
        for line in txt.readlines():
            if line.isspace():
                continue

            # check if a name for the acronym dictionary is mentioned in the file
            if not settledName:
                m = nameFmt.match(line.strip())
                if m:
                   global newDictName                                                                 # if there's a specific name for the acroDict was specified in the file's 1st line in the expected format, use it
                   newDictName = (m.string.split(':')[1].strip())
                   settledName = True
                   continue
                    
            # check if a description for the acronym dictionary is mentioned in the file
            if not settledDesc:
                m = descFmt.match(line.strip())
                if m:
                   global newDictDesc                                                                 # if there's a specific name for the acroDict was specified in the file's 1st line in the expected format, use it
                   newDictDesc = (m.string.split(':')[1].strip())
                   settledDesc = True
                   continue
                    
            # validate and process the acronym
            m = acropairFmt.match(line.strip())
            if m:
               acronym = (m.string.split(':')[0].strip())
               meaning = (m.string.split(':')[1].strip())
               tmpList.append({acronym:meaning})
                
        # create a new acroDict object if this file has been deemed valid
        if not settledName:
            newDictName = file.name.split('.')[0]                                # won't work if file-name contains several dots. But I would need regex with if-else clauses (to avoid errors) to get around that and... no thanks.
        if not settledDesc:
            newDictDesc = ''
            #newDictDesc = f"a list of acronyms related with {newDictName}"
        global acroDictionaries
        acroDictionaries[newDictName] = acroDict(file.name, newDictName,newDictDesc)   # create a acrodictionary object
                
        for acropair in tmpList:
           acroDictionaries[newDictName].addAcronym(acropair)
           if acroDictionaries[newDictName].empty == True:
                acroDictionaries[newDictName].empty = False

def validateAnswer(whichMenu, answer, args = None):
    #print (f"\n\tvalidateAnswer: whichMenu-{whichMenu}, answer-{answer}, args-{args}\n")
    validArr = ['q']
    
    # valid options for the Dictionary Menu
    if whichMenu == 'dictMenu':
        validArr.extend(range(1, len(acroDictionaries)+1))
    
    # valid options for the Acro menu
    elif whichMenu == 'acroMenu':
        validArr.extend(['m', 'a'])
        if args is None or args == {} or args == '':
            print ('Dictionary is empty.')
        else:
            validArr.extend(args)  
    validArr = str(validArr).replace("'",'').strip()

    # insist on a valid answer from the user
    while answer not in validArr or answer.isspace() or not answer:
        answer = str(input(f'\nPlease enter a valid answer {validArr}\n'))
    
    # if q, exit nicely
    if answer.lower() == 'q':
        exitNicely()
    # otherwise, return answer
    else:
        return answer

def dictMenu():
    #print (f"\n\tdictMenu\n")
    # get user's choice
    print ('\nAvailable Acronym Dictionaries:')
    indexnameDict = {}
    for index,(dictName,dictObject) in enumerate(acroDictionaries.items()): # the enumerate method displays index of each list/dictionary member
        indexnameDict[str(index+1)] = dictName
        acroCount = dictObject.countAcronyms()
        # print the dictionary-menu options
        if dictObject.description == '':
            print (f"{index+1}\t{dictName} [{acroCount}]")
        else:
            print (f"{index+1}\t{dictName} ({dictObject.description}) [{acroCount}]")
      
    # validate and process user's choice
    chosenMenu = str(input('\n<dictionary number>\tq (quit)\n'))
    validMenu = validateAnswer('dictMenu', chosenMenu)
    
    # return user's acroDict object
    return acroDictionaries[indexnameDict[validMenu]] 

def acroMenu(dictionary):
    #print (f"\n\tacroMenu: dictionary-{dictionary.name}\n")
    
    # handle empty dictionaries
    if (dictionary.countAcronyms() == 0):
        print (f"\nDictionary '{dictionary.name}' is empty.")
        print (f"Type in 'add' to start adding acronyms to it, or select a different dictionary.\n")
        return True
    
    validAcro = 'not m'
    # keep offering acronym interpretation until otherwise told (*'q' is processed inside validateAnswer)
    while validAcro not in ('m'):
     
        # display available acronyms and the acronym menu
        print (f"\nShowing acronyms for {dictionary.name}:")
        acronyms = dictionary.listAcronyms()

        # process user's answer
        chosenAcro = str(input("\n<acronym>\ta (all acronyms)\tm (main menu)\tq (quit)\n"))
        validAcro = validateAnswer('acroMenu', chosenAcro, acronyms)
        print ('')

        # go back to main dictionary menu if user has pressed m
        if validAcro == 'm':
            return True
        # otherwise display whatever the user has asked for
        else:
            dictionary.showMeaning(validAcro)
            print ('')  
    
    # Go back to main function and end program
    return False 


# Main

def main():

    # set up working- and acroDict- directories
    setUpDirs()

    # greet
    print ('\n******** AcroDict ********')
    print ('#   your acronym guide   #')
    print ('*** LOL *** AD *** FYI ***\n')
    
    # process existing dictionaries 
    findDictFiles()
    
    # loop the main menu until told otherwise
    keepGoing = True
    while keepGoing:
        #print (f"\n\tkeepGoing Main Menu\n")
        # display available dictionaries, if any
        if len(acroDictionaries) == 0:
            print ("No acro-dictionaries are available at this moment.")
            print ("Please try again later.\n")
            exitNicely()
        else:
        # send to dictionary menu
            chosenDict = dictMenu()
        # send to acronym menu
            keepGoing = acroMenu(chosenDict) # pass on the validated dictionary object

main()

print ("\nTNT\n(till next time;D)\n")