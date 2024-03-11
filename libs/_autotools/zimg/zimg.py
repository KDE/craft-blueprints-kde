import os
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *
from CraftCore import CraftCore

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "z image library: scaling, colorspace conversion, and dithering library"

        for ver in ["3.0.5"]:
            # We need to use git tags because the GitHub release archives to not contain the submodules
            self.svnTargets[ver] = f"https://github.com/sekrit-twc/zimg.git||release-{ver}"

        self.svnTargets["master"] = "https://github.com/sekrit-twc/zimg.git"
        self.defaultTarget = "3.0.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # if self.package.isInstalled: # this is causing rebuild every time
        #     PackageBase.unmerge(self) # else build picks old incompatible includes

        if CraftCore.compiler.isAndroid:
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64:
                architecture = "aarch64"
                toolchain = "aarch64-linux-android"
                compiler = "aarch64-linux-android"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.arm32:
                architecture = "arm"
                toolchain = "arm-linux-androideabi"
                compiler = "armv7a-linux-androideabi"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
                architecture = "x86"
                toolchain = "i686-linux-android"
                compiler = "i686-linux-android"
            else:
                architecture = CraftCore.compiler.androidArchitecture
                toolchain = f"{CraftCore.compiler.androidArchitecture}-linux-android"
                compiler = f"{CraftCore.compiler.androidArchitecture}-linux-android"
            toolchain_path = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")
            libgcc_filename = subprocess.run([f"{toolchain_path}/{compiler}{CraftCore.compiler.androidApiLevel()}-clang", "-print-libgcc-file-name"], stdout=subprocess.PIPE, universal_newlines=True).stdout.strip()

            # workaround for https://github.com/android/ndk/issues/1614
            self.subinfo.options.configure.ldflags += f"{libgcc_filename}"

    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True
