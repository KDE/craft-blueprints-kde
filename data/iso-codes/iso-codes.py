# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import glob
import os
import shutil

import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.20.1"]:
            self.targets[ver] = f"https://salsa.debian.org/iso-codes-team/iso-codes/-/archive/v{ver}/iso-codes-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"iso-codes-v{ver}"

        self.targetDigests["4.20.1"] = (["2d7d9f6084ab9ce6c534ce71a3dd5144b6e474f3c97616459a88f73f44a64bff"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Localized data for various ISO standards (e.g. country, language, language scripts, and currency names)"
        self.defaultTarget = "4.20.1"
        self.releaseManagerId = 1408

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        if not CraftCore.compiler.isAndroid:
            self.buildDependencies["libs/gettext"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        # remove deprecated and unused XML copy of the JSON data
        xmlDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()), "xml/iso-codes")
        shutil.rmtree(xmlDir, ignore_errors=True)

        # remove symlinked catalogs, we don't use those and androiddeployqt adds copies for each of those
        localeDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()), "locale")
        catalogs = glob.glob(os.path.join(localeDir, "**/*.mo"), recursive=True)
        for catalog in catalogs:
            if os.path.islink(catalog):
                os.unlink(catalog)

        # put pkgconfig files into the right location on Windows
        if CraftCore.compiler.isWindows:
            pkgConfigSrc = (
                self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig/iso-codes.pc"
            )
            pkgConfigDest = self.installDir() / "lib/pkgconfig/iso-codes.pc"
            if pkgConfigSrc.exists():
                utils.createDir(pkgConfigDest.parent)
                os.rename(pkgConfigSrc, pkgConfigDest)

        return True
