# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["4.6.0"]:
            self.targets[ver] = f"https://salsa.debian.org/iso-codes-team/iso-codes/-/archive/iso-codes-{ver}/iso-codes-iso-codes-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"iso-codes-iso-codes-{ver}"

        self.targetDigests["4.6.0"] = (['c1f5204d4913fba25fdcae6ff5fe9606135717301f99c9ab0b225235023e7d9f'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Localized data for various ISO standards (e.g. country, language, language scripts, and currency names)"
        self.defaultTarget = "4.6.0"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.isAndroid:
            self.buildDependencies["libs/gettext"] = None

from Package.AutoToolsPackageBase import *
import shutil

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )

    def postInstall(self):
        # remove deprecated and unused XML copy of the JSON data
        xmlDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()), "xml/iso-codes")
        shutil.rmtree(xmlDir, ignore_errors=True)
        return True
