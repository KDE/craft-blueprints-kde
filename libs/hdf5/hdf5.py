# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git"

        for ver in ["1.14.3"]:
            self.targets[ver] = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.14/hdf5-{ver}/src/hdf5-{ver}.tar.bz2"
        self.targets["1.14.6"] = "https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6/downloads/hdf5-1.14.6.tar.gz"
        for ver in ["1.14.3", "1.14.6"]:
            self.targetInstSrc[ver] = f"hdf5-{ver}"

        self.targetDigests["1.14.3"] = (["9425f224ed75d1280bb46d6f26923dd938f9040e7eaebf57e66ec7357c08f917"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.14.6"] = (["e4defbac30f50d64e1556374aa49e574417c9e72c6b1de7a4ff88c4b1bea6e9b"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A data model, library, and file format for storing and managing data"

        self.defaultTarget = "1.14.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DHDF5_ENABLE_Z_LIB_SUPPORT=ON"]
