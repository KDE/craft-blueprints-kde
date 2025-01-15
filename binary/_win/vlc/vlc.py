import os

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        for ver in ["3.0.0", "3.0.4", "3.0.8", "3.0.11", "3.0.12"]:
            self.targets[ver] = f"https://download.videolan.org/pub/videolan/vlc/{ver}/win{CraftCore.compiler.bits}/vlc-{ver}-win{CraftCore.compiler.bits}.7z"
            self.targetInstSrc[ver] = f"vlc-{ver}"
            self.targetDigestUrls[
                ver
            ] = f"https://download.videolan.org/pub/videolan/vlc/{ver}/win{CraftCore.compiler.bits}/vlc-{ver}-win{CraftCore.compiler.bits}.7z.sha256"
            self.patchToApply[ver] = [("vlc-2.1.5.diff", 1)]
        self.patchToApply["3.0.11"] += [("vlc-3.0.11-20201106.diff", 1)]
        self.patchToApply["3.0.12"] += [("vlc-3.0.11-20201106.diff", 1)]
        self.patchLevel["3.0.11"] = 1
        self.patchLevel["3.0.12"] = 1
        self.webpage = "https://www.videolan.org/"
        self.description = "an open-source multimedia framework"

        self.defaultTarget = "3.0.12"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        utils.copyDir(self.sourceDir(), self.installDir() / "bin")
        if CraftCore.compiler.isMinGW():
            utils.deleteFile(self.installDir() / "bin/libgcc_s_seh-1.dll")
        utils.mergeTree(self.installDir() / "bin/sdk/include", self.installDir() / "include")
        utils.mergeTree(self.installDir() / "bin/sdk/lib", self.installDir() / "lib")
        utils.rmtree(self.installDir() / "bin/sdk")
        os.makedirs(self.installDir() / "share/applications")
        utils.copyFile(self.blueprintDir() / "vlc.desktop", self.installDir() / "share/applications/vlc.desktop")
        if CraftCore.compiler.isMSVC():
            utils.deleteFile(self.installDir(), "lib", "vlccore.lib")
            utils.deleteFile(self.installDir() / "lib/vlc.lib")

        return True
