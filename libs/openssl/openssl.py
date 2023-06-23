# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import info
from Blueprints.CraftVersion import CraftVersion
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):
        def addTarget(baseUrl, ver):
            self.targets[ver] = f"{baseUrl}openssl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openssl-{ver}"
            self.targetDigestUrls[ver] = ([f"{baseUrl}openssl-{ver}.tar.gz.sha256"], CraftHash.HashAlgorithm.SHA256)

        # latest versions -> inside source/
        for ver in ["1.1.1i", "1.1.1k", "1.1.1l", "1.1.1n", "1.1.1q", "1.1.1s", "1.1.1t", "1.1.1u"]:
            baseUrl = "https://openssl.org/source/"
            addTarget(baseUrl, ver)

        self.description = "The OpenSSL runtime environment"

        # set the default config for openssl 1.1
        self.options.configure.args += [
            "shared",
            "no-zlib",
            "threads",
            "no-rc5",
            "no-idea",
            "no-ssl3-method",
            "no-weak-ssl-ciphers",
            "no-heartbeats",
            "no-dynamic-engine",
            "--libdir=lib",
        ]

        self.defaultTarget = "1.1.1u"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        if CraftCore.compiler.isMinGW():
            # TODO: remove when we drop < 1.1
            self.runtimeDependencies["libs/zlib"] = None
            self.buildDependencies["dev-utils/msys"] = None
        elif CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-utils/nasm"] = None


from Package.CMakePackageBase import *


class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.staticBuild = False
        self.supportsNinja = False
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.install.args += ["install_sw"]

        self.env = {}
        if CraftCore.compiler.isAndroid:
            ndkToolchainPath = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")
            self.env["PATH"] = os.pathsep.join([ndkToolchainPath, os.environ["PATH"]])
            self.subinfo.options.configure.args += [
                f"android-{CraftCore.compiler.androidArchitecture}",
                f"-D__ANDROID_API__={CraftCore.compiler.androidApiLevel()}",
            ]
            self.subinfo.options.make.args += " SHLIB_VERSION_NUMBER= SHLIB_EXT=_1_1.so"
            self.subinfo.options.install.args += ["SHLIB_VERSION_NUMBER=", "SHLIB_EXT=_1_1.so", f"DESTDIR={self.installDir()}"]

    def configure(self, defines=""):
        self.enterBuildDir()
        prefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        args = Arguments(["perl", os.path.join(self.sourceDir(), "Configure"), f"--prefix={prefix}"]) + self.subinfo.options.configure.args
        if not CraftCore.compiler.isAndroid:
            args += [
                "-FS",
                f"-I{OsUtils.toUnixPath(os.path.join(CraftStandardDirs.craftRoot(), 'include'))}",
                "VC-WIN64A" if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64 else "VC-WIN32",
            ]
        with utils.ScopedEnv(self.env):
            return utils.system(args)

    def compile(self):
        with utils.ScopedEnv(self.env):
            return super().compile()

    def postInstall(self):
        # remove API docs here as there is no build option for that
        baseDir = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot())
        return utils.rmtree(baseDir / "doc") and utils.rmtree(baseDir / "man") and utils.rmtree(self.installDir() / "html")


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        # https://github.com/openssl/openssl/issues/18720
        self.subinfo.options.configure.cflags += "-Wno-error=implicit-function-declaration"
        if CraftCore.compiler.isMinGW():
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                self.platform = "mingw64"
            else:
                self.platform = "mingw"
        else:
            self.subinfo.options.configure.projectFile = "config"
            self.platform = ""
        self.supportsCCACHE = False
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noLibDir = True
        self.subinfo.options.install.args += ["install_sw"]

        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative() and CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
            self.subinfo.options.configure.args += ["linux-x86"]
            self.subinfo.options.configure.projectFile = "Configure"

    def install(self):
        self.subinfo.options.make.supportsMultijob = False
        # TODO: don't install doc
        if not super().install():
            return False
        # we don't want people to link to the static build but openssl doesn't provide an option to
        # disable the static build
        return utils.deleteFile(os.path.join(self.installDir(), "lib", "libcrypto.a")) and utils.deleteFile(os.path.join(self.installDir(), "lib", "libssl.a"))


if CraftCore.compiler.isGCCLike() and not CraftCore.compiler.isMSVC() and not CraftCore.compiler.isAndroid:

    class Package(PackageMSys):
        pass

else:

    class Package(PackageCMake):
        pass
