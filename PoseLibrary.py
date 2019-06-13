
##------------------------------------------------------------------
##
## Pose Library Personal Project
##
## v-002
##------------------------------------------------------------------


import pymel.core as pm
import json
import os



dirFiles = 'C:/Users/ALIEN/Documents/maya/2018/scripts/PoseLibraryFolder/Presets'

##--------------------------------
## Pose Library Main Class
##--------------------------------

class poseLibrary(dict):
    def __init__(self):

        ## Main Dictionary
        self.mainData = {}

        self.keyword = 'Ctrl'



    '''
    Description:
            By selection export name and position of the animation controls into a .json file
            create a screenshot that later on will be called by the UI
    
    Input Argument:
                name            The name of the .json File
                directory       Directory where the file will be saved
                screenshot      Create the path to save screenshot
    
    Return Value:
        Path, name
   '''
    def poseExport(self, name, directory, screenshot=True):

        path = os.path.join(directory, '%s.json' % name)

        controlOnScene = self.controlFilter()

        for x in range(len(controlOnScene)):

            valueDic = {}

            parsedControl = str(controlOnScene[x].split('|')[-1])

            if parsedControl not in self.mainData:
                self.mainData[parsedControl] = []

            attrLst = pm.listAttr(controlOnScene[x], k=True, u=True)

            for attr in attrLst:
                attrParsed = str(attr)
                attrStr = getattr(controlOnScene[x], attr)
                attrValue = attrStr.get()

                valueDic[attrParsed] = attrValue

            self.mainData[parsedControl].append(valueDic)

        if screenshot:
            self.mainData['screenshot'] = self.poseScreenShot(name, directory=directory)

        with open(path, 'w') as out_file:

            json.dump(self.mainData, out_file)

        return path, name



    '''
    Description:
        From the .json file import all data of the controls 
    
    Input Argument:
        name            The name of the file 
        dictionary      Directory where the files is
    
    '''
    def poseImport(self, name, directory):

        path = os.path.join(directory, '%s.json' % name)

        with open(path) as File:
            self.mainData = json.load(File)

        ctrlsOnScene = self.controlFilter()

        for pyCtrl, pyAttr in self.mainData.iteritems():
            if pyCtrl in ctrlsOnScene:
                for dicAttr, dicValue in pyAttr[0].iteritems():
                    ctrl = pm.PyNode(pyCtrl)
                    attr = getattr(ctrl,dicAttr)
                    attr.set(dicValue)

    '''
    Description:
        To find all the json files in the directory given by the UI in order to populate 
        the icons(screenshots) on the ListWidget in the UI
    
    Input Arguments:
        directory       the directory to look for the json
         
    
    '''
    def poseFind(self, directory):

        self.clear()

        files = os.listdir(directory)#To find json files inside the folder

        jsonFiles = [f for f in files if f.endswith('.json')]#this's call list comperhention

        for j in jsonFiles:

            name, ext = os.path.splitext(j)

            path = os.path.join(directory, j)

            infoFile = '%s.json' % name

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as fl:
                    info = json.load(fl)

            else:
                info = {}

            self[name] = info

    '''
    Description:
        Filter the selected controls and add them in a list
    
    
    Return Values:
        The list with the controls in it
        
    '''
    def controlFilter(self):

        ctrlSel= pm.ls(sl=1)

        listCtrl = []

        for c in ctrlSel:
            if c not in listCtrl:
                listCtrl.append(c)

        return listCtrl


    '''
    Description:
        Create a scene screenshot and save it in the folder given 
    
    Input Arguments:
        directory       directory to save the image
        name            the name given to the image
    
    Return Values:
        the path where the screenshot is
    
    '''
    def poseScreenShot(self, name,directory=dirFiles):

        path = os.path.join(directory, '%s.png' % name)

        pm.modelEditor("modelPanel4", edit=True, allObjects=False)
        pm.modelEditor("modelPanel4", edit=True, polymeshes=True)

        pm.setAttr('defaultRenderGlobals.imageFormat', 32)
        pm.playblast(completeFilename=path, forceOverwrite=True, format='image', width=500,
                     height=400, showOrnaments=False, startTime=1, endTime=1, viewer=False)

        pm.modelEditor("modelPanel4", edit=True, allObjects=True)

        return path

    '''
    Description:
        Create the folder where json and image of the pose will be saved 
    
    Input Arguments:
        directory       directory to create the folder
        name            the name given to the folder
    
    Return Values:
        the path where the screenshot is
    
    '''
    def createLibrary(self, name, directory=dirFiles):

        libraryDirectory = os.path.join(directory, name)

        if name:
            os.mkdir(libraryDirectory)


    '''
    Description:
        List all presets folders that contains the poses and its call it 
        to populate the librariesWidget on the UI  
    
    Input Arguments:
        directory       directory where the folders are
    
    Return Values:
        list of folders
    
    '''
    def directoryLib(self, directory = dirFiles):

        folder = os.listdir(directory)


        return folder

    '''
    Description:
        creates path for the folder   
    
    Input Arguments:
        directory       directory where the folders are
        name            folder name
    Return Values:
        the path with name and directory    
    '''
    def findFolder(self, name, directory=dirFiles):

        path = os.path.join(directory, '%s' % name)

        return path

    '''
    Description:
        create the path to delete the folder on the UI  
    
    Input Arguments:
        directory       directory where the folder is
        name            folder name
    Return Values:
        folder path
    '''
    def listFolderItems(self, dir, name):

        folder = os.listdir(dir)

        for x in folder:
            if x.find(name)!=-1:
                path = os.path.join(dir, '%s' % x)

                os.remove(path)



        return folder
