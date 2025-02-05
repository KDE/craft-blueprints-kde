# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "A Python framework to work with Lottie files and Telegram animated stickers."
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        # workaround for lottie installing a file that is only needed at build time
        # and breaks signing on macOS, better would be to fix it upstream
        if CraftCore.compiler.isMacOS:
            utils.deleteFile(self.installDir() / "lib/Python.framework/Versions/Current/.version_full")
        return True
