import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "library that provides a collection of standalone file processing filters for spreadsheet formats"

        for ver in ["0.19.2"]:
            self.targets[ver] = f"https://gitlab.com/api/v4/projects/orcus%2Forcus/packages/generic/source/{ver}/liborcus-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"liborcus-{ver}"
        self.targetDigests["0.19.2"] = (["69ed26a00d4aaa7688e62a6e003cbc81928521a45e96605e53365aa499719e39"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.19.2"] = [("liborcus-0.19.2-boost.patch", 1)]

        self.defaultTarget = "0.19.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost"] = None
        self.buildDependencies["libs/libixion"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # help pkg-config (mdds is in share/pkgconfig, python3 in lib/pkgconfig)
        self.subinfo.options.configure.args += f'PKG_CONFIG_PATH="{CraftCore.standardDirs.craftRoot()}/lib/pkgconfig:{CraftCore.standardDirs.craftRoot()}/share/pkgconfig"'
        self.subinfo.options.configure.args += f'CPPFLAGS="-I{CraftCore.standardDirs.craftRoot()}/include"'
        # self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
