# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2022 KDE e.V.
# SPDX-FileContributor: Ingo Klöcker <dev@ingo-kloecker.de>

import info

from Package.AutoToolsPackageBase import AutoToolsPackageBase

class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None  # FIXME: do we need this dependency?
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "PatchELF is a simple utility for modifying existing ELF executables and libraries."
        self.svnTargets["0.16.1"] = "https://github.com/NixOS/patchelf.git||0.16.1"
        self.defaultTarget = "0.16.1"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__(self)
        self.subinfo.options.configure.autoreconf = False

        # FIXME: configure static build ???
        # env LDFLAGS="-static -static-libgcc -static-libstdc++" ./configure --prefix=/usr
        # self.subinfo.options.configure.args += ["blabla", ...]

    def configure(self):
        if not self.shell.execute(self.sourceDir(), "./bootstrap.sh"):
            return False

        return super().configure()
