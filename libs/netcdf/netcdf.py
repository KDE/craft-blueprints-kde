import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/Unidata/netcdf-c.git"
        for ver in ["4.6.0", "4.7.3", "4.7.4"]:
            self.targets[ver] = f"https://github.com/Unidata/netcdf-c/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"netcdf-c-{ver}"
        self.targetDigests['4.6.0'] = (
            ['6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.7.3'] = (
            ['05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.7.4'] = (
            ['99930ad7b3c4c1a8e8831fb061cb02b2170fc8e5ccaeda733bd99c3b9d31666b'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'A set of software libraries and self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data'
        for ver in ["4.7.3", "4.7.4"]:
            self.patchToApply[ver] = [('netcdf-MSVC-install.diff', 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["4.7.4"] += [('netcdf-4.7.4-missing-defines.diff', 1)]
        self.defaultTarget = '4.7.4'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/hdf5"] = None
        # only required for DAP
        #self.runtimeDependencies["libs/libcurl"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.make.supportsMultijob = False

        hdf5dir = os.path.join(CraftStandardDirs.craftRoot(), "cmake", "hdf5")
        # -DBUILD_TESTSETS=OFF -DENABLE_PARALLEL_TESTS=OFF -DENABLE_UNIT_TESTS=OFF
        # DAP needs static libcurl
        self.subinfo.options.configure.args = f"-DHDF5_DIR={hdf5dir} -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DENABLE_DAP=OFF"
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += f" -DCMAKE_C_FLAGS=\"/D_WIN32\" -DPACKAGE_VERSION={self.subinfo.buildTarget}"

    def createPackage(self):
        return TypePackager.createPackage(self)
