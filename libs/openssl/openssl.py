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


class subinfo(info.infoclass):
    def setTargets(self):
        def addTarget(baseUrl, ver):
            self.targets[ver] = f'{baseUrl}openssl-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'openssl-{ver}'
            self.targetDigestUrls[ver] = ([f'{baseUrl}openssl-{ver}.tar.gz.sha256'], CraftHash.HashAlgorithm.SHA256)

        # latest versions -> inside source/
        for ver in ["1.0.2s", "1.1.1d"]:
            baseUrl = 'https://openssl.org/source/'
            addTarget(baseUrl, ver)

        self.patchLevel["1.1.1d"] = 1

        self.description = "The OpenSSL runtime environment"

        #set the default config for openssl 1.1
        self.options.configure.args = "shared no-zlib threads no-rc5 no-idea no-ssl3-method no-weak-ssl-ciphers no-heartbeats no-dynamic-engine"

        self.defaultTarget = '1.1.1d'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        if CraftCore.compiler.isMinGW():
            # TODO: remove when we drop < 1.1
            self.runtimeDependencies["libs/zlib"] = None
            self.buildDependencies["dev-utils/msys"] = None
        elif CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-utils/nasm"] = None

    @property
    def opensslUseLegacyBuildSystem(self):
        return CraftVersion(self.buildTarget) < CraftVersion("1.1")



from Package.CMakePackageBase import *


class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.staticBuild = False
        self.supportsNinja = False
        self.subinfo.options.make.supportsMultijob = False
        if not self.subinfo.opensslUseLegacyBuildSystem:
            self.subinfo.options.install.args = "install_sw"

    def configure( self, defines=""):
        if self.subinfo.opensslUseLegacyBuildSystem:
            return True
        else:
            self.enterBuildDir()
            prefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
            return utils.system(["perl", os.path.join(self.sourceDir(), "Configure"), f"--prefix={prefix}"]
                                + self.subinfo.options.configure.args.split(" ")
                                + ["-FS",
                                    f"-I{OsUtils.toUnixPath(os.path.join(CraftStandardDirs.craftRoot(), 'include'))}",
                                    "VC-WIN64A" if CraftCore.compiler.isX64() else "VC-WIN32"])


    def compile(self):
        if not self.subinfo.opensslUseLegacyBuildSystem:
            return super().compile()
        else:
            self.enterSourceDir()
            cmd = ""
            if CraftCore.compiler.isX64():
                config = "VC-WIN64A"
            else:
                config = "VC-WIN32"

            if not utils.system("perl Configure %s" % config):
                return False

            if CraftCore.compiler.isX64():
                if not utils.system("ms\do_win64a.bat"):
                    return False
            else:
                if not utils.system("ms\do_nasm.bat"):
                    return False

            if self.staticBuild:
                cmd = r"nmake -f ms\nt.mak"
            else:
                cmd = r"nmake -f ms\ntdll.mak"

            return utils.system(cmd)

    def install(self):
        if not self.subinfo.opensslUseLegacyBuildSystem:
            return super().install()
        else:
            src = self.sourceDir()
            dst = self.imageDir()

            if not os.path.isdir(dst):
                os.mkdir(dst)
            if not os.path.isdir(os.path.join(dst, "bin")):
                os.mkdir(os.path.join(dst, "bin"))
            if not os.path.isdir(os.path.join(dst, "lib")):
                os.mkdir(os.path.join(dst, "lib"))
            if not os.path.isdir(os.path.join(dst, "include")):
                os.mkdir(os.path.join(dst, "include"))

            if self.staticBuild:
                outdir = "out32"
            else:
                outdir = "out32dll"

            if not self.staticBuild:
                shutil.copy(os.path.join(src, outdir, "libeay32.dll"), os.path.join(dst, "bin"))
                shutil.copy(os.path.join(src, outdir, "ssleay32.dll"), os.path.join(dst, "bin"))
            shutil.copy(os.path.join(src, outdir, "libeay32.lib"), os.path.join(dst, "lib"))
            shutil.copy(os.path.join(src, outdir, "ssleay32.lib"), os.path.join(dst, "lib"))
            utils.copyDir(os.path.join(src, "inc32"), os.path.join(dst, "include"))

            return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        if CraftCore.compiler.isMinGW():
            if CraftCore.compiler.isX64():
                self.platform = "mingw64"
            else:
                self.platform = "mingw"
        else:
            self.subinfo.options.configure.projectFile = "config"
            self.platform = ""
        self.supportsCCACHE = False
        self.subinfo.options.configure.noDataRootDir = True
        if not self.subinfo.opensslUseLegacyBuildSystem:
            self.subinfo.options.install.args = "install_sw"
        else:
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.useShadowBuild = False

            # target install needs perl with native path on configure time
            self.subinfo.options.configure.args = " shared zlib-dynamic enable-camellia enable-idea enable-mdc2 enable-tlsext enable-rfc3779"

        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative() and CraftCore.compiler.isX86():
            self.subinfo.options.configure.args += " linux-x86"
            self.subinfo.options.configure.projectFile = "Configure"

    def make(self, dummyBuildType=None):
        if not self.subinfo.opensslUseLegacyBuildSystem:
            return super().make()
        else:
            return self.shell.execute(self.sourceDir(), self.makeProgram, "depend") and \
                AutoToolsPackageBase.make(self, dummyBuildType)

    def install(self):
        self.subinfo.options.make.supportsMultijob = False
        if not self.subinfo.opensslUseLegacyBuildSystem:
            # TODO: don't install doc
            if not super().install():
                return False
            # we don't want people to link to the static build but openssl doesn't provide an option to
            # disable the static build
            return (utils.deleteFile(os.path.join(self.installDir(), "lib", "libcrypto.a")) and
                    utils.deleteFile(os.path.join(self.installDir(), "lib", "libssl.a")))
        else:
            self.enterSourceDir()
            self.shell.execute(self.sourceDir(), self.makeProgram,
                            "INSTALLTOP=%s install_sw" % (self.shell.toNativePath(self.imageDir())))
            if OsUtils.isWin():
                self.shell.execute(os.path.join(self.imageDir(), "lib"), "chmod", "-R 664 .")
                self.shell.execute(os.path.join(self.imageDir(), "lib", "engines"), "chmod", " -R 755 .")
                self.shell.execute(os.path.join(self.imageDir(), "bin"), "chmod", " -R 755 .")
                shutil.move(os.path.join(self.imageDir(), "lib", "libcrypto.dll.a"),
                            os.path.join(self.imageDir(), "lib", "libeay32.dll.a"))
                shutil.move(os.path.join(self.imageDir(), "lib", "libssl.dll.a"),
                            os.path.join(self.imageDir(), "lib", "ssleay32.dll.a"))
            return True

if CraftCore.compiler.isGCCLike() and not CraftCore.compiler.isMSVC():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass
