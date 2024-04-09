import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["56"]:
            self.targets[ver] = f"https://github.com/benhoyt/inih/archive/r{ver}.tar.gz"
            self.targetInstSrc[ver] = f"inih-r{ver}"
        self.targetDigests["56"] = (["4f2ba6bd122d30281a8c7a4d5723b7af90b56aa828c0e88256d7fceda03a491a"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Simple .INI file parser in C, good for embedded systems "
        self.defaultTarget = "56"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
