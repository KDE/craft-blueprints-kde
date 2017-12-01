import shutil

import info
from Package.BinaryPackageBase import *

from CraftCore import CraftCore
from Utils.CraftManifest import *

class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        manifest = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl("http://downloads.kdab.com/ci/gammaray/binaries/manifest.json"))

        self.targets["master"] = []
        self.targetDigests["master"] = ([], CraftHash.HashAlgorithm.SHA256)
        for abi in manifest.packages.keys():
            if not "qt-apps/gammaray" in manifest.packages[abi]:
                continue
            latest = manifest.packages[abi]["qt-apps/gammaray"].latest
            if latest.fileName.endswith(".exe"):
                continue
            self.targets["master"].append(f"http://downloads.kdab.com/ci/gammaray/binaries/{latest.fileName}")
            self.targetDigests["master"][0].append(latest.checksum)

        self.description = "Multiple probes for GammaRay"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
