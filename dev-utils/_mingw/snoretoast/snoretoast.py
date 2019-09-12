import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.5.2", "0.6.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/bin/snoretoast_v{ver}-{CraftCore.compiler.architecture}.7z"
            if ver != "0.6.0":# hopefully I correctly package in the next release
                self.targetInstSrc[ver] = f"snoretoast_v{ver}-{CraftCore.compiler.architecture}"
            else:
                self.targetInstallPath[ver] = "bin"

        for ver in ["0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/bin/snoretoast-{ver}-msvc2017_{CraftCore.compiler.bits}-cl.7z"

        self.targetDigests["0.5.2"] = (["94209bbf777265bfbd5b77fde4e0ff5801509db043e0575ee00ba5736d2e946f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64["0.6.0"] = (["170443d2d87318fcaa8d8a051f29c6c65aaca4f79f1d462aa0b4aa5493f4981e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.6.0"] = (["824eb0272cb7ef05856809c9faea0615a480c7c1cac51d9b22e5f90751a91888"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64["0.7.0"] = (["dda52f207e8a9d2c61d7d8b57352cae41804b2fa5b64ca587aff8468ad6aab38"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.7.0"] = (["7097eb62d37a086618fe2aff797bf8337b3503d88950de56ac86526c02b7a590"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"
        
        self.patchLevel["0.6.0"] = 1
        self.defaultTarget = "0.7.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: Path(x).suffix in BuildSystemBase.PatchableFile,
                                             blacklist=lambda x, root: True)
        return self.patchInstallPrefix(files, oldPaths=["C:/Craft/BinaryCache/windows-msvc2017_64-cl", "C:/Craft/BinaryCache/windows-msvc2017_32-cl"])