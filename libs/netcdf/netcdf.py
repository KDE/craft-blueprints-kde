import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/Unidata/netcdf-c.git"
        for ver in ["4.6.0", "4.7.3"]:
            self.targets[ver] = f"https://github.com/Unidata/netcdf-c/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"netcdf-c-{ver}"
        self.targetDigests['4.6.0'] = (
            ['6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.7.3'] = (
            ['05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'A set of software libraries and self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data'
        self.defaultTarget = '4.7.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/hdf5"] = None
        self.runtimeDependencies["libs/libcurl"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        hdf5dir = os.path.join(CraftStandardDirs.craftRoot(), "cmake", "hdf5")
        # -DBUILD_TESTSETS=OFF -DENABLE_PARALLEL_TESTS=OFF -DENABLE_UNIT_TESTS=OFF
        self.subinfo.options.configure.args = f"-DHDF5_DIR={hdf5dir} -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF"
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += "-DCMAKE_CXX_FLAGS='-DH5_BUILT_AS_DYNAMIC_LIB'"
