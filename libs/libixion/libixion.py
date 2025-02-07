import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = (
            "a general purpose formula parser, interpreter, formula cell dependency tracker and spreadsheet document model backend all in one package"
        )

        for ver in ["0.19.0"]:
            self.targets[ver] = f"https://gitlab.com/api/v4/projects/ixion%2Fixion/packages/generic/source/{ver}/libixion-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libixion-{ver}"
        self.targetDigests["0.19.0"] = (["b4864d7a55351a09adbe9be44e5c65b1d417e80e946c947951d0e8428b9dcd15"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.19.0"] = [("libixion-0.19.0_WIN32.patch", 1)]
        self.patchToApply["0.19.0"] += [("libixion-0.19.0_boost.patch", 1)]
        if CraftCore.compiler.isMSVC() or CraftCore.compiler.isMacOS:
            self.patchToApply["0.19.0"] += [("libixion-0.19.0_MSVC.patch", 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["0.19.0"] += [("mdds-2.1.1_MSVC-c++17.patch", 1)]

        self.defaultTarget = "0.19.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost"] = None
        self.buildDependencies["libs/mdds"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # help pkg-config (mdds is in share/pkgconfig, python3 in lib/pkgconfig)
        self.subinfo.options.configure.args += (
            f'PKG_CONFIG_PATH="{CraftCore.standardDirs.craftRoot()}/lib/pkgconfig:{CraftCore.standardDirs.craftRoot()}/share/pkgconfig"'
        )
        self.subinfo.options.configure.args += f'CPPFLAGS="-I{CraftCore.standardDirs.craftRoot()}/include"'
        if CraftCore.compiler.isMacOS:
            # currently breaks signing bue to ixion.so in lib/python3.11/site-packages
            self.subinfo.options.configure.args += "--disable-python"
        if CraftCore.compiler.isMSVC():
            # MSVC explicitly needs to update __cplusplus
            # https://devblogs.microsoft.com/cppblog/msvc-now-correctly-reports-__cplusplus/
            self.subinfo.options.configure.cxxflags += "/Zc:__cplusplus -showIncludes"
            # TODO: use Boost version
            self.subinfo.options.configure.cxxflags += f" -I{CraftCore.standardDirs.craftRoot()}/include/boost-1_86"
            self.subinfo.options.configure.args += f'CPPFLAGS="-I{CraftCore.standardDirs.craftRoot()}/include/boost-1_86"'
            self.subinfo.options.configure.args += f'LIBS="-link -LIBPATH:{CraftCore.standardDirs.craftRoot()}/lib"'
