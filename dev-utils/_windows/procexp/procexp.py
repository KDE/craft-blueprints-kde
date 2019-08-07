import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["16.26"]:
            self.targets[ver] = 'http://download.sysinternals.com/files/ProcessExplorer.zip'
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests['16.26'] = (['dc422a6ca2872207e8d0ef55ba4291998c8923efe847ba9e025c610090ad20be'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "16.26"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
