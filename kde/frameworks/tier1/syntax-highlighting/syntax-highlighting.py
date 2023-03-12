import info


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


from Blueprints.CraftPackageObject import CraftPackageObject

class Package(CraftPackageObject.get('kde').pattern):
    def __init__(self):
        CraftPackageObject.get('kde').pattern.__init__(self)
