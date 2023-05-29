import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["svnHEAD"] = "https://anongit.kde.org/choqok"
        self.svnTargets["0.6.0"] = "tags/choqok/0.6.0/choqok"
        self.defaultTarget = "svnHEAD"

    def setDependencies(self):
        self.runtimeDependencies["kdesupport/qjson"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
