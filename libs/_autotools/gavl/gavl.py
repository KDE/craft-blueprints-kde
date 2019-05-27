import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.4.0']:
            self.targets[ver] = f"https://downloads.sourceforge.net/gmerlin/gavl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gavl-{ver}"
        self.targetDigests['1.4.0'] = (['51aaac41391a915bd9bad07710957424b046410a276e7deaff24a870929d33ce'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['1.4.0'] = ('FixCputest.patch', 1)

        self.description = "Low level library, upon which multimedia APIs can be built"
        self.webpage = "https://gmerlin.sourceforge.net"
        self.defaultTarget = '1.4.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ' --without-doxygen --disable-libpng'
