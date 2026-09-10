import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Solid"
        if CraftCore.compiler.isMacOS:
            # patch will be upstreamed in 6.31.0, fixes BUG 521270
            for ver in ["6.29.0", "6.30.0"]:
                self.patchToApply[ver] = [("mac_cfrelease.patch", 1)]
            self.patchLevel["6.29.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
