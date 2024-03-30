# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

from Package.CMakePackageBase import *


class Pattern(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON", "-DQT_MAJOR_VERSION=6"]
