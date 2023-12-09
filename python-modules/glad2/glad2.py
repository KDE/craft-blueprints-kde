# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2023 George Florea Bănuș <georgefb899@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.PipPackageBase import *

class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Multi-Language Vulkan/GL/GLES/EGL/GLX/WGL Loader-Generator based on the official specs. "
        self.defaultTarget = "master"

class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
