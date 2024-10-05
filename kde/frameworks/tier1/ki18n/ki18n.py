import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

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


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
