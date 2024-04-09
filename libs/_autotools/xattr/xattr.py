# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["libs/gettext"] = None

    def setTargets(self):
        self.description = "Commands for Manipulating Filesystem Extended Attributes"
        self.svnTargets["master"] = "https://git.savannah.nongnu.org/git/attr.git"
        for ver in ["2.5.1"]:
            self.targets[ver] = f"https://download.savannah.nongnu.org/releases/attr/attr-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"attr-{ver}"
        self.targetDigests["2.5.1"] = (["db448a626f9313a1a970d636767316a8da32aede70518b8050fa0de7947adc32"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.5.1"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = True
        self.subinfo.options.configure.ldflags += " -lintl"
        if self.subinfo.options.buildStatic:
            self.subinfo.options.configure.args += ["--enable-static=yes", "--enable-shared=no"]
        else:
            self.subinfo.options.configure.args += ["--enable-static=no", "--enable-shared=yes"]
