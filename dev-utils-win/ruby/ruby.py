import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.1-2"]:
            self.targets[ver] = f"https://github.com/oneclick/rubyinstaller2/releases/download/{ver}/rubyinstaller-{ver}-{CraftCore.compiler.architecture}.7z"
            self.targetInstSrc[ver] = f"rubyinstaller-{ver}-{CraftCore.compiler.architecture}"
            self.targetInstallPath[ver] = "dev-utils-wins"
        self.targetDigestsX64["2.4.1-2"] = (['2ad3c7f68404ba0805cf91e682ecf2d85b75c42a5809e73e54898f24a1e014bb'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.4.1-2"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
