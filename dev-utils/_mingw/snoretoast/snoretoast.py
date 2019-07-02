import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.5.2", "0.6.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/bin/snoretoast_v{ver}-{CraftCore.compiler.architecture}.7z"
            if ver != "0.6.0":
                self.targetInstSrc[ver] = f"snoretoast_v{ver}-{CraftCore.compiler.architecture}"
        self.targetDigests["0.5.2"] = (["94209bbf777265bfbd5b77fde4e0ff5801509db043e0575ee00ba5736d2e946f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64["0.6.0"] = (["170443d2d87318fcaa8d8a051f29c6c65aaca4f79f1d462aa0b4aa5493f4981e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.6.0"] = (["824eb0272cb7ef05856809c9faea0615a480c7c1cac51d9b22e5f90751a91888"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"
        self.defaultTarget = "0.6.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
