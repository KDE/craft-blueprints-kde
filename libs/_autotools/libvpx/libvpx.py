import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.7.0","1.8.0"]:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "libvpx-" + ver
        self.targetDigests['1.7.0'] = (['1fec931eb5c94279ad219a5b6e0202358e94a93a90cfb1603578c326abfc1238'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.8.0'] = (['86df18c694e1c06cc8f83d2d816e9270747a0ce6abe316e93a4f4095689373f6'], CraftHash.HashAlgorithm.SHA256)
        self.description = "VP8 and VP9 video codec"
        self.defaultTarget = '1.8.0'

    def setDependencies(self):
        self.runtimeDependencies["libs/pthreads"] = None
        self.buildDependencies["dev-utils/nasm"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.noDataRootDir = True
        self.platform = ""
        self.subinfo.options.configure.args += "--disable-examples --disable-install-docs --disable-unit-tests --disable-avx512 "
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += " --enable-shared"

