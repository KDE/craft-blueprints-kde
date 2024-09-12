# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.6.0"]:
            self.targets[ver] = f"https://salsa.debian.org/iso-codes-team/iso-codes/-/archive/iso-codes-{ver}/iso-codes-iso-codes-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"iso-codes-iso-codes-{ver}"

        self.targetDigests["4.6.0"] = (["c1f5204d4913fba25fdcae6ff5fe9606135717301f99c9ab0b225235023e7d9f"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Localized data for various ISO standards (e.g. country, language, language scripts, and currency names)"
        self.defaultTarget = "4.6.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.platform.isAndroid:
            self.buildDependencies["libs/gettext"] = None


import glob
import shutil

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
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
        if CraftCore.compiler.platform.isWindows:
            pkgConfigSrc = (
                self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig/iso-codes.pc"
            )
            pkgConfigDest = self.installDir() / "lib/pkgconfig/iso-codes.pc"
            if pkgConfigSrc.exists():
                utils.createDir(pkgConfigDest.parent)
                os.rename(pkgConfigSrc, pkgConfigDest)

        return True
