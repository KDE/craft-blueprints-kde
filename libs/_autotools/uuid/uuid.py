import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.3"]:
            self.targets[ver] = f'https://downloads.sourceforge.net/sourceforge/libuuid/libuuid-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'libuuid-{ver}'
        self.targetDigests["1.0.3"] = (["46af3275291091009ad7f1b899de3d0cea0252737550e7919d17237997db5644"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Portable uuid C library."
        self.defaultTarget = '1.0.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += "--disable-static --enable-shared "
