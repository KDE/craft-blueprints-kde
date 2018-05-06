import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.7.0"]:
            self.targets[ver] = f"https://chromium.googlesource.com/webm/libvpx/+archive/v{ver}.tar.gz"
        self.targetDigests['1.7.0'] = (['542cb556dabff1f2caea1643aa6f528ded0d55261aef71702dad761af7fbeac0'], CraftHash.HashAlgorithm.SHA256)
        self.description = "VP8 and VP9 video codec"
        self.defaultTarget = '1.7.0'

    def setDependencies(self):
        self.runtimeDependencies["libs/pthreads"] = None
        self.buildDependencies["dev-utils/nasm"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.noDataRootDir = True
        self.platform = ""
        self.subinfo.options.configure.args += "--disable-examples --disable-install-docs"
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += " --enable-shared"

