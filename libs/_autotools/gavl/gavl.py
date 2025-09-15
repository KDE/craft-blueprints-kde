import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.0"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/gmerlin/gavl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gavl-{ver}"

        for ver in ["2.0.0pre2"]:
            self.targets[ver] = f"https://github.com/bplaum/gavl/releases/download/v{ver}/gavl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gavl-{ver}"

        self.targetDigests["1.4.0"] = (["51aaac41391a915bd9bad07710957424b046410a276e7deaff24a870929d33ce"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.4.0"] = ("FixCputest.patch", 1)
        self.patchLevel["1.4.0"] = 1

        self.svnTargets["master"] = "https://github.com/bplaum/gavl.git||main"
        self.patchLevel["master"] = 20220321
        # when adding new commit based targets, keep gnutls dependency (below) in mind!
        self.svnTargets["59dd12a"] = "https://github.com/bplaum/gavl.git||59dd12a812141828538e045697148b7a66359181"
        self.patchLevel["59dd12a"] = 2

        self.description = "Low level library, upon which multimedia APIs can be built"
        self.webpage = "https://github.com/bplaum/gavl"
        if CraftCore.compiler.isMacOS or CraftCore.compiler.isLinux:
            self.defaultTarget = "59dd12a"
        else:
            self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.buildTarget in ["master", "59dd12a"]:
            self.runtimeDependencies["libs/gnutls"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--without-doxygen", "--disable-libpng"]
        self.subinfo.options.configure.cflags += " -Wno-implicit-function-declaration"
