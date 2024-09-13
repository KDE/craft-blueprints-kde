import info
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # netcdf on MinGW does not work out of the box. It is a dependency of labplot which uses MSVC. Needs someone who cares.
        self.parent.package.categoryInfo.platforms &= (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMinGW() else CraftCore.compiler.Platforms.All
        )

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/Unidata/netcdf-c.git"
        for ver in ["4.6.0", "4.7.3", "4.7.4", "4.8.0", "4.9.2"]:
            self.targets[ver] = f"https://github.com/Unidata/netcdf-c/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"netcdf-c-{ver}"
        self.targetDigests["4.6.0"] = (["6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.7.3"] = (["05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.7.4"] = (["99930ad7b3c4c1a8e8831fb061cb02b2170fc8e5ccaeda733bd99c3b9d31666b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.8.0"] = (["aff58f02b1c3e91dc68f989746f652fe51ff39e6270764e484920cb8db5ad092"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.9.2"] = (["bc104d101278c68b303359b3dc4192f81592ae8640f1aee486921138f7f88cb7"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A set of software libraries and self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data"
        for ver in ["4.7.3", "4.7.4", "4.8.0"]:
            self.patchToApply[ver] = [("netcdf-MSVC-install.diff", 1)]
        for ver in ["4.7.4", "4.8.0"]:
            if CraftCore.compiler.isMSVC():
                self.patchToApply[ver] += [("netcdf-4.7.4-missing-defines.diff", 1)]
        for ver in ["4.8.0"]:
            if CraftCore.compiler.isMSVC():
                self.patchToApply[ver] += [("netcdf-4.8.0-missing-defines.diff", 1)]
        self.defaultTarget = "4.8.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/hdf5"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/libzip"] = None
        # only required for DAP
        # self.runtimeDependencies["libs/libcurl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.supportsNinja = False
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.make.supportsMultijob = False

        hdf5dir = CraftStandardDirs.craftRoot() / "cmake/hdf5"
        # -DENABLE_TESTS=OFF -DENABLE_EXAMPLE_TESTS=OFF -DENABLE_UNIT_TESTS=OFF -DENABLE_PARALLEL_TESTS=OFF
        # DAP needs static libcurl
        self.subinfo.options.configure.args = [f"-DHDF5_DIR={hdf5dir}", "-DENABLE_DAP=OFF"]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += ['-DCMAKE_C_FLAGS="/D_WIN32"', f"-DPACKAGE_VERSION={self.subinfo.buildTarget}"]
        # several errors building tests on macOS (clang 16?): incompatible function pointer types
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DENABLE_TESTS=OFF"]

    def createPackage(self):
        return super().createPackage()
