import info
from CraftCore import CraftCore
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in ["1.3.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kuserfeedback/kuserfeedback-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kuserfeedback-{ver}"

        self.targetDigests["1.3.0"] = (["252308b822dd4690ea85ab1688c9b0da5512978ac6b435f77a5979fc1d2ffd13"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.3.0"

        self.description = "KUserFeedback"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["libs/qt6/qtcharts"] = None


from Blueprints.CraftPackageObject import CraftPackageObject


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)
        self.subinfo.options.configure.args += ["-DENABLE_DOCS=OFF"]
