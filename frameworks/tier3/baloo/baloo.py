import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Baloo is a file indexing and searching framework."

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["frameworks/tier1/solid"] = None
        self.runtimeDependencies["frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["frameworks/tier3/kio"] = None
        self.runtimeDependencies["libs/lmdb"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
