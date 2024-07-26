import pickle

class serverDatabase:

    databaseName = ""

    yearDict = {}
    faceDict = {}

    def __init__(self, name:str):
        self.databaseName = name
        

    #name is the name of the database
    #fileLocation is the file location of the data we want to import (w/ \\ at end)\
    #fileName is the name given to the file before save (aka PUSSY)
    #REMEMBER: THERE MUST BE TWO FILES, -dates and -faces!!!
    def __init__(self, name:str, fileLocation:str, fileName:str):
        try:
            self.databaseName = name
            if fileLocation == None:
                self.yearDict = {}
                self.faceDict = {}
            else:
                with open(fileLocation+fileName+"-dates.pkl", 'rb') as yearFile:
                    self.yearDict = pickle.load(yearFile)
                with open(fileLocation+fileName+"-faces.pk1", 'rb') as faceFiles:
                    self.faceDict = pickle.load(faceFiles)
        except FileNotFoundError:
            return
        except:
            print("SERVER ERROR: In Server constructor!")
            return

    #row is an array of [pathToFile, faces] strs
    def addTo(self, row):
        self.addDate(row)
        self.addFace(row)
        return True

    #row should be an array w/ [path(str)]
    def addDate(self, row):
        date = row[0].split("\\")[-4:-1] #uses the path to get [year, month, day]
        if date[0] in self.yearDict:
            tempDict = self.yearDict[date[0]]
            #if month in dictionary of year
            if date[1] in tempDict:
                tempDict = tempDict[date[1]]
                #if day is in month dict
                if date[2] in tempDict:
                    self.yearDict[date[0]][date[1]][date[2]].append(row)
                else:
                    self.yearDict[date[0]][date[1]].update({date[2]:[row]})
            else:
                self.yearDict[date[0]].update({date[1]:{date[2]:[row]}})
        else:
            self.yearDict.update({date[0]:{date[1]:{date[2]:[row]}}})

    #date format should be YEAR-MONTH-DAY FOLLOW IT DIBSHIT!!!
    def getDate(self, date:str):
        date = date.split("-")
        try:
            return self.yearDict[date[0]][date[1]][date[2]].copy()
        except KeyError:
            return None
        except:
            print("SERVER ERROR: getRow function had an issue w/ "+date+".")
            return None
        
    def getAllDates(self):
        result=[]
        years=list(self.yearDict.keys())
        years.sort()
        for year in years[1:]:
            months=list(self.yearDict[year].keys())
            months.sort()
            for month in months:
                days=list(self.yearDict[year][month].keys())
                days.sort()
                for day in days:
                    result=result+self.yearDict[year][month][day]
        return result
        
    def getName(self):
        return self.databaseName
    
    def addFace(self, row:str):
        if(row[1]==None):
            return
        faces = row[1].split("-")
        for face in faces:
            if face in self.faceDict:
                self.faceDict[face].append(row)
            else:
                self.faceDict.update({face:[row]})

    def getFace(self, name:str):
        try:
            return self.faceDict[name]
        except KeyError:
            return None
        except:
            print("SERVER ERROR: getFace function had an issue w/ "+name+".")
            return
        
    
    #name is the name of the file (no .pkl)
    #fileLocation is a valid file location!!!! w/ \\ at end
    #raises exception when save failed!
    def saveTable(self,name:str, fileLocation:str):
        try:
            with open(fileLocation+name+"-dates.pkl", 'wb') as fileSave:
                pickle.dump(self.yearDict, fileSave)
            with open(fileLocation+name+"-faces.pk1", "wb") as fileSave:
                pickle.dump(self.faceDict, fileSave)
        except:
            raise Exception