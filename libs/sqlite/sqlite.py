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
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.8.1.0'] = 'http://sqlite.org/2013/sqlite-amalgamation-3080100.zip'
        self.targets['3.15.0'] = 'https://sqlite.org/2016/sqlite-amalgamation-3150000.zip'
        self.targets['3.24.0'] = 'https://sqlite.org/2018/sqlite-amalgamation-3240000.zip'

        self.targetDigests['3.8.1.0'] = '75a1ab154e796d2d1b391a2c7078679e15512bda'
        self.targetDigests['3.15.0'] = (
            ['356109b55f76a9851f9bb90e8e3d722da222e26f657f76a471fdf4d7983964b9'], CraftHash.HashAlgorithm.SHA256)

        self.targetDigests['3.24.0'] = (
            ['ad68c1216c3a474cf360c7581a4001e952515b3649342100f2d7ca7c8e313da6'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['3.8.1.0'] = [("sqlite_cmake_and_wince_20130124.diff", 1)]
        self.patchToApply['3.15.0'] = [("sqlite-amalgamation-3150000-20161021.diff", 1)]
        self.patchToApply['3.15.0'] += [("sqlite-pkgconfig-file-20180728.diff", 1)]
        self.patchLevel['3.15.0'] = 2
        self.patchToApply['3.24.0'] = [("sqlite-amalgamation-3150000-20161021.diff", 1)]
        self.patchToApply['3.24.0'] += [("sqlite-pkgconfig-file-20180728.diff", 1)]
        self.patchLevel['3.24.0'] = 2

        self.targetInstSrc['3.8.1.0'] = "sqlite-amalgamation-3080100"
        self.targetInstSrc['3.15.0'] = "sqlite-amalgamation-3150000"
        self.targetInstSrc['3.24.0'] = "sqlite-amalgamation-3240000"

        self.description = "a library providing a self-contained, serverless, zero-configuration, transactional SQL database engine"
        self.defaultTarget = '3.24.0'

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if OsUtils.isMac():
            pass

            # /usr/lib/libsqlite3.dylib is version 9.0.0
            # %CraftRoot%/lib/libsqlite3.dylib is version 3.0.0
            # Akonadi tried to link to the first one,
            # while the second one is packaged into the final package.
            # Since 2018-07-28 SQLite can be found through PKGConfig,
            # so let's see if below error will persist without static library.

            # Build sqlite as static library under macOS
            # Otherwise we might run into:
            # executing command: .../macdeployqt .../kdevelop.app -always-overwrite -verbose=1
            # dyld: Library not loaded: /usr/lib/libsqlite3.dylib
            #  Referenced from: /System/Library/Frameworks/Security.framework/Versions/A/Security
            #  Reason: Incompatible library version: Security requires version 9.0.0 or later, but libsqlite3.dylib provides version 3.0.0
            # self.subinfo.options.configure.args += " -DSTATIC_LIBRARY=TRUE"

    def configure(self):
        CMakeListsFile = os.path.join(self.sourceDir(), "CMakeLists.txt")
        with open(CMakeListsFile, "rt") as f:
            content = f.read()

        content = content.replace(r"set(SQLITE_VERSION_MINOR 15)", r"set(SQLITE_VERSION_MINOR %s)" % self.version.split(".")[1])

        with open(CMakeListsFile, "wt") as f:
            f.write(content)

        return super().configure()

    def install(self):

        isInstalled = super().install()

        if isInstalled and OsUtils.isMac():
            # allow finding sqlite library by pkgconfig module
            # otherwise e.g. Akonadi finds /usr/lib/libsqlite3.dylib
            # instead of Craft's sqlite library
            pkgConfigDir = os.path.join(self.installDir(), "lib", "pkgconfig")
            pkgConfigFile = os.path.join(pkgConfigDir, "sqlite3.pc")
            utils.createDir(pkgConfigDir)
            utils.copyFile(os.path.join(self.sourceDir(), "sqlite.pc.in"), pkgConfigFile)

            with open(pkgConfigFile, "rt") as f:
                content = f.read()

            content = content.replace(r"@prefix@", CraftCore.standardDirs.craftRoot())
            content = content.replace(r"@exec_prefix@", r"${prefix}/bin")
            content = content.replace(r"@libdir@", r"${prefix}/lib")
            content = content.replace(r"@includedir@", r"${prefix}/include")
            content = content.replace(r"@RELEASE@", self.version)

            with open(pkgConfigFile, "wt") as f:
                f.write(content)

        return isInstalled


