import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtwebsockets"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
