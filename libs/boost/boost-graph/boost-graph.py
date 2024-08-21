import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.parent.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = "https://www.boost.org/"

        self.description = "portable C++ libraries"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
        self.buildDependencies["libs/boost/boost-bjam"] = None


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
