import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "x264 video coding library"
        for ver in ['20180119-2245', '20180806-2245-stable']:
            self.targets[ ver ] = f"https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"x264-snapshot-{ver}"
        self.targetDigests['20180806-2245-stable'] = (['958e78e7563f0018285ebdbff563fb22db89b0abf3649d7e914abd9d50785fc6'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['20180119-2245'] = (['c9162e612f989c8d97c7a6bb3924a04f43d14221dcc983c69fb9ab12613c3669'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["20180119-2245"] = 1
        self.defaultTarget = '20180119-2245'

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-shared --disable-cli --disable-avs--disable-lavf --disable-swscale --disable-ffms --disable-gpac --enable-pic"


    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True

