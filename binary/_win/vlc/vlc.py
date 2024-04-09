import info
from Package.BinaryPackageBase import *


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
        utils.copyDir(self.sourceDir(), os.path.join(self.installDir(), "bin"))
        if CraftCore.compiler.isMinGW():
            utils.deleteFile(os.path.join(self.installDir(), "bin", "libgcc_s_seh-1.dll"))
        utils.mergeTree(os.path.join(self.installDir(), "bin", "sdk", "include"), os.path.join(self.installDir(), "include"))
        utils.mergeTree(os.path.join(self.installDir(), "bin", "sdk", "lib"), os.path.join(self.installDir(), "lib"))
        utils.rmtree(os.path.join(self.installDir(), "bin", "sdk"))
        os.makedirs(os.path.join(self.installDir(), "share", "applications"))
        utils.copyFile(os.path.join(self.blueprintDir(), "vlc.desktop"), os.path.join(self.installDir(), "share", "applications", "vlc.desktop"))
        if CraftCore.compiler.isMSVC():
            utils.deleteFile(os.path.join(self.installDir(), "lib", "vlccore.lib"))
            utils.deleteFile(os.path.join(self.installDir(), "lib", "vlc.lib"))

        return True
