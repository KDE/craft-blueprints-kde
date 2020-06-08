# -*- coding: utf-8 -*-
import info
from Package import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.0.1"] = 2
        self.patchLevel["6.0.0"] = 2
        self.patchLevel["7.0.1"] = 1
        self.patchLevel["8.0.0"] = 1
        if CraftCore.compiler.isMacOS:
            self.patchLevel["8.0.0"] += 1
        self.patchToApply["6.0.1"] = [("llvm-6.0.1-20181019.diff", 1)]
        self.patchToApply["7.0.1"] = [("llvm-7.0.1-20190118.diff", 1), ("llvm-7.0.1-20190102.diff", 1)]
        if CraftCore.compiler.isLinux:
            # don't just link against xml2 but use cmake logic...
            # don't apply this at Windows as it is used there for configurtion files...
            self.patchToApply["9.0.0"] = [("fix_libxml.diff", 1)]
            self.patchToApply["9.0.1"] = [("fix_libxml.diff", 1)]
        if not CraftCore.compiler.isMacOS:
            self.patchToApply["8.0.0"] = [("llvm-8.0.0-20190411.diff", 1)]

    def setDependencies(self):
        # workaround, ensure system clang is used to build bjam
        self.buildDependencies["libs/boost/boost-bjam"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["dev-utils/python3"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        self.subinfo.options.configure.args += " -DLLVM_BUILD_TESTS=OFF  -DLLVM_INCLUDE_TESTS=OFF -DLLVM_INCLUDE_GO_TESTS=OFF"
        self.subinfo.options.configure.args += " -DLLVM_TARGETS_TO_BUILD='host'"
        self.subinfo.options.configure.args += " -DLLVM_ENABLE_RTTI=ON -DLLVM_ENABLE_EH=ON -DLLVM_INCLUDE_DOCS=OFF -DLLVM_INSTALL_UTILS=ON -DLLVM_OPTIMIZED_TABLEGEN=ON -DLLVM_TARGETS_TO_BUILD=all"
        # allow gcc < 5
        self.subinfo.options.configure.args += " -DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=ON"

        # BEGIN: sub-package handling
        self.subPackages = []
        def maybeAddSubPackage(pkg, cmakeDefine):
            if not pkg.isIgnored():
                self.subinfo.options.configure.args += f" -D{cmakeDefine}=\"{OsUtils.toUnixPath(pkg.instance.sourceDir())}\""
                self.subPackages.append(pkg.instance)

        maybeAddSubPackage(CraftPackageObject.get('libs/llvm-meta/clang'),
                           "LLVM_EXTERNAL_CLANG_SOURCE_DIR")
        maybeAddSubPackage(CraftPackageObject.get('libs/llvm-meta/clang-tools-extra'),
                           "LLVM_EXTERNAL_CLANG_TOOLS_EXTRA_SOURCE_DIR")
        maybeAddSubPackage(CraftPackageObject.get('libs/llvm-meta/lld'),
                           "LLVM_EXTERNAL_LLD_SOURCE_DIR")

        # END: sub-package handling

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += " -DLLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON"
        elif CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += " -DLLVM_BUILD_LLVM_DYLIB=ON"
        else:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"

        # lldb by default needs SWIG for the Python integration
        # disable this support until we have a swig package in Craft
        self.subinfo.options.configure.args += " -DLLDB_DISABLE_PYTHON=ON"

    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        for p in self.subPackages:
            if not p.fetch(noop=False):
                return False
        return True

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        for p in self.subPackages:
            if not p.unpack(noop=False):
                return False
        return True

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
            utils.copyFile(os.path.join(self.buildDir(), "lib", "clang.lib"),
                           os.path.join(self.installDir(), "lib", "craft_clang_plugins.lib"))

        # the build system is broken so....
        src = os.path.join(self.installDir(), "bin", f"clang{CraftCore.compiler.executableSuffix}")
        def maybeCopy(dest):
            dest = f"{dest}{CraftCore.compiler.executableSuffix}"
            if not os.path.exists(dest):
                return utils.copyFile(src, dest)
            else:
                return True

        if CraftCore.compiler.isMSVC():
            if not maybeCopy(os.path.join(self.installDir(), "bin", "clang-cl")):
                return False
        return maybeCopy(os.path.join(self.installDir(), "bin", "clang++"))

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            # wrapper for python scripts
            root = Path(CraftCore.standardDirs.craftRoot())
            if not utils.createShim(os.path.join(self.installDir(), "bin","git-clang-format.exe"), root / "dev-utils/bin/python3.exe", [ root/ "bin/git-clang-format"], useAbsolutePath=True):
                return False
        return True
