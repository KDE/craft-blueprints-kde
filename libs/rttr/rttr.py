import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/rttrorg/rttr.git"

        for ver in ["0.9.6"]:
            self.targets[ver] = f"https://github.com/rttrorg/rttr/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"rttr-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rttr-{ver}"
        self.targetDigests["0.9.6"] = (["058554f8644450185fd881a6598f9dee7ef85785cbc2bb5a5526a43225aa313f"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.9.6"] = [("FixGcc8Build.patch", 1), ("rttr-0.9.6-20190506.diff", 1)]

        self.description = "Run Time Type Reflection library written in C++"
        self.webpage = "https://www.rttr.org/"
        self.defaultTarget = "0.9.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
