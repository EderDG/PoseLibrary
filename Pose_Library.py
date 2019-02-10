import pymel.core as pm
import json

class poseLibray(object):

    def __init__(self):

        self.mainData = {}

        self.path = 'C:/Users/ALIEN/Desktop/control_Info.json'

        self.keyword = 'CON'

        #self.mainExport()

        self.mainImport()


    def mainExport(self):

        controlOnScene = self.controlFilter()
        coordinates = ['X','Y','Z']

        for x in controlOnScene:

            valueDic={}

            parsedControl = str(x.split('|')[-1])

            if parsedControl not in self.mainData:
                self.mainData[parsedControl]=[]

            for coor in coordinates:

                attrTranslate = getattr(x,'translate' + coor)
                parsedTrans ='translate' + coor

                attrRotate = getattr(x, 'rotate' + coor)
                parsedRotate ='rotate' + coor

                attrScale = getattr(x, 'scale' + coor)
                parsedScale='scale' + coor


                if attrTranslate.get(k=True) and not attrTranslate.get(lock=True) and not attrTranslate.get(cb=True):


                    attrValue=attrTranslate.get()

                    valueDic[parsedTrans]=attrValue

                else:
                    pass

                if attrRotate.get(k=True) and not attrRotate.get(lock=True) and not attrRotate.get(cb=True):


                    attrValue=attrRotate.get()

                    valueDic[parsedRotate]=attrValue

                else:
                    pass
                if attrScale.get(k=True) and not attrScale.get(lock=True) and not attrScale.get(cb=True):


                    attrValue=attrScale.get()

                    valueDic[parsedScale]=attrValue

                else:
                    pass


            self.mainData[parsedControl].append(valueDic)



        with open(self.path, 'w') as out_file:

            json.dump(self.mainData, out_file)


    def mainImport(self):


        with open(self.path) as File:
            self.mainData = json.load(File)

        ctrlsOnScene = self.controlFilter()


        for pyCtrl in ctrlsOnScene:

            transformCtrl= str(pyCtrl)

            if transformCtrl in self.mainData:

                for transform in range(len(self.mainData[transformCtrl])):

                    transX=self.mainData[transformCtrl][transform]['translateX']
                    transY=self.mainData[transformCtrl][transform]['translateY']
                    transZ=self.mainData[transformCtrl][transform]['translateZ']

                    pyCtrl.translateX.set(transX)
                    pyCtrl.translateY.set(transY)
                    pyCtrl.translateZ.set(transZ)





    def controlFilter(self):

        listCtrl = []

        for c in pm.ls(et='nurbsCurve', long=True):

            parentCtrl = c.getParent()

            if parentCtrl.find(self.keyword)!=-1 and parentCtrl not in listCtrl:

                listCtrl.append(parentCtrl)

        return listCtrl

test=poseLibray()
