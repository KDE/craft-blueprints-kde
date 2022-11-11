# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2022 KDE e.V.
# SPDX-FileContributor: Ingo Klöcker <dev@ingo-kloecker.de>

from pathlib import Path
import stat

import info
import utils

from Package.SourceOnlyPackageBase import SourceOnlyPackageBase

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.targets["this"] = ""
        self.targetInstallPath["this"] = "dev-utils/bin"
        self.defaultTarget = "this"


class Package(SourceOnlyPackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        # nothing to fetch
        return True

    def unpack(self):
        # nothing to unpack
        return True

    def install(self):
        utils.createDir(self.installDir())
        for f in (self.packageDir() / 'src' / 'linuxdeploy-plugin-craft.sh',):
            src = Path(f)
            dest = Path(self.installDir()) / src.name
            if not utils.copyFile(src, dest):
                return False
            dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
