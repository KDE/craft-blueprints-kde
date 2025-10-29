# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase

# attention: if you want to build ebook-tools with msvc, please apply the msvc-toC89.diff patch first
# currently msvc gets problems when compiling it


class subinfo(info.infoclass):
    def setTargets(self):
        svnurl = "https://ebook-tools.svn.sourceforge.net/svnroot/ebook-tools/"
        self.svnTargets["svnHEAD"] = svnurl + "trunk/ebook-tools"
        for ver in ["0.2.1", "0.2.2"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/ebook-tools/ebook-tools-{ver}.tar.gz"
            self.targetInstSrc[ver] = "ebook-tools-" + ver
            ver2 = ver.split(".")
            # no patches for versions >= 0.2.2:
            if not (int(ver2[0]) >= 0 and int(ver2[1]) >= 2 and int(ver2[2]) >= 2):
                self.patchToApply[ver] = [(f"ebook-tools-{ver}.diff", 1)]

        self.targetDigests["0.2.1"] = "1340eb7141b453088d39e62bba771413053a6d18"
        self.targetDigests["0.2.2"] = "1f10bef62c9125cf804366134e486a58308f07ff"

        self.description = "Tools for accessing and converting various ebook file formats"
        self.defaultTarget = "0.2.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzip"] = None
        self.runtimeDependencies["libs/libxml2"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
