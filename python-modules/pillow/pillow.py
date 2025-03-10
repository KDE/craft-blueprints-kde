# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import os

import info
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.PipPackageBase import PipPackageBase
from utils import ScopedEnv


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Pillow is the friendly PIL fork. The Python Imaging Library adds image processing capabilities to your Python interpreter."
        self.defaultTarget = "master"

        # webp: provides the WebP format.
        self.runtimeDependencies["libs/webp"] = None
        # tiff: provides compressed TIFF functionality
        self.runtimeDependencies["libs/tiff"] = None
        # zlib: provides access to compressed PNGs
        self.runtimeDependencies["libs/zlib"] = None
        # openjpeg: provides JPEG 2000 functionality
        self.runtimeDependencies["libs/openjpeg"] = None
        # freetype: provides type related services
        self.runtimeDependencies["libs/freetype"] = None
        # libjpeg-turbo: provides JPEG functionality
        self.runtimeDependencies["libs/libjpeg-turbo"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        env = {}
        if CraftCore.compiler.isMSVC():
            env.update(
                {
                    "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include/python3.11'}",
                }
            )
        with ScopedEnv(env):
            return super().install()
