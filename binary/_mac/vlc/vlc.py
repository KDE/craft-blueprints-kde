import shutil

import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    vlc_ver = None

    def setTargets(self):
        for ver in ["2.2.6", "2.2.7", "2.2.8", "3.0.0", "3.0.1", "3.0.2", "3.0.3", "3.0.4", "3.0.5", "3.0.6"]:
            self.targets[ver] = f"http://download.videolan.org/pub/videolan/vlc/{ver}/macosx/vlc-{ver}.dmg"
            self.targetInstSrc[ver] = f"vlc-{ver}"
            self.targetDigestUrls[ver] = f"http://download.videolan.org/pub/videolan/vlc/{ver}/macosx/vlc-{ver}.dmg.sha256"
            self.patchToApply[ver] = [("vlc-plugin-headers.diff", 1)]
        self.webpage = "https://www.videolan.org/"
        self.description = "an open-source multimedia framework"

        self.defaultTarget = "3.0.6"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        for filename in self.localFileNames():
            utils.system("hdiutil attach -mountpoint %s %s"%(os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path, "temp"),
                os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path, filename)))
            utils.copyDir(os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path, "temp", "VLC.app"),
                os.path.join(self.workDir(), "VLC.app"), linkOnly=False)
            
            for patch, depth in self.subinfo.patchesToApply():
                utils.applyPatch(self.workDir(), os.path.join(self.packageDir(), patch), depth)

            utils.system('hdiutil detach %s'%os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path, "temp"))

        return True

    def install(self):

        utils.mergeTree(os.path.join(self.workDir(), "VLC.app", "Contents", "MacOS", "include"),
                    os.path.join(self.installDir(), "include"))
        utils.mergeTree(os.path.join(self.workDir(), "VLC.app", "Contents", "MacOS", "lib"), os.path.join(self.installDir(), "lib"))
        print(self.installDir())

        return True
