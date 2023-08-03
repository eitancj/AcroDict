## Classes for storing the Acronym Dictionaries as objects ##
## Used by main program AcroDict.py in the same folder ##

class acroDict:
    def __init__(self, fileName, name, description = None):
        self.fileName = fileName
        self.name = name
        self.description = description
        self.acronyms = {}
        self.empty = True
        #print(f'name: {self.name}, description: {self.description}. Created.')

    #def reloadDict(self):
    #    try:
    #        with open(self.fileName, 'r'):
    #            if {self.acronyms}
    #    except Exception as e:
    #        print (f"\nException while reading file '{self.fileName}' for dictionary '{self.name}'.\n")


    def addAcronym(self, acronym):                             # acronym is a dictionary key-value pair
        try:
            self.acronyms.update(acronym)
            #print(f"{acronym} added to the '{self.name}' dictionary.")
        except Exception as e:
            print(f"Exception received: {e}")

    def remAcronym(self, acronym):
        #try:
        #    del self.acronyms[acronym]
        #except Exception as e:
        #    print(f"Exception received: {e}")
        print ('')



    def countAcronyms(self):
        return len(self.acronyms)
    
    def listAcronyms(self):
        c = self.countAcronyms()
        print(end='--> ')
        for i,acronym in enumerate(self.acronyms):
            if i+1 < c:
                print (acronym + ', ', end='')
            else:                                               # last acronym in list skip comma
                print (acronym)
        return self.acronyms
        
    def showMeaning(self, userAcro):
        # display all acronym-meaning pairs in dictionary
        if userAcro.lower() != 'a':
            print (f"--> {userAcro} — {self.acronyms.get(userAcro)}")
        else:
        # display specified acronym-meaning pair
            for acronym,meaning in sorted(self.acronyms.items()):
                print(f"--> {acronym} – {meaning}")