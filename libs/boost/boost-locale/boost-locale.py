import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.parent.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setBuildOptions(self):
        info.infoclass.setBuildOptions(self)

        self.options.configure.args += "-sICONV_PATH"
        # self.options.configure.args += " -DBUILD_TESTS=OFF"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
        self.buildDependencies["libs/boost/boost-bjam"] = None
        self.buildDependencies["libs/iconv"] = None


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)
