import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "library for the FITS (Flexible Image Transport System) file format"

        self.defaultTarget = "4.0.0"
        self.targets[self.defaultTarget] = f"http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"cfitsio-{self.defaultTarget}"
        self.targetDigests["4.0.0"] = (["b2a8efba0b9f86d3e1bd619f662a476ec18112b4f27cc441cc680a4e3777425e"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DUSE_CURL=OFF"]
