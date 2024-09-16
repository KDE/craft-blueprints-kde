import os

import info
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.76"]:
            # always point to the latest, if the checksum mismatches there was probably a new release
            self.targets[ver] = "https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip"
            self.archiveNames[ver] = f"putty-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetDigests["0.76"] = (["48f28aa050a1b5ebe37c88d7fcf97401f931321775a3a95d983aee7097d2766d"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.76"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
