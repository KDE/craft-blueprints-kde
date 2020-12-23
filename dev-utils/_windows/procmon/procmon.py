import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = 'https://download.sysinternals.com/files/ProcessMonitor.zip'
        self.defaultTarget = 'latest'
        self.targetInstallPath['latest'] = os.path.join("dev-utils", "bin")


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
