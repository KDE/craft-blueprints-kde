import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "library for the FITS (Flexible Image Transport System) file format"

        for ver in ["4.0.0", "4.3.0", "4.6.2"]:
            self.targets[ver] = f"https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"cfitsio-{ver}"
        self.targetDigests["4.0.0"] = (["b2a8efba0b9f86d3e1bd619f662a476ec18112b4f27cc441cc680a4e3777425e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.3.0"] = (["fdadc01d09cf9f54253802c5ec87eb10de51ce4130411415ae88c30940621b8b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.6.2"] = (["66fd078cc0bea896b0d44b120d46d6805421a5361d3a5ad84d9f397b1b5de2cb"], CraftHash.HashAlgorithm.SHA256)

        self.releaseManagerId = 270
        self.webpage = "https://heasarc.gsfc.nasa.gov/fitsio/"
        self.defaultTarget = "4.6.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DUSE_CURL=OFF"]
