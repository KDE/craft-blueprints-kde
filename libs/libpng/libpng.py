import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.6.39", "1.6.40", "1.6.43"]:
            self.targets[ver] = "https://downloads.sourceforge.net/libpng/libpng-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "libpng-" + ver

        self.patchToApply["1.6.39"] = [("libpng-1.6.39-install.pc-on-windows.diff", 1), ("libpng-fix-android-shared-build.diff", 1)]
        self.patchToApply["1.6.40"] = [("libpng-1.6.40-install.pc-on-windows.diff", 1), ("libpng-android-remove-zlib-dependency.diff", 1)]
        self.patchToApply["1.6.43"] = []

        if CraftCore.compiler.isWindows or CraftCore.compiler.isAndroid:
            self.patchToApply["1.6.43"] += [
                ("libpng-1.6.40-install.pc-on-windows.diff", 1),
                ("libpng-android-remove-zlib-dependency.diff", 1),
            ]

        if CraftCore.compiler.isMinGW():
            # disable broken symlink creation
            self.patchToApply["1.6.43"] += [("libpng-1.6.43-20240730.diff", 1)]

        self.targetDigests["1.6.39"] = (["af4fb7f260f839919e5958e5ab01a275d4fe436d45442a36ee62f73e5beb75ba"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.40"] = (["8f720b363aa08683c9bf2a563236f45313af2c55d542b5481ae17dd8d183bb42"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.43"] = (["e804e465d4b109b5ad285a8fb71f0dd3f74f0068f91ce3cdfde618180c174925"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["1.6.39"] = 1
        self.patchLevel["1.6.40"] = 2
        self.patchLevel["1.6.43"] = 1

        self.description = "A library to display png images"
        self.defaultTarget = "1.6.43"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supportsCCACHE = False
        self.subinfo.options.configure.args += [
            "-DPNG_TESTS=OFF",
            "-DPNG_NO_STDIO=OFF",
            # don't add a postfix, we don't allow parallel install and this breaks the .pc
            "-DPNG_DEBUG_POSTFIX=",
        ]
        if CraftCore.compiler.isMacOS and self.subinfo.buildTarget == "1.6.39":
            self.subinfo.options.configure.args += ["-DPNG_ARM_NEON=off"]
        # PNG_EXECUTABLES is used for <= 1.6.40, PNG_TOOLS for > 1.6.40
        self.subinfo.options.configure.args += [
            f"-DPNG_EXECUTABLES={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-DPNG_TOOLS={self.subinfo.options.dynamic.buildTools.asOnOff}",
        ]
        if self.subinfo.options.buildStatic:
            self.subinfo.options.configure.args += ["-DPNG_STATIC=ON", "-DPNG_SHARED=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DPNG_STATIC=OFF", "-DPNG_SHARED=ON"]
