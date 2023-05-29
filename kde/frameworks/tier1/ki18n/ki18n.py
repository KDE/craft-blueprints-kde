import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in ["master"] + self.versionInfo.tarballs():
            self.patchToApply[ver] = [("0002-Keep-LibIntl-libraries-path.patch", 1)]

        self.description = "Ki18n"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["data/iso-codes"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/gettext"] = None
        else:
            self.buildDependencies["libs/libintl-lite"] = None
        # Qt
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt/qtandroidextras"] = None


from Blueprints.CraftPackageObject import CraftPackageObject


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)

