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

import os

import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Native

    def setTargets(self):
        for ver in ["1.14.0", "1.14.4", "1.14.8"]:
            self.targets[ver] = f"http://dbus.freedesktop.org/releases/dbus/dbus-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"dbus-{ver}"

        self.svnTargets["master"] = "git://anongit.freedesktop.org/git/dbus/dbus"
        self.targetSrcSuffix["master"] = "git"

        self.targetDigests["1.14.0"] = (["ccd7cce37596e0a19558fd6648d1272ab43f011d80c8635aea8fd0bad58aebd4"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.14.0"] = [("0002-fix-macos-build.diff", 1)]
        self.description = "Freedesktop message bus system (daemon and clients)"
        self.webpage = "http://www.freedesktop.org/wiki/Software/dbus/"
        self.defaultTarget = "1.14.8"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/expat"] = None


class PackageCMake(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DDBUS_BUILD_TESTS=OFF", "-DDBUS_ENABLE_XML_DOCS=OFF"]

        if self.buildType() == "Debug":
            self.subinfo.options.configure.args += ["-DDBUS_ENABLE_VERBOSE_MODE=ON"]
        else:
            self.subinfo.options.configure.args += ["-DDBUS_ENABLE_VERBOSE_MODE=OFF", "-DDBUS_DISABLE_ASSERT=ON"]

        if CraftCore.compiler.isWindows:
            # kde uses debugger output, so dbus should do too
            self.subinfo.options.configure.args += [
                "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON",
                "-DCMAKE_INSTALL_DATADIR:STRING=bin/data",
                "-DENABLE_TRADITIONAL_ACTIVATION=ON",
                "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path",
                "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path",
                "-DDBUS_SYSTEM_BUS_DEFAULT_ADDRESS:STRING=autolaunch:scope=*install-path",
            ]

    def install(self):
        if not super().install():
            return False
        # TODO: fix
        if self.buildType() == "Debug":
            imagedir = self.installDir() / "lib"
            if CraftCore.compiler.isMSVC():
                if os.path.exists(imagedir / "dbus-1d.lib"):
                    utils.copyFile(imagedir / "dbus-1d.lib", imagedir / "dbus-1.lib")
                if not os.path.exists(imagedir / "dbus-1d.lib"):
                    utils.copyFile(imagedir / "dbus-1.lib", imagedir / "dbus-1d.lib")
            if CraftCore.compiler.isMinGW():
                if os.path.exists(imagedir / "libdbus-1.dll.a"):
                    utils.copyFile(imagedir / "libdbus-1.dll.a", imagedir / "libdbus-1d.dll.a")

        return True


class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += [
            "--disable-dependency-tracking",
            "--disable-static",
            "--disable-doxygen-docs",
            "--disable-xml-docs",
            "--enable-verbose-mode",
            "--without-x",
            "--disable-tests",
        ]
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += (
                "--enable-launchd " f"--with-launchd-agent-dir='{CraftCore.standardDirs.craftRoot() / 'Library/LaunchAgents'}' "
            )

    def postInstall(self):
        hardCodedFiles = []
        if CraftCore.compiler.isMacOS:
            hardCodedFiles += [self.installDir() / "Library/LaunchAgents/org.freedesktop.dbus-session.plist"]
        return self.patchInstallPrefix(hardCodedFiles, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())

    def postQmerge(self):
        if CraftCore.compiler.isMacOS:
            utils.system(["launchctl", "load", CraftCore.standardDirs.craftRoot() / "Library/LaunchAgents/org.freedesktop.dbus-session.plist"])
        return True


if not CraftCore.compiler.isWindows:

    class Package(PackageAutotools):
        pass

else:

    class Package(PackageCMake):
        pass
