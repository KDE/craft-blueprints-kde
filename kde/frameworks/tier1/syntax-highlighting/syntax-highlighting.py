import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Syntax highlighting engine for Kate syntax definitions."
        self.displayName = "KSyntaxHighlighting"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
