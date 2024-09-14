import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


#
# this library is used by kdeedu/kstars
# the library is c-only
#
class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.15.0"] = "download.sourceforge.net/libnova/libnova-0.15.0.tar.gz"
        self.targetInstSrc["0.15.0"] = "libnova-0.15.0"
        self.targetDigests["0.15.0"] = (["7c5aa33e45a3e7118d77df05af7341e61784284f1e8d0d965307f1663f415bb1"], CraftHash.HashAlgorithm.SHA256)
        # self.patchToApply['0.15.0'] = [('libnova-20101215.diff', 1),
        #                                     ('libnova-20130629.diff', 1)]
        self.patchToApply["0.15.0"] = [
            ("libnova-remove-conflicting-definition.patch", 1)
        ]  # https://github.com/msys2/MINGW-packages/tree/92798d888cfaf779a83bae0a293a197d8825aac2/mingw-w64-libnova
        self.description = "a Celestial Mechanics, Astrometry and Astrodynamics library"
        self.defaultTarget = "0.15.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
