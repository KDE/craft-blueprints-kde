# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = (
            "library that provides a collection of standalone file processing filters for spreadsheet formats"
        )

        for ver in ["0.20.0"]:
            self.targets[ver] = f"https://gitlab.com/orcus/orcus/-/archive/{ver}/orcus-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"orcus-{ver}"
        self.targetDigests["0.20.0"] = (["767ddd06d72b18c5e6c65af74a78b8c7b9326c7163fde1066b97369769a68f35"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.20.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost"] = None
        self.buildDependencies["libs/mdds"] = None
        self.runtimeDependencies["libs/ixion"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # to find mdds and ixion header
        self.subinfo.options.configure.args += [
            f'-DMDDS_INCLUDEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/mdds-3.0',
            f'-DIXION_INCLUDEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/include/ixion-0.20'
        ]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += [
                '-DCMAKE_CXX_FLAGS="-EHsc -DBOOST_ALL_NO_LIB -DBOOST_PROGRAM_OPTIONS_DYN_LINK"',
                f'-DCMAKE_SHARED_LINKER_FLAGS="-LIBPATH:{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/lib boost_filesystem-vc143-mt-x64-1_86.lib boost_program_options-vc143-mt-x64-1_86.lib"',
                f'-DCMAKE_EXE_LINKER_FLAGS="-LIBPATH:{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/lib boost_program_options-vc143-mt-x64-1_86.lib boost_filesystem-vc143-mt-x64-1_86.lib"'
            ]
        if CraftCore.compiler.isLinux or CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += [
                f'-DCMAKE_SHARED_LINKER_FLAGS=-L{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/lib -lboost_filesystem -lboost_program_options',
                f'-DCMAKE_EXE_LINKER_FLAGS=-L{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/lib -lboost_filesystem -lboost_program_options'
            ]
