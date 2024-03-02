# -*- coding: utf-8 -*-
# Copyright 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
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
        self.versionInfo.setDefaultValues()
        self.description = "a personal finance manager for KDE"
        self.displayName = "KMyMoney"
        self.defaultTarget = "5.1"

    def setDependencies(self):
        if CraftCore.compiler.isWindows:
            self.buildDependencies["dev-utils/subversion"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        if self.buildTarget != "master":
            self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["libs/gpgme/gpgmepp"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kholidays"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/libofx"] = None
        self.runtimeDependencies["libs/libical"] = None
        self.runtimeDependencies["libs/sqlcipher"] = None
        self.runtimeDependencies["libs/pulseaudio"] = None
        if not CraftCore.compiler.isMSVC():
            self.runtimeDependencies["libs/aqbanking"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["extragear/libalkimia"] = None
        self.runtimeDependencies["extragear/kdiagram"] = None
        self.buildDependencies["libs/gettext"] = None
        if self.buildTarget != "master":
            self.runtimeDependencies["libs/qt/qtwebengine"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        else:
            self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/qt5/qtserialport"] = None
        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["kdesupport/kdewin"] = None


from Package.CMakePackageBase import *
from Packager.AppImagePackager import AppImagePackager


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DFETCH_TRANSLATIONS=ON"]

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DENABLE_WOOB=OFF"]

    def install(self):
        if not CMakePackageBase.install(self):
            return False

        # For AppImages create a gpgconf.ctl file that forces gpgconf to use the actual APPDIR
        # as rootdir and not the ci build dir which causes gpg operations to fail.
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            with open(os.path.join(self.installDir(), "bin", "gpgconf.ctl"), "wt") as f:
                f.write("rootdir=${APPDIR}/usr")
        return True

    def createPackage(self):
        self.defines["executable"] = "bin\\kmymoney.exe"  # Windows-only, mac is handled implicitly
        self.defines["icon"] = os.path.join(self.blueprintDir(), "kmymoney.ico")
        self.defines["mimetypes"] = [
            "application/x-kmymoney",
            "application/x-ofx",
            "application/vnd.intu.qfx",
            "application/x-qfx",
            "application/x-qif",
            "text/csv",
        ]
        self.defines["file_types"] = [".kmy", ".ofx", ".qfx", ".qif", ".csv"]
        self.defines["website"] = "https://kmymoney.org/"

        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist_mac.txt"))

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
