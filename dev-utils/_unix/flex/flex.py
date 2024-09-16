# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # We need this as a host tool. Craft at this point isn't set up to produce both
        # host and target binaries, so on Android we have host tools in the docker image.
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Native

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/gettext"] = None

    def setTargets(self):
        self.description = "Flex is a tool for generating scanners: programs which recognize lexical patterns in text."
        self.svnTargets["master"] = "https://github.com/westes/flex.git"
        for ver in ["2.6.4"]:
            self.targets[ver] = f"https://github.com/westes/flex/releases/download/v{ver}/flex-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"flex-{ver}"

        self.targetDigests["2.6.4"] = (["e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.6.4"] = [
            ("0001-flex-disable-documentation.patch", 1),
            ("0002-build-AC_USE_SYSTEM_EXTENSIONS-in-configure.ac.patch", 1),
        ]  # https://git.busybox.net/buildroot/commit/?id=c128c5f3c79b31d89256ffbc5c650ba613d3d52b
        self.defaultTarget = "2.6.4"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False
        # autoreconf is not enough here
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
