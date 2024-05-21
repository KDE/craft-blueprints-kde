import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git"
        for ver in ["1.10.8"]:
            self.targets[ver] = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-{ver}/src/hdf5-{ver}.tar.gz"
            self.archiveNames[ver] = f"hdf5-{ver}.tar.gz"
        for ver in ["1.12.1"]:
            self.targets[ver] = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-{ver}/src/hdf5-{ver}.tar.bz2"
        for ver in ["1.14.3"]:
            self.targets[ver] = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.14/hdf5-{ver}/src/hdf5-{ver}.tar.bz2"
        for ver in ["1.10.8", "1.12.1", "1.14.3"]:
            self.targetInstSrc[ver] = f"hdf5-{ver}"

        self.targetDigests["1.10.8"] = (["d341b80d380dd763753a0ebe22915e11e87aac4e44a084a850646ff934d19c80"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.12.1"] = (["aaf9f532b3eda83d3d3adc9f8b40a9b763152218fa45349c3bc77502ca1f8f1c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.14.3"] = (["9425f224ed75d1280bb46d6f26923dd938f9040e7eaebf57e66ec7357c08f917"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A data model, library, and file format for storing and managing data"

        self.defaultTarget = "1.14.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DHDF5_ENABLE_Z_LIB_SUPPORT=ON"]
        # build with the 1.10 APIs
        if self.buildTarget == "1.12.1" or self.buildTarget == "1.14.3":
            self.subinfo.options.configure.args += ["-DDEFAULT_API_VERSION:STRING=v110"]
