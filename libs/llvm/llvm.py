# -*- coding: utf-8 -*-
import os

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        for ver in ["15.0.2", "15.0.7", "16.0.1", "17.0.6", "18.1.2"]:
            self.targets[ver] = f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{ver}/llvm-project-{ver}.src.tar.xz"
            self.targetInstSrc[ver] = f"llvm-project-{ver}.src"
            self.targetConfigurePath[ver] = "llvm"
            self.patchToApply[ver] = []
            if CraftCore.compiler.isMSVC():
                self.patchToApply[ver] += [("llvm-15.0.2-20221107.diff", 1)]
        self.patchToApply["16.0.1"] += [(".16.0.1", 1)]
        self.patchToApply["17.0.6"] += [(".17.0.6", 1)]
        self.patchToApply["18.1.2"] += [(".17.0.6", 1)]
        self.patchToApply["18.1.2"] += [(".18.1.2", 1)]
        self.targetDigests["15.0.2"] = (
            ["7877cd67714728556a79e5ec0cc72d66b6926448cf73b12b2cb901b268f7a872"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["16.0.1"] = (
            ["ab7e3b95adb88fd5b669ca8c1d3c1e8d2a601c4478290d3ae31d8d70e96f2064"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["17.0.6"] = (
            ["58a8818c60e6627064f312dbf46c02d9949956558340938b71cf731ad8bc0813"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["18.1.2"] = (
            ["51073febd91d1f2c3b411d022695744bda322647e76e0b4eb1918229210c48d5"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.patchLevel["15.0.2"] = 3
        self.patchLevel["16.0.1"] = 2
        self.patchLevel["18.1.2"] = 2

        self.description = "The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines."
        self.webpage = "http://llvm.org/"
        self.tags = "clang, clang-tools-extra"
        self.defaultTarget = "18.1.2"

    def setDependencies(self):
        # workaround, ensure system clang is used to build bjam
        self.buildDependencies["libs/boost/boost-bjam"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["libs/libzstd"] = None
        self.buildDependencies["dev-utils/python3"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.supportsClang = False
        self.subinfo.options.configure.args += [
            "-DLLVM_ENABLE_PROJECTS=clang;clang-tools-extra;lld",
            # "-DLLVM_ENABLE_RUNTIMES=libunwind",
            "-DLLVM_BUILD_TESTS=OFF",
            "-DLLVM_INCLUDE_TESTS=OFF",
            "-DLLVM_INCLUDE_GO_TESTS=OFF",
            "-DLLVM_INCLUDE_EXAMPLES=OFF",
            "-DLLVM_BUILD_EXAMPLES=OFF",
            "-DLLVM_INCLUDE_BENCHMARKS=OFF",
            "-DLLVM_BUILD_BENCHMARKS=OFF",
            "-DLLVM_TARGETS_TO_BUILD=X86;AArch64",
            "-DLLVM_ENABLE_RTTI=ON",
            "-DLLVM_ENABLE_EH=ON",
            # The problem with the DIA SDK is that the Path to the DIA library
            # depends on the MSVC version, so if this tool was build with Commercial
            # and I'm using Community, clang will fail to configure as
            # the library will be missing.
            "-DLLVM_ENABLE_DIA_SDK=OFF",
            "-DLLVM_INCLUDE_DOCS=OFF",
            "-DLLVM_INSTALL_UTILS=ON",
            "-DLLVM_OPTIMIZED_TABLEGEN=ON",
            # we use kshimgen on Windows
            "-DLLVM_USE_SYMLINKS=ON",
        ]
        # allow gcc < 5
        self.subinfo.options.configure.args += ["-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=ON"]

        # build static in general
        self.subinfo.options.dynamic.buildStatic = True
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += ["-DLLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON"]
            # CMake Error at CMakeLists.txt:555 (message): BUILD_SHARED_LIBS options is not supported on Windows
        elif CraftCore.compiler.isMinGW():
            # LLVM_BUILD_LLVM_DYLIB would result in "error: export ordinal too large: 72285"
            self.subinfo.options.dynamic.buildStatic = True
        else:
            # generate a shared lib from the gathered static libs
            self.subinfo.options.configure.args += ["-DLLVM_BUILD_LLVM_DYLIB=ON", "-DLLVM_LINK_LLVM_DYLIB=ON"]

        # lldb by default needs SWIG for the Python integration
        # disable this support until we have a swig package in Craft
        self.subinfo.options.configure.args += ["-DLLDB_DISABLE_PYTHON=ON"]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMinGW():
            files = os.listdir(self.buildDir() / "lib")
            for f in files:
                if f.endswith("dll.a"):
                    src = self.buildDir() / "lib" / f
                    dest = self.installDir() / "lib" / f
                    if not os.path.exists(dest):
                        utils.copyFile(src, dest, False)
        elif CraftCore.compiler.isMSVC():
            utils.copyFile(
                self.buildDir() / "lib/clang.lib",
                self.installDir() / "lib/craft_clang_plugins.lib",
            )

        return True

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            # wrapper for python scripts
            root = CraftCore.standardDirs.craftRoot()
            if not utils.createShim(
                self.installDir() / "bin/git-clang-format.exe",
                root / "dev-utils/bin/python3.exe",
                [root / "bin/git-clang-format"],
                useAbsolutePath=True,
            ):
                return False
        return True
