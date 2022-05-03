import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "x264 video coding library"
        git = {'20220326': '5db6aa6cab1b146e07b60cc1736a01f21da01154'}
        for ver in git.keys():
            self.targets[ver] = f"https://code.videolan.org/videolan/x264/-/archive/{git[ver]}/x264-{git[ver]}.tar.bz2"
            self.targetInstSrc[ver] = f"x264-{git[ver]}"
        self.targetDigests['20220326'] = (['05a60491ef2e96d7bd3487576fbfded2677d7185dd53f59e263d18d050b836de'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["20220326"] = [("shebang-fix.diff", 1)]
        if CraftCore.compiler.isWindows:
            # copy make file instead of creating a symlink
            self.patchToApply["20220326"] = [("fix-paths-and-symlinks-win.diff", 1)]

        self.defaultTarget = '20220326'

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # if self.package.isInstalled: # this is causing rebuild every time
        #     PackageBase.unmerge(self) # else build picks old incompatible includes
        self.subinfo.options.configure.args = "--enable-shared --disable-cli --disable-avs --disable-lavf --disable-swscale --disable-ffms --disable-gpac --enable-pic"


    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True

