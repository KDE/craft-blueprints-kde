import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            # Movet to frameworks with KF6, was independent before
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KUserFeedback"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtcharts"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DENABLE_DOCS=OFF"]
