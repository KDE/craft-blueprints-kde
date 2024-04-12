import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.0"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/gmerlin/gavl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gavl-{ver}"
        self.targetDigests["1.4.0"] = (["51aaac41391a915bd9bad07710957424b046410a276e7deaff24a870929d33ce"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.4.0"] = ("FixCputest.patch", 1)
        self.svnTargets["master"] = "https://github.com/bplaum/gavl.git"
        self.patchLevel["master"] = 20220321
        # when adding new commit based targets, keep gnutls dependency (below) in mind!
        self.svnTargets["59dd12a"] = "https://github.com/bplaum/gavl.git||59dd12a812141828538e045697148b7a66359181"
        self.patchLevel["59dd12a"] = 1

        self.description = "Low level library, upon which multimedia APIs can be built"
        self.webpage = "https://gmerlin.sourceforge.net"
        if CraftCore.compiler.isMacOS:
            self.defaultTarget = "59dd12a"
        else:
            self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.buildTarget in ["master", "59dd12a"]:
            self.runtimeDependencies["libs/gnutls"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--without-doxygen", "--disable-libpng"]
