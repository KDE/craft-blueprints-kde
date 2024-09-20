import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.PackageBase import PackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "x264 video coding library"
        self.svnTargets["eaa68fa"] = "https://github.com/mirror/x264.git||eaa68fad9e5d201d42fde51665f2d137ae96baf0"
        self.patchToApply["eaa68fa"] = [("shebang-fix.diff", 1)]
        if CraftCore.compiler.isWindows:
            # copy make file instead of creating a symlink
            self.patchToApply["eaa68fa"] = [("fix-paths-and-symlinks-win.diff", 1)]

        self.defaultTarget = "eaa68fa"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = [
            "--disable-cli",
            "--disable-avs",
            "--disable-lavf",
            "--disable-swscale",
            "--disable-ffms",
            "--disable-gpac",
            "--enable-pic",
        ]
        if CraftCore.compiler.isAndroid and (
            CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64 or CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32
        ):
            self.subinfo.options.configure.args += ["--disable-asm"]

    def configure(self):
        if self.package.isInstalled:  # this is causing rebuild every time
            PackageBase.unmerge(self)  # else build picks old incompatible includes
        return super().configure()

    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True
