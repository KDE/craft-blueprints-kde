import info
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["4.90"] = "http://download.sysinternals.com/files/DebugView.zip"
        self.targetInstallPath["4.90"] = "dev-utils/bin"
        self.targetDigests["4.90"] = (["9ccac2978ef0ad16611dfeb15f0fb5f3c554882e1b193c8eebd16ce58a2fed4b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.90"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
