import shutil

import info
from Package.BinaryPackageBase import *

from CraftCore import CraftCore

class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        cache = CraftCore.cache.cacheJsonFromUrl("http://downloads.kdab.com/ci/gammaray/binaries/manifest.json")
        build = cache["APPVEYOR_BUILD_VERSION"]

        self.targets[build] = []
        self.targetDigests[build] = ([], CraftHash.HashAlgorithm.SHA256)
        for abi in ["windows-msvc2015_32-cl", "windows-mingw_32-gcc"]:
            if abi == "-".join(CraftCore.compiler.signature):
                continue
            self.targets[build].append(f"http://downloads.kdab.com/ci/gammaray/binaries/gammaray-{build}-{abi}.7z")
            self.targetDigests[build][0].append(cache["qt-apps/gammaray"][f"gammaray-{build}-{abi}.7z"]["checksum"])

        self.description = "Multiple probes for GammaRay"

        self.defaultTarget = build

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
