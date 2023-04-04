import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
