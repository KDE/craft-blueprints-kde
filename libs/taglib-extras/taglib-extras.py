import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.description = "more plugins for the taglib library"

    def setTargets(self):
        self.svnTargets["svnHEAD"] = "trunk/kdesupport/taglib-extras"
        self.targets["1.0.1"] = "https://download.kde.org/stable/taglib-extras/1.0.1/src/taglib-extras-1.0.1.tar.gz"
        self.targetInstSrc["1.0.1"] = "taglib-extras-1.0.1"
        self.patchToApply["1.0.1"] = [("taglib-extras-1.0.1-20130310.diff", 1)]
        self.defaultTarget = "1.0.1"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ""


# self.subinfo.options.configure.args += ["-DWITH_KDE=ON"]
