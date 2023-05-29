import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.76"]:
            # always point to the latest, if the checksum mismatches there was probably a new release
            self.targets[ver] = f"https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip"
            self.archiveNames[ver] = f"putty-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetDigests["0.76"] = (["48f28aa050a1b5ebe37c88d7fcf97401f931321775a3a95d983aee7097d2766d"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.76"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
