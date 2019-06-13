##------------------------------------------------------------------
##
## Pose Library Personal Project (UI)
##
## v-002
##------------------------------------------------------------------

import PoseLibrary
reload(PoseLibrary)

import pymel.core as pm
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui


def getMayaMainWindow():
    window = omui.MQtUtil_mainWindow()
    pointer = wrapInstance(long(window), QtWidgets.QMainWindow)
    return pointer

def getDock(name='poseLibraryDock'):
    deleteDock(name)
    ctrl  = pm.workspaceControl(name, ttc=("AttributeEditor", -1), label='Pose Library')
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    pointer = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return pointer

def deleteDock(name='poseLibraryDock'):
    if pm.workspaceControl(name, query=True, exists=True):
        pm.deleteUI(name)

##--------------------------------------------------
## Pose Library UI Main Class
##--------------------------------------------------
class PoseLibraryUI(QtWidgets.QWidget):
    def __init__(self, dock=True):
        if dock:
            parent = getDock()

        else:
            deleteDock()

            try:
                pm.deleteUI('poseLibraryTool')
            except:
                print 'hello'

            parent = QtWidgets.QDialog(parent = getMayaMainWindow())

            parent.setObjectName('poseLibraryTool')
            parent.setWindowTitle('Pose Library')
            layout = QtWidgets.QVBoxLayout(parent)

        super(PoseLibraryUI, self).__init__(parent=parent)


        _libraries = self.ClipLibrariesWidgets()
        _applyItem = self.ApplyClipWidget()

        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()

    '''
    Description:
            -MainLayout initialize
            -Buttons Layout
            -Methods declaration
            -Creation of 3 buttons
    
    '''
    def ClipLibrariesWidgets(self):
        self._libraryCore = PoseLibrary.poseLibrary()
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.libraries = QtWidgets.QComboBox()
        self.populateLibraries()

        createButton = QtWidgets.QPushButton("Create New Folder....", parent=self)
        createButton.clicked.connect(self.on_CreateLibrary)

        reloadButton = QtWidgets.QPushButton("Reload Poses", parent=self)
        reloadButton.clicked.connect(self._populate)

        deleteButton = QtWidgets.QPushButton("Delete Pose", parent=self)
        deleteButton.clicked.connect(self.on_DeleteLibrary)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)

        self.mainLayout.addWidget(btnWidget)

        btnLayout.addWidget(self.libraries)
        btnLayout.addWidget(createButton)
        btnLayout.addWidget(reloadButton)
        btnLayout.addWidget(deleteButton)

        #Limit of Create,Reload and Delete Buttons

        iconSize = 150

        self._listWidget = QtWidgets.QListWidget()
        self._listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self._listWidget.setIconSize(QtCore.QSize(iconSize,iconSize))
        self._listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)

        lstWidget = QtWidgets.QWidget()
        lstLayout = QtWidgets.QVBoxLayout(lstWidget)
        self.mainLayout.addWidget(lstWidget)

        lstLayout.addWidget(self._listWidget)

    '''
    Description:
            Apply Pose and Create New Pose init 
    '''
    def ApplyClipWidget(self):

        self._apply = QtWidgets.QPushButton("Apply Pose", parent=self)
        self._apply.clicked.connect(self._load)

        self._create = QtWidgets.QPushButton("Create New Pose", parent=self)
        self._create.clicked.connect(self._save)

        clipWidget = QtWidgets.QWidget()
        clipLayout = QtWidgets.QHBoxLayout(clipWidget)
        self.mainLayout.addWidget(clipWidget)

        clipLayout.addWidget(self._apply)
        clipLayout.addWidget(self._create)


    '''
    Description:
           Populate the ListWidget with the icons(screenshot)
    
    '''

    def _populate(self):

        self._listWidget.clear()

        hg = self.askIndex()
        self._libraryCore.poseFind(hg)

        for name, info in self._libraryCore.items():

            item = QtWidgets.QListWidgetItem(name)
            self._listWidget.addItem(item)

            screenshot = info.get('screenshot')

            if screenshot:

                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
    '''
    Description:
           Look for the name of the icons/pose in the poseImport method 
           this method is used by the Apply Pose
    
    '''
    def _load(self):
        direc = self.askIndex()
        currentItem = self._listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        self._libraryCore.poseImport(name,direc)

    '''
    Description:
           Pop up a little window to
           save a new pose in the given pose folder
    '''
    def _save(self):

        direc = self.askIndex()

        poseName, ret = QtWidgets.QInputDialog.getText(self, "Create New Pose", "Pose name")

        if ret:
            newName = self._libraryCore.poseExport(poseName, direc)

    '''
    Description:
           Pop up a little window to
           create a new folder 
    '''
    def on_CreateLibrary(self):
        libraryName, ret = QtWidgets.QInputDialog.getText(self, "Create New Library", "Library name")

        if ret:
            newLibrary = self._libraryCore.createLibrary(libraryName)
            self.folders.append(libraryName)
            self.libraries.clear()
            for x in self.folders:
                self.libraries.addItem(str(x))

    '''
    Description:
           Populates the combobox with the pose folders 
    '''
    def populateLibraries(self):

        self.libraries #this is the qtwidget.combobox

        self.coreLib = PoseLibrary.poseLibrary()

        self.folders = []

        for folder in self.coreLib.directoryLib():
            self.appendLibrary(folder)

    '''
    Description:
           Add the libraries to the combobox widget
           
    Input Argument:
        library        the name of the library folder 
    '''
    def appendLibrary(self, library):

        self.folders.append(library)
        self.libraries.addItem(str(library))

    '''
    Description:
           Ask for the name of the current library to look for it the find folder methos
           
    '''
    def askIndex(self):

        vr = self.libraries.currentText()
        vl = self.coreLib.findFolder(vr)
        return vl

    '''
    Description:
           Delete library 
           
    '''
    def on_DeleteLibrary(self):
        currentItem = self._listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()

        folderName= self.askIndex()

        gg= self.coreLib.listFolderItems(folderName, name)

        self._populate()
