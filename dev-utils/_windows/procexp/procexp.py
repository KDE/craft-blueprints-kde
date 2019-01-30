import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["16.22"]:
            self.targets[ver] = 'http://download.sysinternals.com/files/ProcessExplorer.zip'
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests['16.22'] = (['d393f062091c4fcf720ce0cad56520a920ffcc9412cdc7941150e3bb3fc4fefa'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "16.22"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
