# -*- coding: utf-8 -*-
import info
from Package import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        for ver in ["15.0.2", "15.0.7", "16.0.1"]:
            self.targets[ver] = f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{ver}/llvm-project-{ver}.src.tar.xz"
            self.targetInstSrc[ver] = f"llvm-project-{ver}.src"
            self.targetConfigurePath[ver] = "llvm"
            self.patchToApply[ver] = [("llvm-15.0.2-20221030.diff", 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply[ver] += [("llvm-15.0.2-20221107.diff", 1), ("1b9fbc81ff15f6ad5a0e7f29c486c6edd0bce94c.patch", 1)]
        self.targetDigests["15.0.2"] = (
            ["7877cd67714728556a79e5ec0cc72d66b6926448cf73b12b2cb901b268f7a872"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["16.0.1"] = (
            ["ab7e3b95adb88fd5b669ca8c1d3c1e8d2a601c4478290d3ae31d8d70e96f2064"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.patchLevel["15.0.2"] = 2

        self.description = "The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines."
        self.webpage = "http://llvm.org/"
        self.tags = "clang, clang-tools-extra"
        self.defaultTarget = "16.0.1"

    def setDependencies(self):
        # workaround, ensure system clang is used to build bjam
        self.buildDependencies["libs/boost/boost-bjam"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["libs/libzstd"] = None
        self.buildDependencies["dev-utils/python3"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        self.subinfo.options.configure.args += [
            "-DLLVM_ENABLE_PROJECTS=clang;clang-tools-extra;lld",
            # "-DLLVM_ENABLE_RUNTIMES=libunwind",
            "-DLLVM_BUILD_TESTS=OFF",
            "-DLLVM_INCLUDE_TESTS=OFF",
            "-DLLVM_INCLUDE_GO_TESTS=OFF",
            "-DLLVM_INCLUDE_EXAMPLES=OFF",
            "-DLLVM_BUILD_EXAMPLES=OFF",
            "-DLLVM_TARGETS_TO_BUILD=all",
            "-DLLVM_ENABLE_RTTI=ON",
            "-DLLVM_ENABLE_EH=ON",
            "-DLLVM_INCLUDE_DOCS=OFF",
            "-DLLVM_INSTALL_UTILS=ON",
            "-DLLVM_OPTIMIZED_TABLEGEN=ON",
            # Limit the maximum number of concurrent link jobs to 1. This should fix low amount of memory issue for link.
            "-DLLVM_PARALLEL_LINK_JOBS=1",
        ]
        # allow gcc < 5
        self.subinfo.options.configure.args += ["-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=ON"]

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += ["-DLLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON"]
            # CMake Error at CMakeLists.txt:555 (message): BUILD_SHARED_LIBS options is not supported on Windows
            self.subinfo.options.configure.args += ["-DBUILD_SHARED_LIBS=OFF"]
        elif CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DLLVM_BUILD_LLVM_DYLIB=ON"]
        else:
            self.subinfo.options.configure.args += ["-DBUILD_SHARED_LIBS=ON"]

        # lldb by default needs SWIG for the Python integration
        # disable this support until we have a swig package in Craft
        self.subinfo.options.configure.args += ["-DLLDB_DISABLE_PYTHON=ON"]

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if CraftCore.compiler.isMinGW():
            files = os.listdir(os.path.join(self.buildDir(), "lib"))
            for f in files:
                if f.endswith("dll.a"):
                    src = os.path.join(self.buildDir(), "lib", f)
                    dest = os.path.join(self.installDir(), "lib", f)
                    if not os.path.exists(dest):
                        utils.copyFile(src, dest, False)
        elif CraftCore.compiler.isMSVC():
            utils.copyFile(
                os.path.join(self.buildDir(), "lib", "clang.lib"),
                os.path.join(self.installDir(), "lib", "craft_clang_plugins.lib"),
            )

        return True

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            # wrapper for python scripts
            root = Path(CraftCore.standardDirs.craftRoot())
            if not utils.createShim(
                os.path.join(self.installDir(), "bin", "git-clang-format.exe"),
                root / "dev-utils/bin/python3.exe",
                [root / "bin/git-clang-format"],
                useAbsolutePath=True,
            ):
                return False
        return True
