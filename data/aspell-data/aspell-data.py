import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.60.6'] = """ http://files.kolab.org/local/windows-ce/aspell-0.60.6-data.zip"""

        self.defaultTarget = '0.60.6'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
