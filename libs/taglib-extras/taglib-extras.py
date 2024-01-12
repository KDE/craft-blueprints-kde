import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.description = "more plugins for the taglib library"

    def setTargets(self):
        self.svnTargets["svnHEAD"] = "trunk/kdesupport/taglib-extras"

        for ver in ["1.0.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/taglib-extras/{ver}/src/taglib-extras-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"taglib-extras-{ver}"

        self.patchToApply["1.0.1"] = [("taglib-extras-1.0.1-20130310.diff", 1)]
        self.defaultTarget = "1.0.1"


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args = ""


# self.subinfo.options.configure.args += ["-DWITH_KDE=ON"]
