import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.19'] = "http://download.sourceforge.net/lcms/lcms-1.19.tar.gz"
        self.targetInstSrc['1.19'] = "lcms-1.19"
        if CraftCore.compiler.isWindows:
            self.patchToApply['1.19'] = ('lcms-1.19-20101212.diff', 1)
        self.targetDigests['1.19'] = (['80ae32cb9f568af4dc7ee4d3c05a4c31fc513fc3e31730fed0ce7378237273a9'], CraftHash.HashAlgorithm.SHA256)
        self.description = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = '1.19'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None

if not CraftCore.compiler.isWindows:
    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.args += " --disable-static "
else:
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            # both examples and tests can be run here
            self.subinfo.options.configure.args += "-DBUILD_TESTS=OFF -DBUILD_SAMPLES=ON -DBUILD_TOOLS=OFF"

