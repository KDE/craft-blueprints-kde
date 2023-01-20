import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/nodejs"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None
        self.runtimeDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["libs/qt6/qtwebchannel"] = None

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
