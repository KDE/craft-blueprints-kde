import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git"
        for ver in ["1.10.5"]:
            self.targets[ver] = f"https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-{ver}/src/hdf5-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"hdf5-{ver}"
            self.archiveNames[ver] = f"hdf5-{ver}.tar.gz"
        self.targetDigests['1.10.5'] = (
            ['6d4ce8bf902a97b050f6f491f4268634e252a63dadd6656a1a9be5b7b7726fa8'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'A data model, library, and file format for storing and managing data'
        self.defaultTarget = '1.10.5'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF"
