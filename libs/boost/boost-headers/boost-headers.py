import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests["1_65_1"] = (['a13de2c8fbad635e6ba9c8f8714a0e6b4264b60a29b964b940a22554705b6b60'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1_67_0"] = (['8aa4e330c870ef50a896634c931adf468b21f8a69b77007e45c444151229f665'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['1_55_0'] = [('boost_1_54_0-spirit-20131114.diff', 1)]
        self.patchToApply['1_56_0'] = [
            ('boost_1_56_0-spirit-20131114.diff', 1)]  # TODO: also include in future releases!
        self.patchToApply['1_57_0'] = [('boost_1_56_0-spirit-20131114.diff', 1)]

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)
        self.subinfo.options.package.packSources = True
        # we can't cache this as we might need the src for the uncached boost modules
        self.subinfo.options.package.disableBinaryCache = True

    def make(self):
        return True

    def install(self):
        shutil.copytree(os.path.join(self.sourceDir(), 'boost'),
                        os.path.join(self.imageDir(), 'include', 'boost'))  # disable autolinking
        f = open(os.path.join(self.imageDir(), 'include', 'boost', 'config', 'user.hpp'), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True
