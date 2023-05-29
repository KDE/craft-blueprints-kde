import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.8.0', '1.9.0']:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "libvpx-" + ver
        self.targetDigests['1.8.0'] = (['86df18c694e1c06cc8f83d2d816e9270747a0ce6abe316e93a4f4095689373f6'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.9.0'] = (['d279c10e4b9316bf11a570ba16c3d55791e1ad6faa4404c67422eb631782c80a'], CraftHash.HashAlgorithm.SHA256)
        self.description = "VP8 and VP9 video codec"
        self.defaultTarget = '1.9.0'
        self.patchToApply["1.9.0"] = [("detect-clang.diff", 1)]
        if CraftCore.compiler.isFreeBSD:
            self.patchToApply["1.9.0"] += [("dont-check-for-diff.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/pthreads"] = None
        self.buildDependencies["dev-utils/nasm"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.noDataRootDir = True
        self.platform = ""
        self.subinfo.options.configure.args += ["--disable-examples", "--disable-install-docs",
                                                "--disable-unit-tests", "--disable-avx512"]
        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["--enable-shared"]
