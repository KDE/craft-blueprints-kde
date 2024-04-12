import shutil

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targets["1.80.0"] = "https://files.kde.org/craft/sources/libs/boost/boost_1_80_0.tar.gz"
        self.targetDigests["1.80.0"] = (["4b2136f98bdd1f5857f1c3dea9ac2018effe65286cf251534b6ae20cc45e1847"], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://www.boost.org/"

        self.description = "portable C++ libraries"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.packSources = True
        # we can't cache this as we might need the src for the uncached boost modules
        self.subinfo.options.package.disableBinaryCache = True

    def make(self):
        return True

    def install(self):
        if not super().install():
            return False
        shutil.copytree(os.path.join(self.sourceDir(), "boost"), os.path.join(self.imageDir(), "include", "boost"))  # disable autolinking
        f = open(os.path.join(self.imageDir(), "include", "boost", "config", "user.hpp"), "a")
        f.write("#define BOOST_ALL_NO_LIB\n")
        f.close()
        return True
