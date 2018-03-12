import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.0.1'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/gperf-3.0.1-bin.zip"
        self.targetInstallPath["3.0.1"] = "dev-utils"
        self.targetDigests['3.0.1'] = 'ff74599cbdf8e970b7f3246da8b4b73909867c66'
        self.defaultTarget = '3.0.1'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
