# -*- coding: utf-8 -*-
import info
from Package import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.supportsClang = False
        self.subinfo.options.configure.args = "-DLLVM_TARGETS_TO_BUILD='X86'"

        # BEGIN: sub-package handling
        self.subPackages = []
        def maybeAddSubPackage(pkg, cmakeDefine):
            if not pkg.isIgnored():
                self.subinfo.options.configure.args += " -D%s=\"%s\"" % (cmakeDefine, pkg.instance.sourceDir().replace("\\", "/"))
                self.subPackages.append(pkg.instance)

        maybeAddSubPackage(CraftPackageObject.get('win32libs/llvm-meta/clang'),
                           "LLVM_EXTERNAL_CLANG_SOURCE_DIR")
        maybeAddSubPackage(CraftPackageObject.get('win32libs/llvm-meta/clang-tools-extra'),
                           "LLVM_EXTERNAL_CLANG_TOOLS_EXTRA_SOURCE_DIR")
        maybeAddSubPackage(CraftPackageObject.get('win32libs/llvm-meta/lld'),
                           "LLVM_EXTERNAL_LLD_SOURCE_DIR")
        maybeAddSubPackage(CraftPackageObject.get('win32libs/llvm-meta/lldb'),
                           "LLVM_EXTERNAL_LLDB_SOURCE_DIR")
        # END: sub-package handling

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += " -DLLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON"
        else:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"

    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        for p in self.subPackages:
            if not p.fetch():
                return False
        return True

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        for p in self.subPackages:
            if not p.unpack():
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
                    dest = os.path.join(self.imageDir(), "lib", f)
                    if not os.path.exists(dest):
                        utils.copyFile(src, dest, False)

        if OsUtils.isWin():
            exeSuffix = ".exe"
        else:
            exeSuffix = ""

        # the build system is broken so....
        src = os.path.join(self.imageDir(), "bin", "clang" + exeSuffix)
        if CraftCore.compiler.isGCCLike():
            dest = os.path.join(self.imageDir(), "bin", "clang++" + exeSuffix)
        elif CraftCore.compiler.isMSVC():
            dest = os.path.join(self.imageDir(), "bin", "clang-cl" + exeSuffix)
        else:
            CraftCore.log.error("Unknown compiler")
        if not os.path.exists(dest):
            utils.copyFile(src, dest)
        return True
