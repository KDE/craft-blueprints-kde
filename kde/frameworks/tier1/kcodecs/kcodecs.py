import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Plugins allowing Qt applications to access further types of images"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.buildDependencies["dev-utils/gperf"] = None


from Blueprints.CraftPackageObject import CraftPackageObject

class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)
