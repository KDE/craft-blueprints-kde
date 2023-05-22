import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "x264 video coding library"
        self.svnTargets['eaa68fa'] = "https://github.com/mirror/x264.git||eaa68fad9e5d201d42fde51665f2d137ae96baf0"
        self.patchToApply["eaa68fa"] = [("shebang-fix.diff", 1)]
        if CraftCore.compiler.isWindows:
            # copy make file instead of creating a symlink
            self.patchToApply["eaa68fa"] = [("fix-paths-and-symlinks-win.diff", 1)]

        self.defaultTarget = 'eaa68fa'

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        if self.package.isInstalled: # this is causing rebuild every time
            PackageBase.unmerge(self) # else build picks old incompatible includes
        self.subinfo.options.configure.args = "--enable-shared --disable-cli --disable-avs --disable-lavf --disable-swscale --disable-ffms --disable-gpac --enable-pic"


    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True

