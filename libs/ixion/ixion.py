import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppImagePackager import AppImagePackager
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = (
            "a general purpose formula parser, interpreter, formula cell dependency tracker and spreadsheet document model backend all in one package"
        )

        for ver in ["0.20.0"]:
            self.targets[ver] = f"https://gitlab.com/ixion/ixion/-/archive/{ver}/ixion-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"ixion-{ver}"
        self.targetDigests["0.20.0"] = (["39e54cd486fed458c2a6e83a5e658d4c2e818862355b33645bb1342449428463"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.20.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost"] = None
        self.buildDependencies["libs/mdds"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # to find mdds header
        self.subinfo.options.configure.args += f'-DMDDS_INCLUDEDIR="{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/mdds-3.0"'
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += '-DCMAKE_CXX_FLAGS="-EHsc -DBOOST_ALL_NO_LIB"'
        if CraftCore.compiler.isLinux and isinstance(self, AppImagePackager):
            self.subinfo.options.configure.args += '-DCMAKE_SHARED_LINKER_FLAGS="-ldl"'
