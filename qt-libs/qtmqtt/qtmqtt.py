import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['5.12.9','5.13.2','5.14.0','5.14.1','5.14.2','5.15.0','5.15.1', '5.15.2']:
            self.svnTargets[ver] = f"https://github.com/qt/qtmqtt|{ver}"

        #self.defaultTarget = CraftPackageObject.get("libs/qt5/qtdoc").version
        # latest 5.15
        self.defaultTarget = '5.15.2'
        self.description = "QtMQTT"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None

from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
