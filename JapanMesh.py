# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
import resources_rc
import os
import sip

class JapanMesh:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        settings = QSettings()
        locale = settings.value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir,'i18n','japanmeshplugin_{0}.qm'.format(locale))

        if (os.path.exists(locale_path)):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if (qVersion() > '4.3.3'):
                QCoreApplication.installTranslator(self.translator)

        self.canvas = self.iface.mapCanvas()
        self.win = self.iface.mainWindow()
        self.plugin_name = u"JapanMesh"
        self.menu_name = self.plugin_name
        self.title = self.plugin_name
        self.base_layer_name = u"mesh1"
        self.base_fileld_name = u"m1code"
        self.base_crs = "EPSG:4612"
        self.submenu1 = self.tr(u"Create 1st Mesh")
        self.submenu2 = self.tr(u"Create 2nd Mesh")
        self.submenu3 = self.tr(u"Create 3rd Mesh")
        self.submenu4 = self.tr(u"Create 4th Mesh")
        self.submenu5 = self.tr(u"Create 5th Mesh")
        self.submenu6 = self.tr(u"Create 6th Mesh")
        self.submenu7 = self.tr(u"Create 7th Mesh")
        self.submenu8 = self.tr(u"Create 8th Mesh")
        self.submenu9 = u"README.TXT"
        self.submenu10 = u"README.html"
        self.lat_min = 20
        self.lat_max = 46
        self.lon_min = 122
        self.lon_max = 154
        self.progressMessageBar = None
        self.progress = None
        self.icon = QIcon(self.plugin_dir + "/icons/icon.png")
        self.readme_file = u"README.txt"
        self.readme_file_html = u"README.html"
        self.mesh_types = 8

        #選択フィーチャー数の制限
        self.limit = 40000

        QObject.connect(self.canvas,SIGNAL("layersChanged()"),self.layersChange)

        self.msg_1 = u"({})file is not found."
        self.msg_2 = u"({})layer is already existing."
        self.msg_3 = u"(self.limit) parameter is invalid."
        self.msg_4 = u"({}) not found."
        self.msg_5 = u"Feature of the layer({}) is not selected."
        self.msg_6 = u"Selected features({0}) is over the limitation({1})."
        self.msg_7 = u"({})field is not found."
        self.msg_8 = u"Error"
        self.msg_9 = u"String is included in the field({})."
        self.msg_10 = u"({0})field is already existing at layer({1})."
        self.msg_11 = u"Creating a mesh layer..."
        self.msg_12 = u"Cancel"
        self.msg_13 = u"Finished"
        self.msg_14 = u"Stopped"
        self.msg_15 = u"Processing stopped."
        self.msg_16 = u"Error({})"
        self.msg_17 = u"({})layer is not a polygon layer."

        #test for i18n
        #for i in range(1,18):
        #    msg = eval("self.msg_"  + str(i))
        #    QMessageBox.information(self.win,self.title,self.tr(msg))

    def tr(self,msg):
        return QCoreApplication.translate(self.plugin_name,msg)

    def initGui(self):
        icon = self.icon
        self.action_m1 = QAction(icon,self.submenu1,self.win)
        self.action_m2 = QAction(icon,self.submenu2,self.win)
        self.action_m3 = QAction(icon,self.submenu3,self.win)
        self.action_m4 = QAction(icon,self.submenu4,self.win)
        self.action_m5 = QAction(icon,self.submenu5,self.win)
        self.action_m6 = QAction(icon,self.submenu6,self.win)
        self.action_m7 = QAction(icon,self.submenu7,self.win)
        self.action_m8 = QAction(icon,self.submenu8,self.win)
        self.action_readme = QAction(icon,self.submenu9,self.win)
        self.action_readme_html = QAction(icon,self.submenu10,self.win)

        self.iface.addToolBarIcon(self.action_m1)
        self.iface.addToolBarIcon(self.action_m2)
        self.iface.addToolBarIcon(self.action_m3)
        self.iface.addToolBarIcon(self.action_m4)
        self.iface.addToolBarIcon(self.action_m5)
        self.iface.addToolBarIcon(self.action_m6)
        self.iface.addToolBarIcon(self.action_m7)
        self.iface.addToolBarIcon(self.action_m8)
        self.iface.addToolBarIcon(self.action_readme)
        self.iface.addToolBarIcon(self.action_readme_html)

        if hasattr(self.iface,"addPluginToVectorMenu" ):
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m1)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m2)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m3)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m4)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m5)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m6)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m7)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_m8)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_readme)
            self.iface.addPluginToVectorMenu(self.menu_name,self.action_readme_html)
        else:
            self.iface.addPluginToMenu(self.menu_name,self.action_m1)
            self.iface.addPluginToMenu(self.menu_name,self.action_m2)
            self.iface.addPluginToMenu(self.menu_name,self.action_m3)
            self.iface.addPluginToMenu(self.menu_name,self.action_m4)
            self.iface.addPluginToMenu(self.menu_name,self.action_m5)
            self.iface.addPluginToMenu(self.menu_name,self.action_m6)
            self.iface.addPluginToMenu(self.menu_name,self.action_m7)
            self.iface.addPluginToMenu(self.menu_name,self.action_m8)
            self.iface.addPluginToMenu(self.menu_name,self.action_readme)
            self.iface.addPluginToMenu(self.menu_name,self.action_readme_html)

        self.action_m2.setDisabled(True)
        self.action_m3.setDisabled(True)
        self.action_m4.setDisabled(True)
        self.action_m5.setDisabled(True)
        self.action_m6.setDisabled(True)
        self.action_m7.setDisabled(True)
        self.action_m8.setDisabled(True)

        QObject.connect(self.action_m1,SIGNAL("triggered()"),self.createBaseMesh)
        QObject.connect(self.action_m2,SIGNAL("triggered()"),lambda level=2:self.createMesh(level))
        QObject.connect(self.action_m3,SIGNAL("triggered()"),lambda level=3:self.createMesh(level))
        QObject.connect(self.action_m4,SIGNAL("triggered()"),lambda level=4:self.createMesh(level))
        QObject.connect(self.action_m5,SIGNAL("triggered()"),lambda level=5:self.createMesh(level))
        QObject.connect(self.action_m6,SIGNAL("triggered()"),lambda level=6:self.createMesh(level))
        QObject.connect(self.action_m7,SIGNAL("triggered()"),lambda level=7:self.createMesh(level))
        QObject.connect(self.action_m8,SIGNAL("triggered()"),lambda level=8:self.createMesh(level))
        QObject.connect(self.action_readme,SIGNAL("triggered()"),self.showReadme)
        QObject.connect(self.action_readme_html,SIGNAL("triggered()"),self.showReadmeHtml)

    def unload(self):
        self.iface.removeToolBarIcon(self.action_m1)
        self.iface.removeToolBarIcon(self.action_m2)
        self.iface.removeToolBarIcon(self.action_m3)
        self.iface.removeToolBarIcon(self.action_m4)
        self.iface.removeToolBarIcon(self.action_m5)
        self.iface.removeToolBarIcon(self.action_m6)
        self.iface.removeToolBarIcon(self.action_m7)
        self.iface.removeToolBarIcon(self.action_m8)
        self.iface.removeToolBarIcon(self.action_readme)
        self.iface.removeToolBarIcon(self.action_readme_html)

        if hasattr(self.iface,"addPluginToVectorMenu" ):
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m1)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m2)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m3)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m4)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m5)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m6)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m7)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_m8)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_readme)
            self.iface.removePluginVectorMenu(self.menu_name,self.action_readme_html)
        else:
            self.iface.removePluginMenu(self.menu_name,self.action_m1)
            self.iface.removePluginMenu(self.menu_name,self.action_m2)
            self.iface.removePluginMenu(self.menu_name,self.action_m3)
            self.iface.removePluginMenu(self.menu_name,self.action_m4)
            self.iface.removePluginMenu(self.menu_name,self.action_m5)
            self.iface.removePluginMenu(self.menu_name,self.action_m6)
            self.iface.removePluginMenu(self.menu_name,self.action_m7)
            self.iface.removePluginMenu(self.menu_name,self.action_m8)
            self.iface.removePluginMenu(self.menu_name,self.action_readme)
            self.iface.removePluginMenu(self.menu_name,self.action_readme_html)

        QObject.disconnect(self.canvas,SIGNAL("layersChanged()"),self.layersChange)

    def showReadme(self):
        readme_file = os.path.join(self.plugin_dir,"docs" ,self.readme_file)
        if (os.path.exists(readme_file)):
            os.startfile(readme_file)
        else:
            QMessageBox.information(self.win,self.title,self.tr(self.msg_1).format(self.readme_file))

    def showReadmeHtml(self):
        readme_file = os.path.join(self.plugin_dir,"docs" ,self.readme_file_html)
        if (os.path.exists(readme_file)):
            os.startfile(readme_file)
        else:
            QMessageBox.information(self.win,self.title,self.tr(self.msg_1).format(self.readme_file_html))

    def layersChange(self):
        for i in range(2,self.mesh_types + 1):
            action = getattr(self,"action_m" + str(i))
            if (action != None):
                if (isinstance(action,QAction) == True):
                    action.setDisabled(True)

        for id,layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if (layer.isValid()):
                if (layer.type() == QgsMapLayer.VectorLayer):
                    layer_name = layer.name()
                    if (len(layer_name) == len(self.base_layer_name)):
                        mesh = layer_name[:4]
                        level = layer_name[-1:]
                        if  (mesh == "mesh") and (level.isdigit()):
                            if  (0 < int(level) < self.mesh_types):
                                if (layer.fieldNameIndex("m" + level + "code") >= 0):
                                    action = getattr(self,"action_m" + str(int(level) + 1))
                                    if (action != None) and (isinstance(action,QAction) == True):
                                        action.setDisabled(False)
                                    if (layer_name == "mesh5"):
                                        self.action_m7.setDisabled(False)

    def createBaseMesh(self):
        height = float(40.0 / 60.0)
        gosa = 0.0001
        lat_min = self.lat_min
        lat_max = self.lat_max
        lon_min = self.lon_min
        lon_max = self.lon_max
        lat = lat_min
        crs = self.base_crs

        layer_name = self.base_layer_name
        if (self.getVectorLayer(layer_name) != None):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_2).format(layer_name))
            return

        layer = QgsVectorLayer("Polygon?crs=" + crs,layer_name,"memory")
        provider = layer.dataProvider()
        layer.startEditing()
        provider.addAttributes([QgsField(self.base_fileld_name,QVariant.String)])

        while lat < (lat_max - height) :
            for lon in range(lon_min,lon_max):
                l_b = QgsPoint(lon,lat)
                l_t = QgsPoint(lon,lat + height)
                r_t = QgsPoint(lon + 1,lat + height)
                r_b = QgsPoint(lon + 1,lat )

                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolygon([[l_b,l_t,r_t,r_b,l_b]]))
                code = int(((lat + gosa) * 1.5 * 100) + ((lon + gosa) - 100))
                feature.setAttributes([str(code)])
                provider.addFeatures([feature])
            lat = lat + height

        layer.commitChanges()
        layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def checkInputLayer(self,level):
        if  (1 < level <= self.mesh_types):
            if (level == 7):
                return "mesh5"
            else:
                return "mesh"  + str(level - 1)
        return None

    def checkInputField(self,level):
        if (1 < level <= self.mesh_types):
            if (level == 7):
                return "m5code"
            else:
                return "m"  + str(level - 1) + "code"
        return None

    def getCodeFigures(self,level):
        if (level == 2):
            return 100#10km
        elif (level == 3):
            return 100#1km
        elif (level == 4):
            return 10#500m
        elif (level == 5):
            return 10#250m
        elif (level == 6):
            return 10#125m
        elif (level == 7):
            return 100#50m
        elif (level == 8):
            return 100#10m
        else:
            return None

    def getMaxRange(self,level):
        if (level == 2):
            return 8#10km
        elif (level == 3):
            return 10#1km
        elif (level == 4):
            return 2#500m
        elif (level == 5):
            return 2#250m
        elif (level == 6):
            return 2#125m
        elif (level == 7):
            return 5#50m
        elif (level == 8):
            return 5#10m
        else:
            return None

    def getVectorLayer(self,find_layer_name):
        for id, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
                layer_name = layer.name()
                if (find_layer_name == layer_name):
                        return layer
        return None

    def checkFieldValue(self,layer,field_index):
        check = True
        feature = QgsFeature()
        features = layer.selectedFeatures()
        for feature in features:
            if (str(feature.attributes()[field_index]).isdigit() == False):
                check = False
                break
        return check

    def checkFieldName(self,layer,new_field_name):
        check = True
        fields = layer.dataProvider().fields()
        for field in fields:
            if (field.name() == new_field_name):
                check = False
                break
        return check

    def checkGeometry(self,layer):
        check = True
        if (layer.geometryType() != QGis.Polygon):
                check = False
        return check

    def createMesh(self,level):
        crs = self.base_crs
        input_layer_name = self.checkInputLayer(level)
        input_layer = self.getVectorLayer(input_layer_name)
        max_range = int(self.getMaxRange(level))
        limit = self.limit

        if (type(limit) != int):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_3))
            return

        if (input_layer == None):
            QMessageBox.information(self.win,self.title,
                                    self.tr(self.msg_4).format(input_layer_name))
            return

        features_count = len(input_layer.selectedFeaturesIds())

        if (features_count == 0):
            QMessageBox.information(self.win,self.title,
                                    self.tr(self.msg_5).format(input_layer_name))
            return

        if (features_count > self.limit):
            QMessageBox.information(self.win,self.title,
                                    self.tr(self.msg_6).format(str(features_count),str(limit)))
            return

        field_name = self.checkInputField(level)
        field_index = input_layer.fieldNameIndex(field_name)

        if (not field_index >= 0) or (field_name == None):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_7).format(field_name))
            return

        layer_name = "mesh" + str(level)
        if (self.getVectorLayer(layer_name) != None):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_2).format(layer_name))
            return

        figures = self.getCodeFigures(level)
        if (figures == None) or (max_range == None):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_8))
            return

        check_field_value = self.checkFieldValue(input_layer,field_index)
        if (check_field_value == False) :
            QMessageBox.information(self.win,self.title,self.tr(self.msg_9).format(field_name))
            return

        new_field_name = "m" + str(level) + "code"
        check_field_value = self.checkFieldName(input_layer,new_field_name)
        if (check_field_value == False) :
            QMessageBox.information(self.win,self.title,
                                    self.tr(self.msg_10).format(new_field_name,input_layer_name))
            return

        check_geom = self.checkGeometry(input_layer)
        if (check_geom == False):
            QMessageBox.information(self.win,self.title,self.tr(self.msg_17).format(layer_name))
            return

        mesh_thread = MeshThread(input_layer,crs,layer_name,
                                 new_field_name,field_index,figures,max_range)

        messageBar = self.iface.messageBar().createMessage(self.tr(self.msg_11))
        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        cancelButton = QPushButton()
        cancelButton.setText(self.tr(self.msg_12))
        cancelButton.clicked.connect(mesh_thread.kill)
        messageBar.layout().addWidget(self.progressBar)
        messageBar.layout().addWidget(cancelButton)
        self.iface.messageBar().pushWidget(messageBar, self.iface.messageBar().INFO)
        self.messageBar = messageBar

        thread = QThread()
        mesh_thread.moveToThread(thread)
        mesh_thread.finished.connect(self.threadFinished)
        mesh_thread.error.connect(self.threadError)
        mesh_thread.progress.connect(self.threadProgressbar)
        thread.started.connect(mesh_thread.run)
        thread.start()
        self.thread = thread
        self.mesh_thread = mesh_thread

    def threadProgressbar(self,step):
        if (type(step) == int) or (type(step) == float):
            if (self.progressBar is not None):
                if (sip.isdeleted(self.progressBar) == False):
                    self.progressBar.setValue(int(step * 100))

    def threadFinished(self, ret):
        self.threadDisconnect()
        self.threadCleanup()
        messageBar = self.iface.messageBar()
        messageBar.popWidget(self.messageBar)
        if (ret is not None):
            layer,is_sccess = ret
            if (is_sccess == 1) and (layer != None) and (layer.isValid()):
                layer.commitChanges()
                layer.updateExtents()
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                messageBar.pushMessage(self.tr(self.msg_13),duration=3)
            else:
                messageBar.pushMessage(self.tr(self.msg_14),
                                       level=QgsMessageBar.CRITICAL,duration=3)
                self.clearMemoryProvider(layer)
        else:
            messageBar.pushMessage(self.tr(self.msg_14),
                                   level=QgsMessageBar.CRITICAL,duration=3)

    def threadCleanup(self):
        if (self.mesh_thread is not None):
            if (sip.isdeleted(self.mesh_thread) == False):
                if (isinstance(self.mesh_thread,MeshThread)):
                    self.mesh_thread.deleteLater()
                    self.mesh_thread = None

        if (self.thread is not None):
            if (sip.isdeleted(self.thread) == False):
                if (isinstance(self.thread,QThread)):
                    self.thread.quit()
                    self.thread.wait()
                    self.thread.deleteLater()
                    self.thread = None

    def threadDisconnect(self):
        if (self.mesh_thread is not None):
            if (sip.isdeleted(self.mesh_thread) == False):
                if (isinstance(self.mesh_thread,MeshThread)):
                    self.mesh_thread.finished.disconnect(self.threadFinished)
                    self.mesh_thread.error.disconnect(self.threadError)
                    self.mesh_thread.progress.disconnect(self.threadProgressbar)

    def threadError(self, error,layer):
        self.threadDisconnect()
        self.threadCleanup()

        messageBar = self.iface.messageBar()
        messageBar.popWidget(self.messageBar)
        messageBar.pushMessage(self.tr(self.msg_15) + error,level=QgsMessageBar.CRITICAL)
        QgsMessageLog.logMessage(self.plugin_name + ":" +self.tr(self.msg_16).format(error),
                                 level=QgsMessageLog.CRITICAL)
        self.clearMemoryProvider(layer)

    def clearMemoryProvider(self,layer):
        try:
            if (layer != None):
                if (isinstance(layer,QgsVectorLayer) == True):
                    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
                    layer.startEditing()
                    provider = layer.dataProvider()
                    if (isinstance(provider,QgsVectorDataProvider) == True):
                        feature = QgsFeature()
                        features = provider.getFeatures()
                        while features.nextFeature(feature):
                            if (isinstance(feature,QgsFeature)):
                                layer.deleteFeature(feature.id())
                        provider.deleteAttributes(provider.attributeIndexes())
                        layer.commitChanges()
        except:
            pass

class MeshThread(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(basestring,object)
    progress = pyqtSignal(float)

    def __init__(self,input_layer,crs,layer_name,new_field_name,field_index,figures,max_range):
        QObject.__init__(self)
        self.input_layer = input_layer
        self.layer = None
        self.crs = crs
        self.layer_name = layer_name
        self.new_field_name = new_field_name
        self.field_index = field_index
        self.figures = figures
        self.max_range = max_range
        self.killed = False

    def kill(self):
        self.killed = True

    def run(self):
        try:
            self._run()
        except Exception, e:
            self.error.emit(e.message,self.layer)

    def _run(self):
        ret = None
        is_sccess = 0

        input_layer = self.input_layer
        crs = self.crs
        layer_name = self.layer_name
        new_field_name = self.new_field_name
        field_index = self.field_index
        figures = self.figures
        max_range = self.max_range

        layer = QgsVectorLayer("Polygon?crs=" + crs,layer_name,"memory")
        self.layer = layer
        layer.startEditing()
        provider = layer.dataProvider()

        fields = []
        input_fields = input_layer.dataProvider().fields()
        for field in input_fields:
            if (field.type() == QVariant.Int):
                fields.append(QgsField(QgsField(field.name(),QVariant.Int)))
            elif (field.type() == QVariant.Double):
                fields.append(QgsField(QgsField(field.name(),QVariant.Double)))
            elif (field.type() == QVariant.String):
                fields.append(QgsField(QgsField(field.name(),QVariant.String)))
            else:
                fields.append(QgsField(QgsField(field.name(),QVariant.String)))

        fields.append(QgsField(new_field_name,QVariant.String))
        provider.addAttributes(fields)

        feat = QgsFeature()
        geom = QgsGeometry()
        input_map = []
        attributes = []
        count = 0
        input_features = input_layer.selectedFeatures()
        total = len(input_features)

        for feat in input_features:
            if (self.killed is True):
                break

            count += 1
            self.progress.emit(count / float(total))

            geom = QgsGeometry(feat.geometry())
            if (geom.type() == QGis.Polygon):
                input_code = int(feat.attributes()[field_index])
                base_code = int(input_code * figures)

                input_map[:] = []
                for i in range(len(input_fields)):
                    input_map.append(feat.attributes()[i])

                poly = geom.asPolygon()
                min_pt = poly[0][0]
                max_pt = poly[0][2]

                min_x,min_y = min_pt
                max_x,max_y = max_pt

                base_width = float(max_x - min_x)
                base_height = float(max_y - min_y)

                width = base_width / float(max_range)
                height = base_height / float(max_range)

                lon = min_x
                lat = min_y

                ii = 1
                for i in range(0,max_range):
                    for j in range(0,max_range):
                        if (self.killed is True):
                            break

                        l_b = QgsPoint(lon,lat)
                        l_t = QgsPoint(lon,lat + height)
                        r_t = QgsPoint(lon + width,lat + height)
                        r_b = QgsPoint(lon + width,lat )

                        if (figures == 10):
                            code = base_code +  ii
                            ii = ii + 1
                        else:
                            code = base_code +  (i * 10) + j

                        attributes[:] = []
                        attributes.extend(input_map)
                        attributes.append(str(code))

                        feature = QgsFeature()
                        feature.setGeometry(QgsGeometry.fromPolygon([[l_b,l_t,r_t,r_b,l_b]]))
                        feature.setAttributes(attributes)
                        provider.addFeatures([feature])
                        lon = lon + width

                    lat = lat + height
                    lon = min_x

        if (self.killed is False):
            self.progress.emit(100)
            is_sccess = 1
            ret = (layer,is_sccess)
        else:
            ret = (layer,is_sccess)

        self.finished.emit(ret)


