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


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.4", "1.10.4", "1.11.4", "1.11.8", "1.11.14"]:
            self.targets[ver] = f"http://dbus.freedesktop.org/releases/dbus/dbus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dbus-{ver}"
            self.targetConfigurePath[ver] = "cmake"

        self.svnTargets["master"] = "git://anongit.freedesktop.org/git/dbus/dbus"
        self.targetSrcSuffix["master"] = "git"
        self.targetConfigurePath["master"] = "cmake"

        self.patchToApply["1.8.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.10.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.11.4"] = [("dbus-1.11.4-20160903.diff", 1)]
        self.patchToApply["1.11.14"] = [("dbus-1.11.4-20160903.diff", 1),
                                        ("dbus-fix_data_dir.diff", 1)]
        self.patchLevel["1.11.14"] = 2

        self.targetDigests["1.10.4"] = "ec1921a09199c81ea20b20448237146a414d51ae"
        self.targetDigests["1.11.4"] = (
            ["474de2afde8087adbd26b3fc5cbf6ec45559763c75b21981169a9a1fbac256c9"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.8'] = (
            ['fa207530d694706e33378c87e65b2b4304eb99fff71fc6d6caa6f70591b9afd5'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.14'] = (
            ['55cfc7fdd2cccb2fce1f75d2132ad4801b5ed6699fc2ce79ed993574adf90c80'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Freedesktop message bus system (daemon and clients)"
        self.webpage = "http://www.freedesktop.org/wiki/Software/dbus/"
        self.defaultTarget = "1.11.14"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/expat"] = "default"
        self.runtimeDependencies["libs/glib"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = (
            "-DDBUS_BUILD_TESTS=OFF "
            "-DDBUS_ENABLE_XML_DOCS=OFF ")

        if (self.buildType() == "Release"):
            self.subinfo.options.configure.args += (
                "-DDBUS_ENABLE_VERBOSE_MODE=OFF "
                "-DDBUS_DISABLE_ASSERTS=ON ")
        elif (self.buildType() == "Debug"):
            self.subinfo.options.configure.args += "-DDBUS_ENABLE_VERBOSE_MODE=ON "

        self.subinfo.options.configure.args += (
            "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path "
            "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path "
            "-DDBUS_SYSTEM_BUS_DEFAULT_ADDRESS:STRING=autolaunch:scope=*install-path ")

        if OsUtils.isWin():
            # kde uses debugger output, so dbus should do too
            self.subinfo.options.configure.args += "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON "
            self.subinfo.options.configure.args += "-DCMAKE_INSTALL_DATADIR:STRING=bin/data "

        if OsUtils.isMac():
            self.subinfo.options.configure.args += "-DDBUS_BUILD_X11:BOOL=OFF "

    def install(self):
        if not CMakePackageBase.install(self): return False
        # TODO: fix
        if self.buildType() == "Debug":
            imagedir = os.path.join(self.installDir(), "lib")
            if CraftCore.compiler.isMSVC():
                if os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1d.lib"), os.path.join(imagedir, "dbus-1.lib"))
                if not os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1.lib"), os.path.join(imagedir, "dbus-1d.lib"))
            if CraftCore.compiler.isMinGW():
                if os.path.exists(os.path.join(imagedir, "libdbus-1.dll.a")):
                    utils.copyFile(os.path.join(imagedir, "libdbus-1.dll.a"),
                                   os.path.join(imagedir, "libdbus-1d.dll.a"))

        return True
