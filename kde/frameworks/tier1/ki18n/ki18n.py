import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in ["master"] + self.versionInfo.tarballs():
            self.patchToApply[ver] = [("0002-Keep-LibIntl-libraries-path.patch", 1)]

        self.description = "Ki18n"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/gettext"] = None
        self.buildDependencies["libs/qt5/qtdeclarative"] = None # only needed for unit tests
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        if CraftVersion(self.buildTarget) < CraftVersion("5.50.0"):
            self.runtimeDependencies["libs/qt5/qtscript"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/gettext"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
