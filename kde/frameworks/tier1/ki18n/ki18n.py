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
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/gettext"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
            self.buildDependencies["libs/libintl-lite"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["data/iso-codes"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
