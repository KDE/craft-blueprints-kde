import info


# deprecated class
class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/libkgeomap"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
