import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.1-1"]:
            self.targets[ver] = f"https://github.com/oneclick/rubyinstaller2/releases/download/rubyinstaller-{ver}/rubyinstaller-{ver}-{CraftCore.compiler.architecture}.7z"
            self.targetInstSrc[ver] = f"rubyinstaller-{ver}-{CraftCore.compiler.architecture}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigestsX64["2.5.1-1"] = (['d1666d4b08574947af702f7714e1fb66b8139ed20eb957859fcb929f4f015864'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.5.1-1"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
