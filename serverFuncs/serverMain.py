import multiprocessing as mp
import serverController
import serverUserInterface
import bulkConverter

if __name__ == '__main__':
    processManager = mp.Manager()
    
    startEvent = processManager.Event()
    processQueue = processManager.Queue()
    returnQueue = processManager.Queue()

    databaseProcess = mp.Process(target=serverController.controller, args=(processQueue, startEvent, returnQueue))
    userInterfaceProcess = mp.Process(target=serverUserInterface.main, args=(processQueue, startEvent, returnQueue))
    bulkImporter = mp.Process(target=bulkConverter.Importer,args=(processQueue, startEvent))

    databaseProcess.start()
    userInterfaceProcess.start()
    bulkImporter.start()

    bulkImporter.join()
    print("MAIN: BULK IMPORTER DONE")

    databaseProcess.join()
    userInterfaceProcess.join()

    print("MAIN: SHUTTING DOWN")