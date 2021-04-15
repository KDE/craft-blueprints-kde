import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "x264 video coding library"
        git = {'20210211': 'b86ae3c66f51ac9eab5ab7ad09a9d62e67961b8a', # fails to build on centos7
               '20180806': '0a84d986e7020f8344f00752e3600b9769cc1e85'} # last to build
        for ver in git.keys():
            self.targets[ver] = f"https://code.videolan.org/videolan/x264/-/archive/{git[ver]}/x264-{git[ver]}.tar.bz2"
            self.targetInstSrc[ver] = f"x264-{git[ver]}"
        self.targetDigests['20180806'] = (['e8f54662a5c4b0c4da91fd6e69b6a6f45b3292c1aee1279e8cfa916790407337'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '20210211'

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # if self.package.isInstalled: # this is causing rebuild every time
        #     PackageBase.unmerge(self) # else build picks old incompatible includes
        self.subinfo.options.configure.args = "--enable-shared --disable-cli --disable-avs--disable-lavf --disable-swscale --disable-ffms --disable-gpac --enable-pic"


    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True

