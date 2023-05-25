import info
from Utils import CraftHash
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.targets['1.2.0'] = 'https://download.kde.org/stable/kuserfeedback/kuserfeedback-1.2.0.tar.xz'
        self.targetDigests['1.2.0'] = (
            ['76aac922b153249b274680a6f4c72c238ef14e3df04bad00cb64158b1063f264'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['1.2.0'] = 'kuserfeedback-1.2.0'

        if CraftCore.compiler.isWindows:
            self.defaultTarget = 'master'
        else:
            self.defaultTarget = '1.2.0'

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
