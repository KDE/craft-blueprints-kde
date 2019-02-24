import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.33"]:
            self.targets[ver] = f'https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v{ver}/util-linux-{ver}.tar.xz'
            self.targetInstSrc[ver] = f'util-linux-{ver}'
        self.targetDigests["2.33"] = (['f261b9d73c35bfeeea04d26941ac47ee1df937bd3b0583e748217c1ea423658a'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.33'

    def setDependencies(self):
        self.buildDependencies["dev-utils/python2"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/zlib"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += "--disable-static --enable-shared  --disable-all-programs  --enable-libuuid"
