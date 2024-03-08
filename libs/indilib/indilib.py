# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def fixLibraryFolder(self, folder):
        craftLibDir = CraftCore.standardDirs.craftRoot() / "lib"
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
                # Note: The following code is to correct hard coded links to homebrew
                # The links are often caused by different camera manufacturer's binary libraries, not built by us.
                if (
                    path == "/usr/local/lib/libusb-1.0.0.dylib"
                    or path == "/usr/local/opt/libusb/lib/libusb-1.0.0.dylib"
                    or path == "@loader_path/libusb-1.0.0.dylib"
                ):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath/libusb-1.0.dylib"), library])
            if library.endswith(".dylib"):
                utils.system(["install_name_tool", "-id", os.path.join("@rpath", os.path.basename(library)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__(self):
        super().__init__()
        craftLibDir = CraftCore.standardDirs.craftRoot() / "lib"
        self.subinfo.options.configure.args += [
            "-DCMAKE_MACOSX_RPATH=1",
            f"-DCMAKE_INSTALL_RPATH={craftLibDir}",
        ]
