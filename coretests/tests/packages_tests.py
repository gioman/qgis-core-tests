'''
Tests to ensure that a QGIS installation contains Processing dependencies
and they are correctly configured by default
'''
import unittest
import time
import tempfile
from processing.algs.saga.SagaUtils import *
from processing.core.ProcessingConfig import ProcessingConfig
from processing.algs.grass.GrassUtils import GrassUtils
from processing.algs.otb.OTBUtils import *
from qgis.utils import active_plugins
from qgis.core import *
import os


class PackageTests(unittest.TestCase):

    def testSaga(self):
        '''Test SAGA is installed. QGIS-89 (1)'''
        folder = ProcessingConfig.getSetting(SAGA_FOLDER)
        hasSetting = True
        try:
            ProcessingConfig.removeSetting(SAGA_FOLDER)
        except:
            hasSetting = False
        self.assertTrue(getSagaInstalledVersion(True) in ["2.1.2", "2.1.3", "2.1.4", "2.2.0"])
        if hasSetting:
            ProcessingConfig.setSettingValue(SAGA_FOLDER, folder)

    def testGrass(self):
        '''Test GRASS is installed QGIS-89 (2)'''
        folder = ProcessingConfig.getSetting(GrassUtils.GRASS_FOLDER)
        ProcessingConfig.removeSetting(GrassUtils.GRASS_FOLDER)
        msg = GrassUtils.checkGrassIsInstalled()
        self.assertIsNone(msg)
        ProcessingConfig.setSettingValue(GrassUtils.GRASS_FOLDER, folder)

    def testOtb(self):
        '''Test OTB is installed QGIS-89 (3)'''
        folder = findOtbPath()
        self.assertIsNotNone(folder)

    def testCorePluginsAreLoaded(self):
        '''Test core plugins are loaded. QGIS-55'''
        corePlugins = ['processing', 'GdalTools', 'MetaSearch', 'db_manager']
        for p in corePlugins:
            self.assertTrue(p in active_plugins)

    def testGDB(self):
        '''Test GDB format. QGIS-62'''
        layernames = ['T_1_DirtyAreas', 'T_1_PointErrors', 'landbnds', 'counties', 'neighcountry',
                      'cities', 'usabln', 'T_1_LineErrors', 'states', 'T_1_PolyErrors', 'us_lakes',
                      'us_rivers', 'intrstat']
        for layername in layernames:
            layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data",
                                    "ESRI_FileGDB-API_sample_Topo.gdb|layername=%s" % layername),
                                    "test", "ogr")
            self.assertTrue(layer.isValid())
            #QgsMapLayerRegistry.instance().addMapLayer(layer)

    def testGeoPackage(self):
        '''Test GeoPackage'''
        layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data","airports.gpkg"),
                                    "test", "ogr")
        self.assertTrue(layer.isValid())
        filepath = os.path.join(tempfile.mkdtemp(), str(time.time()) + ".gpkg")
        QgsVectorFileWriter.writeAsVectorFormat(layer, filepath, 'utf-8', layer.crs(), 'GPKG')
        layer = QgsVectorLayer(filepath, "test", "ogr")
        self.assertTrue(layer.isValid())



if __name__ == '__main__':
    unittest.main()
