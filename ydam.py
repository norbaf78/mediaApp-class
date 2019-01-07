"""
/***************************************************************************
Name                    : Ydam
Description          : 
Date                 : 2/Nov/2017/
copyright            : (C) 2011 by Ruggero Valentinotti
email                : valruggero@gmail.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
#from PyQt4 import uic # used in old
#from PyQt4.QtCore import * # used in old
#from PyQt4.QtGui import * # used in old
from PyQt5 import uic # # new for Qgis3
from PyQt5.QtCore import * # new for Qgis3
from PyQt5.QtGui import * # new for Qgis3
from PyQt5.QtWidgets import * # new for Qgis3
from qgis.core import *
from qgis.gui import *
import qgis.utils
import os
import time
#import ws_ydam as ws  #OLD#### NO CLASS
import ws_ydam  # NEW WITH CLASS
import pandas
from functools import partial # new for Qgis3

#import sys
#sys.path.insert(0,'C:\\Users\\fabio.roncato\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\ydam')
#import ws_ydam as ws


class Ydam:
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.distance_max = 50
        self.ws_ydamInstance = ws_ydam.ws_ydam("http://multimedia.trentinonetwork.it", "fabio.roncato@trilogis.it", "Norbaf78_", 20154, 2564504, 0, 72728)
           
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/ydam/icon.png"), "YDAM", self.iface.mainWindow())
        #Add toolbar button and menu item
        #self.iface.addPluginToVectorMenu("&YDAM", self.action)
        self.iface.addPluginToMenu("&SBM-Tools", self.action)
        #self.iface.addToolBarIcon(self.action)
        
        #load the form
        path = os.path.dirname(os.path.abspath(__file__))
        self.dock = uic.loadUi(os.path.join(path, "ui_ydam.ui"))
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        
        self.sourceIdEmitPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())
        #self.sourceIdEmitPoint.setButton(buttonSelectSourceId)
        self.targetIdEmitPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())
        #self.targetIdEmitPoint.setButton(buttonSelectTargetId)
        
        
        #connect the action to each method

#        QObject.connect(self.action, SIGNAL("triggered()"), self.show) # used in old
        self.action.triggered.connect(self.show) # new for Qgis3
#        QObject.connect(self.dock.comboLayers, SIGNAL("currentIndexChanged(int)"), self.updateComboFields) # used in old
        self.dock.comboLayers.currentIndexChanged.connect(partial( self.updateComboFields) ) # new for Qgis3
#        QObject.connect(self.sourceIdEmitPoint, SIGNAL("canvasClicked(const QgsPoint&, Qt::MouseButton)"), self.setPointXY) # used in old
        self.sourceIdEmitPoint.canvasClicked.connect(self.setPointXY)


#        QObject.connect(self.dock.buttonSelectPoint, SIGNAL("clicked(bool)"), self.selectPoint) # used in old
        self.dock.buttonSelectPoint.clicked.connect(partial( self.selectPoint) ) # new for Qgis3
#        QObject.connect(self.dock.buttonRun, SIGNAL("clicked()"), self.run) # used in old
        self.dock.buttonRun.clicked.connect(self.run) # new for Qgis3
#        QObject.connect(self.dock.buttonFiles, SIGNAL("clicked()"), self.selectFiles) # used in old
        self.dock.buttonFiles.clicked.connect(self.selectFiles) # new for Qgis3
#        QObject.connect(self.dock.buttonReload, SIGNAL("clicked()"), self.clear) # used in old
        self.dock.buttonReload.clicked.connect(self.clear) # new for Qgis3
#        QObject.connect(self.dock.buttonHelp, SIGNAL("clicked()"), self.call_help) # used in old
        self.dock.buttonHelp.clicked.connect(self.call_help) # new for Qgis3
#        QObject.connect(self.dock.checkSelectAll,SIGNAL("clicked()"),self.selUnselAllLayers) # used in old
        self.dock.checkSelectAll.clicked.connect(self.selUnselAllLayers) # new for Qgis3
        
# NEW NEW  NEW  NEW  NEW  NEW  NEW  NEW           
        self.dock.maxDistance.valueChanged .connect(self.setDistanceMax)
# NEW NEW  NEW  NEW  NEW  NEW  NEW  NEW          
       
        self.filesList = []
        self.myPoint = None
        self.progressiva = None
        self.asta = None
        self.idrSpIndex = None
        # ydam setting parameters
        self.endpoint = "http://multimedia.trentinonetwork.it"
        self.companyId = 20154
        self.groupId = 2564504
        self.repositoryId = 0
    
       
        #self.dock.lineEditSourceId.setValidator(QIntValidator())
        #self.dock.lineEditTargetId.setValidator(QIntValidator())
               
    def show(self):
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
       
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&SBM-Tools", self.action)
        self.iface.removeDockWidget(self.dock)
        
# NEW NEW  NEW  NEW  NEW  NEW  NEW  NEW   
    def setDistanceMax(self):
        self.distance_max = self.dock.maxDistance.value()
        self.dock.textEditLog.append("DEBUG(Fabio): (setDistanceMax) distance_max: " + str(self.distance_max))
        
    def getDistanceMax(self):
        self.dock.textEditLog.append("DEBUG(Fabio): (getDistanceMax) distance_max: " + str(self.distance_max))
        return self.distance_max
# NEW NEW  NEW  NEW  NEW  NEW  NEW  NEW  

    def getMapCRS(self):
        mapCanvas = self.iface.mapCanvas()
       # mapRenderer = mapCanvas.mapRenderer()  # used in old vedi https://qgis.org/api/api_break.html
       # srs=mapRenderer.destinationCrs() # used in old 
        mapSettings = mapCanvas.mapSettings() # new for Qgis3
        srs=mapSettings.destinationCrs() # new for Qgis3
        return srs

    def transfToWGS(self,point,crsSrc):
        crsDest = QgsCoordinateReferenceSystem(4326)
       # xform = QgsCoordinateTransform(crsSrc, crsDest) # used in old 
        xform = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance()) # new for Qgis3
        point4326=xform.transform(point)
        return point4326

    def getYdamConfig(self):
        user=self.dock.lineEditUser.text()
        password=self.dock.lineEditPass.text()
        endpoint=self.dock.lineEditEndpoint.text()
        companyid=self.dock.lineEditCompanyid.text()
        groupid=self.dock.lineEditGroupid.text()
        repositoryid=self.dock.lineEditRepositoryid.text()
        parentfolder=self.dock.lineEditParentfolder.text()
        YdamConfig={'user':user,'password':password,'endpoint':endpoint,'companyid':companyid,
                    'groupid':groupid,'repositoryid':repositoryid,'parentfolder':parentfolder}
        return YdamConfig

    def updateComboLayers(self):
        self.dock.textEditLog.append("DEBUG(Fabio): updateComboLayers(self) started")
        #populate the combo with vector layers
        self.dock.comboLayers.clear()
        mapCanvas = self.iface.mapCanvas() 
        self.dock.textEditLog.append("DEBUG(Fabio): (updateComboLayers) Number of layer: " + str(mapCanvas.layerCount()))
        for i in range(mapCanvas.layerCount()):
            layer = mapCanvas.layer(i)
          #  if ( layer.type() == layer.VectorLayer  ) and (layer.geometryType() == QGis.Line): # used in old
            if ( layer.type() == layer.VectorLayer  ) and (layer.geometryType() == QgsWkbTypes.LineGeometry): # new for Qgis3
                self.dock.comboLayers.addItem(layer.name(),layer.id())
           # index = self.dock.comboLayers.findText("idrfiu_tt", Qt.MatchFixedString)
            index = self.dock.comboLayers.findText("Idrografia", Qt.MatchFixedString)
            if index >= 0:
                self.dock.comboLayers.setCurrentIndex(index)
                self.dock.textEditLog.append("DEBUG(Fabio): layer find at index: " + str(index))
        self.dock.textEditLog.append("DEBUG(Fabio): updateComboLayers(self) terminated")


    def updateComboFields(self, index):
        self.dock.comboFields.clear()
        self.dock.comboFields.addItem("")
        self.dock.textEditLog.append("DEBUG(Fabio): index: " + str(index))
        activeLayerID = str(self.dock.comboLayers.itemData(index))
       # layer = QgsMapLayerRegistry.instance().mapLayer(activeLayerID) # used in old
        layer = QgsProject.instance().mapLayer(activeLayerID) # new for Qgis3
        if layer:
           # fields = layer.pendingFields() # used in old
            fields = layer.fields() # new for Qgis3
            for field in fields:
                #QMessageBox.warning(self.dock, self.dock.windowTitle(),str(field.typeName()))
                self.dock.textEditLog.append("DEBUG(Fabio): layer.fields(): " + str(field.name()) + "- " + str(field.typeName()))
## funziona solo se metto "varchar(20)"
                if field.typeName() == 'String' or field.typeName() == 'varchar(20)' or field.typeName() == 'char' or field.typeName() == 'text' or field.typeName() == 'TEXT':
                 ##if field.typeName() == 'String' or field.typeName() == 'varchar()' or field.typeName() == 'char' or field.typeName() == 'text' or field.typeName() == 'TEXT':
                    self.dock.comboFields.addItem(field.name())
                    self.dock.textEditLog.append("DEBUG(Fabio):  self.dock.comboFields.addItem(field.name()): " + str(field.name()))
            index = self.dock.comboFields.findText("classid", Qt.MatchFixedString)
            if index >= 0:
                self.dock.comboFields.setCurrentIndex(index)

    def updateLineEditData (self):
        self.dock.lineEditData.setText(time.strftime("%Y%m%d"))

    def selectFiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        #dlg.setFilter("Immagini (*.png *.tif *.jpg);;Documenti (*.odt *.pdf);;CAD (*.dxf)") # used in old
        #dlg.setNameFilters(["Immagini (*.png *.tif *.jpg)", "Documenti (*.odt *.pdf)", "CAD (*.dxf)"]) # new for Qgis3 but cancelled to enable differt types of files
        self.dock.textEditLog.append("DEBUG(Fabio): Please select file ") 
        if dlg.exec_():
            self.filesList = dlg.selectedFiles()
            self.dock.textEditLog.append("DEBUG(Fabio): Selected files " + str(self.filesList)) 

    def getIdrografia(self):
        if self.dock.comboLayers.currentText()=='':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'WARNING: Seleziona layer idrografia!\n')
            return        
        if self.dock.comboFields.currentText()=='':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'WARNING: Seleziona classid di idrografia!\n')
        activeLayerID = str(self.dock.comboLayers.itemData(self.dock.comboLayers.currentIndex()))
     ##  layer = QgsMapLayerRegistry.instance().mapLayer(activeLayerID) # used in old
        layer = QgsProject.instance().mapLayer(activeLayerID) # new for Qgis3
        if layer:
            if self.idrSpIndex == None:    
                self.idrSpIndex = QgsSpatialIndex(layer.getFeatures())
            #nearestIds = self.idrSpIndex.nearestNeighbor(self.myPoint,5) # we need only five neighbour
         #  intersectsIds = self.idrSpIndex.intersects(QgsGeometry.fromPoint(self.myPoint).buffer(50,-1).boundingBox())  # used in old
     ###############       intersectsIds = self.idrSpIndex.intersects(QgsGeometry.fromPointXY(self.myPoint).buffer(self.distance_max,-1).boundingBox())  # new for Qgis3
            intersectsIds = self.idrSpIndex.intersects(QgsGeometry.fromPointXY(self.myPoint).buffer(self.getDistanceMax(),-1).boundingBox()) # new for Qgis3
            self.dock.textEditLog.append("DEBUG(Fabio): getIdrografia(self)  len(intersectsIds): " + str(len(intersectsIds))) 
            if len(intersectsIds) >0:
                request=QgsFeatureRequest().setFilterFids(intersectsIds)
                features = layer.getFeatures(request)
                nearestFtr = QgsFeature()
                dista=100.0
                for feature in features:
               #     myDista=QgsGeometry.distance(QgsGeometry.fromPoint(self.myPoint),feature.geometry()) # used in old
                    myDista=QgsGeometry.distance(QgsGeometry.fromPointXY(self.myPoint),feature.geometry()) # new for Qgis3
                    if myDista<dista:
                        nearestFtr=feature
                        dista=myDista
                features.nextFeature(nearestFtr)
                attrs = nearestFtr.attributes()
              #  myAsta=attrs[layer.fieldNameIndex(self.dock.comboFields.currentText())] # used in old
                myAsta=attrs[layer.dataProvider().fieldNameIndex(self.dock.comboFields.currentText())] # new for Qgis3
                self.asta=myAsta[:10]        
                expr = QgsExpression( " \"{}\" ILIKE '{}%' ".format(self.dock.comboFields.currentText(),self.asta) )
                features = layer.getFeatures( QgsFeatureRequest( expr ) )
                crs = layer.crs().toWkt()
                geom = QgsGeometry.fromWkt('GEOMETRYCOLLECTION()')
                for feat in features:
                    geom = geom.combine(feat.geometry())
                geom.mergeLines()
             #   self.progressiva = str(int(round((geom.length()-geom.lineLocatePoint(QgsGeometry.fromPoint(self.myPoint)))))).zfill(6) # used in old
                self.progressiva = str(int(round((geom.length()-geom.lineLocatePoint(QgsGeometry.fromPointXY(self.myPoint)))))).zfill(6) # new for Qgis3
            
    def updateTableWidget(self):
        #populate the table with vector layers elements
        self.dock.tableWidget.setRowCount(0)
        self.dock.tableWidget.setColumnWidth(0,30)
        self.dock.tableWidget.setColumnWidth(1,230)
        self.dock.tableWidget.setColumnWidth(2,80)
        self.dock.tableWidget.setColumnWidth(3,100)
        mapCanvas = self.iface.mapCanvas()
        self.dock.textEditLog.append("DEBUG(Fabio): mapCanvas.layerCount(): " + str(mapCanvas.layerCount()))
        for i in range(mapCanvas.layerCount()):
            layer = mapCanvas.layer(i)            
            self.dock.textEditLog.append("DEBUG(Fabio): layer(i) i: " + str(i))
            self.dock.textEditLog.append("DEBUG(Fabio): layer.type(): " + str(layer.type()))
            self.dock.textEditLog.append("DEBUG(Fabio): layer.name(): " + str(layer.name()))
         #   if ( layer.type() == layer.VectorLayer  ) and (layer.geometryType() != QGis.NoGeometry) and ( # used in old
         #           layer.name() != "idrfiu_tt"):# used in old
            if ( layer.type() == layer.VectorLayer  ) and (layer.geometryType() != QgsWkbTypes.NoGeometry) and (layer.name() != "idrfiu_tt"): # new for Qgis3
                currentRowCount = self.dock.tableWidget.rowCount()
                self.dock.tableWidget.insertRow(currentRowCount)
                chkBoxItem = QTableWidgetItem()
                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(Qt.Unchecked) 
                self.dock.tableWidget.setItem(currentRowCount,0, chkBoxItem)
                comboBoxItemL = QComboBox()
                comboBoxItemL.addItem(layer.name(),layer.id())
                self.dock.tableWidget.setCellWidget(currentRowCount,1, comboBoxItemL)
                #self.dock.tableWidget.setItem(currentRowCount,1, QTableWidgetItem(layer.name()))
                comboBoxItemF = QComboBox()              
              #  fields = layer.pendingFields() # used in old
                fields = layer.fields() # new for Qgis3
                for field in fields:
                     comboBoxItemF.addItem(field.name())
                     self.dock.textEditLog.append("DEBUG(Fabio): field.name(): " + str(field.name()))
                index = comboBoxItemF.findText("classid", Qt.MatchFixedString)
                if index >= 0:
                    comboBoxItemF.setCurrentIndex(index)
                self.dock.tableWidget.setCellWidget(currentRowCount,2, comboBoxItemF)

    def selUnselAllLayers(self):
        if self.dock.checkSelectAll.checkState() == Qt.Checked:
            stato=Qt.Checked
        else:
            stato=Qt.Unchecked
        allRows = self.dock.tableWidget.rowCount()
       # for row in xrange(0,allRows): # used in old
        for row in range(0,allRows): # new for Qgis3
                self.dock.tableWidget.item(row,0).setCheckState(stato) 

    def getLayersAndIds(self):
        results=[]
        allRows = self.dock.tableWidget.rowCount()
       # for row in xrange(0,allRows):  # used in old
        for row in range(0,allRows): # new for Qgis3
                if (self.dock.tableWidget.item(row,0).checkState() == Qt.Checked) and (self.dock.tableWidget.item(row,3)):
                    riga=[]
                    riga.append(self.dock.tableWidget.cellWidget(row,1).currentText())
                    riga.append(self.dock.tableWidget.cellWidget(row,2).currentText())
                    riga.append(self.dock.tableWidget.item(row,3).text())
                    results.append(riga)
        return results

    def findFeatures(self):
        allRows = self.dock.tableWidget.rowCount()
     #   for row in xrange(0,allRows): # used in old
        for row in range(0,allRows): # new for Qgis3
                if self.dock.tableWidget.item(row,0).checkState() == Qt.Checked: 
                    twi1 = self.dock.tableWidget.cellWidget(row,1) # layer
                    twi2 = self.dock.tableWidget.cellWidget(row,2) # field
                    layerID = str(twi1.itemData(twi1.currentIndex()))
                  ##  layer = QgsMapLayerRegistry.instance().mapLayer(layerID) # used in old 
                    layer = QgsProject.instance().mapLayer(layerID) # new for Qgis3
                    if layer.featureCount() > 0:
                        spIndex = QgsSpatialIndex(layer.getFeatures())
                      #  intersectsIds = spIndex.intersects(QgsGeometry.fromPoint(self.myPoint).buffer(50,-1).boundingBox()) # used in old 
                        intersectsIds = spIndex.intersects(QgsGeometry.fromPointXY(self.myPoint).buffer(self.distance_max,-1).boundingBox()) # new for Qgis3 self.distance_max
                        if len(intersectsIds) >0:
                            self.dock.textEditLog.append("DEBUG(Fabio): ----££££----- len(intersectsIds): " + str(len(intersectsIds))) 
                            request=QgsFeatureRequest().setFilterFids(intersectsIds)
                            features = layer.getFeatures(request)
                            nearestFtr = QgsFeature()
                            dista=100.0
                            for feature in features:
                              #  myDista=QgsGeometry.distance(QgsGeometry.fromPoint(self.myPoint),feature.geometry())  # used in old
                                myDista=QgsGeometry.distance(QgsGeometry.fromPointXY(self.myPoint),feature.geometry()) # new for Qgis3
                                if myDista<dista:
                                    nearestFtr=feature
                                    dista=myDista
                            features.nextFeature(nearestFtr)
                            attrs = nearestFtr.attributes()
                            self.dock.textEditLog.append("DEBUG(Fabio): --------- twi2.currentText(): " + str(twi2.currentText())) 
                            self.dock.textEditLog.append("DEBUG(Fabio): ----###---- attr Value: " + str(layer.fields().indexFromName(twi2.currentText()))) 
                            self.dock.textEditLog.append("DEBUG(Fabio): ----###---- attr Value: " + str(layer.dataProvider().fieldNameIndex(twi2.currentText())))
                            self.dock.textEditLog.append("DEBUG(Fabio): ----###---- attr: " + str(attrs))
                            
                         #   attrValue=attrs[layer.fieldNameIndex(twi2.currentText())] # used in old
                            attrValue=attrs[layer.dataProvider().fieldNameIndex(twi2.currentText())] # new for Qgis3
                            self.dock.textEditLog.append("DEBUG(Fabio): -----00---- attrValue: " + str(attrValue)) 
                            self.dock.tableWidget.setItem(row,3, QTableWidgetItem(str(attrValue)))
            
        
    def selectPoint(self, checked):
        if checked:
            self.toggleSelectButton(self.dock.buttonSelectPoint)
            self.dock.lineEditX.setValue(0.0)
            self.dock.lineEditY.setValue(0.0)
          #  self.myPoint = QgsPoint(0.0,0.0)  # used in old
            self.myPoint = QgsPointXY(0.0,0.0) # new for Qgis3
            self.iface.mapCanvas().setMapTool(self.sourceIdEmitPoint)
        else:
            self.iface.mapCanvas().unsetMapTool(self.sourceIdEmitPoint)
        
    def setPointXY(self, pt):
        self.dock.lineEditX.setValue(pt.x())
        self.dock.lineEditY.setValue(pt.y())
      #  self.myPoint = QgsPoint(pt.x(),pt.y()) # used in old
        self.myPoint = QgsPointXY(pt.x(),pt.y()) # new for Qgis3
    
    def run(self):
        self.dock.textEditLog.clear()
        self.dock.textEditLog.append("DEBUG(Fabio): Start RUN ")
        self.dock.textEditLog.append("self.dock.comboLayers.currentText(): " + self.dock.comboLayers.currentText())
        if self.dock.comboLayers.currentText()=='':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: Seleziona il layer idrografia!\n')
            return        
        if self.dock.comboFields.currentText()=='':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: Seleziona il campo classid per l\' idrografia!\n')
            return
        if self.dock.lineEditX.value() < 1.0 or self.dock.lineEditY.value() < 1.0:
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: Seleziona un punto sulla mappa!\n')
            return 
#        if self.dock.lineEditTitolo.text() == '':
#            QMessageBox.warning(self.dock, self.dock.windowTitle(),
#                    'ATTENZIONE: il campo Titolo e\' vuoto!\n')
#            return 
#        if self.dock.textEditDescrizione.toPlainText() == '':
#            QMessageBox.warning(self.dock, self.dock.windowTitle(),
#                    'ATTENZIONE: il campo Descrizione e\' vuoto!\n')
#            return 
        if len(self.dock.lineEditData.text()) < 4 or not self.dock.lineEditData.text().isdigit():
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Data e\' vuoto o non corretto!\n')
            return 
        if len(self.filesList) < 1:
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: Nessun file selezionato!\n')
            return 
        if self.dock.lineEditUser.text() == '@provincia.tn.it':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->User non e\' completo!\n')
            return 
        if self.dock.lineEditPass.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->Password e\' vuoto!\n')
            return    
        if self.dock.lineEditEndpoint.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->Server e\' vuoto!\n')
            return         
        if self.dock.lineEditCompanyid.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->CompaniId e\' vuoto!\n')
            return
        if self.dock.lineEditGroupid.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->GroupId e\' vuoto!\n')
            return
        if self.dock.lineEditRepositoryid.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->RepositoriId e\' vuoto!\n')            
            return  
        if self.dock.lineEditParentfolder.text() == '':
            QMessageBox.warning(self.dock, self.dock.windowTitle(),
                    'ATTENZIONE: il campo Config->parentFolder e\' vuoto!\n')            
            return         
        
        ydamConfig=self.getYdamConfig()

        self.dock.textEditLog.append(str(round(self.myPoint.x()))+' '+str(round(self.myPoint.y())))
        self.findFeatures()
        self.getIdrografia()
        self.dock.textEditLog.append("Asta "+str(self.asta))
        self.dock.textEditLog.append("Progressiva "+str(self.progressiva))
    
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        mydata=self.dock.lineEditData.text()
        
#OLD#### NO CLASS CALL foldersXydam=ws.getNomeAsta("C:\\Users\\fabio.roncato\\qgis_plugin\\ydam\\nomeasta.csv",self.asta,mydata) 
        foldersXydam = self.ws_ydamInstance.getNomeAsta("C:\\Users\\fabio.roncato\\qgis_plugin\\ydam\\nomeasta.csv",self.asta,mydata) # NEW WITH CLASS
        self.dock.textEditLog.append("/".join(foldersXydam))
        # creo gerarchia folder se non esistono
        self.dock.textEditLog.append("DEBUG(Fabio): ############################### ") 
        self.dock.textEditLog.append("DEBUG(Fabio): foldersXydam " + str(foldersXydam)) 
        self.dock.textEditLog.append("DEBUG(Fabio): foldersXydam[1:] " + str(foldersXydam[1:])) 
        self.dock.textEditLog.append("DEBUG(Fabio): ydamConfig['parentfolder'] " + str(ydamConfig['parentfolder'])) 
        self.dock.textEditLog.append("DEBUG(Fabio): ydamConfig " + str(ydamConfig)) 
#OLD#### NO CLASS CALL newFid=ws.createYdamFolders(foldersXydam[1:],0,ydamConfig['parentfolder'],ydamConfig) 
        newFid=self.ws_ydamInstance.createYdamFolders(foldersXydam[1:],0,ydamConfig['parentfolder'],ydamConfig) # NEW WITH CLASS
        
        # carico i files
        # creo titolo
        titolo=self.progressiva+"_"+self.asta
        if (self.dock.lineEditTitolo.text()!=''):
            titolo+="_"+self.dock.lineEditTitolo.text()
        # creo descrizione
        if (self.dock.textEditDescrizione.toPlainText()!=''):
            descri=self.dock.textEditDescrizione.toPlainText()+";"
        else:
            descri=''
        pt4326=self.transfToWGS(self.myPoint,self.getMapCRS())
        descri+="coordinate="+str(round(pt4326.x(),4))+" "+str(round(pt4326.y(),4))+";"
        descri+="progressiva="+self.progressiva+";"
        descri+="asta="+self.asta+";"
        righeLayerIds=self.getLayersAndIds()
        for layer,idfield,val in righeLayerIds:
            descri+=layer+"."+idfield+"="+val+";"        
        for fName in self.filesList:
            fileSize=round(os.stat(fName).st_size/(1024.0*1024.0),2)
            if fileSize < 100:        
#OLD#### NO CLASS CALL ws.sendFileToYdam(newFid,fName,titolo,descri,ydamConfig) 
                self.ws_ydamInstance.sendFileToYdam(newFid,fName,titolo,descri,ydamConfig) # NEW WITH CLASS
                self.dock.textEditLog.append(fName+" caricato!")
            else:
                self.dock.textEditLog.append(fName+" non caricato: "+str(fileSize)+"MB > 100MB")
        self.dock.textEditLog.append("")
        QApplication.restoreOverrideCursor()
        
    def call_help(self):
        qgis.utils.showPluginHelp()
        
    def clear(self):
        self.updateComboLayers()
        self.idrSpIndex = None
        self.dock.lineEditX.setValue(0.0)
        self.dock.lineEditY.setValue(0.0)
        #self.dock.textEditLog.clear() # commentato Fabio
        self.dock.lineEditTitolo.clear()
        self.dock.textEditDescrizione.clear()
        self.dock.lineEditData.clear()
        self.updateLineEditData()
        self.dock.textEditTag.clear()
        self.updateTableWidget()
        QApplication.restoreOverrideCursor()

        
    def toggleSelectButton(self, button):
        selectButtons = [
            self.dock.buttonSelectPoint
        ]
        for selectButton in selectButtons:
            if selectButton != button:
                if selectButton.isChecked():
                    selectButton.click()
        

