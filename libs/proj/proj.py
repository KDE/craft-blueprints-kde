import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.8.0"]:
            self.targets[ver] = f"http://download.osgeo.org/proj/proj-{ver}.zip"
            self.targetInstSrc[ver] = f"proj-{ver}"
        self.patchToApply["4.8.0"] = [("proj-4.8.0-20120424.diff", 1)]
        self.targetDigests["4.8.0"] = "15f51318b0314f107919b83bdab7b03f31193b75"
        self.description = "Projection library"
        self.defaultTarget = "4.8.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
