import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtmultimedia"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if CraftCore.compiler.isMSVC2026() and CraftVersion(self.buildTarget) < CraftVersion("6.12.0"):
            self.subinfo.options.configure.args += [
                '-DCMAKE_CXX_FLAGS="/D_SILENCE_EXPERIMENTAL_COROUTINE_DEPRECATION_WARNINGS"',
            ]
