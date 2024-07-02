import server

def controller(processQueue, serverIntializedEvent, returnQueue):

    while(True):
        initArr = processQueue.get()
        if(initArr[0] == "N"):
            try:
                serverObject = server.serverDatabase("New", None, None)
                break
            except:
                print("Bad Server Initialization, try again.")
        elif(initArr[0] == "O"):
            try:
                serverObject = server.serverDatabase("New", initArr[1], initArr[2])
                break
            except:
                print("Bad Server Initialization, try again.")
        elif(initArr[0] == "Q"):
            exit()
        else:
            print("Bad Server Initialization, try again.")

    serverIntializedEvent.set()

    #replace input w/ queue of arrays, each array has command (char) + filename/whatever else is needed!
    while(True):
        #wait for input from queue
        serverInput = processQueue.get()

        #FindFace
        if(serverInput[0].upper() == "FF"):
            result = serverObject.getFace(serverInput[1])
            returnQueue.put(result)

        #FindDate
        elif(serverInput[0].upper() == "FD"):
            result = serverObject.getDate(serverInput[1])
            returnQueue.put(result)

        #Add Data
        elif(serverInput[0].upper() == "AD"):
            serverObject.addTo(serverInput[1])

        #Stop server
        elif(serverInput[0].upper() == "Q"):
            print("DATABASE: Stopping Database")
            serverIntializedEvent.clear()
            break

        #Save function
        elif(serverInput[0].upper() == "S"):
            try:
                serverObject.saveTable(fileLocation=serverInput[1],name=serverInput[2])
                print("SERVER: Save Successful")
            except FileNotFoundError:
                print("SERVER ERROR: File Location not accessible")
            except:
                print("SERVER ERROR: Save unsuccessful")
        
        
        else:
            print("SERVER ERROR: Bad input with: "+serverInput)




#OLD CODE

        # userInput = input("Please enter your desired command: [f]-getFace, [s] - save [q]-quit")
        # if(userInput == "f"):
        #     userRequest = input("Please enter the face of the desired person: ")
        #     result = serverObject.getFace(userRequest)
        #     if(result == None):
        #         print("Person not found")
        #     else:
        #         print(result)
        # elif(userInput == "q"):
        #     print("Stopping Server")
        #     serverIntializedEvent.clear()
        #     break
        # elif(userInput == "s"):
        #     while(True):
        #         try:
        #             filesaveLocation = input("Enter location of save")
        #             filesaveName = input("Name of file")
        #             serverObject.saveTable(filesaveName, filesaveLocation)
        #         except:
        #             print("Save failed, please try again!")
        # else:
        #     print("Invalid command try again!")


# userHistory = input("Would you like to use a database or create a new one? (n = new, o = old)").upper()
# if(userHistory=="N"):
#     serverObject = server.serverDatabase("New", None, None)
#     break
# elif(userHistory == "O"):
#     try:
#         fileLocation= input("What is the file location (don't forget \\ at end!)")
#         fileName = input("What is the file name?")
        
#         break
#     except:
#         print("Input failed, try again!")
#         pass
# else:
#     print("Bad input, try again")