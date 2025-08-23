# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Mauritius Clemens <gitlab@janitor.chat>

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    # This defines the basic information about your software package (both the basic
    # metainformation like human readable names, where the source comes from, and
    # what other blueprints it depends on).
    def setTargets(self):
        # The human-readable name of the main binary
        self.displayName = "onnxruntime"
        # A description of the entire package
        self.description = " ONNX Runtime: cross-platform, high performance ML inferencing and training accelerator "
        # The project's webpage (if you're unsure for a KDE project, just use this one)
        self.webpage = "https://github.com/microsoft/onnxruntime"

        VERSION = "1.22.1"
        for ver in [VERSION]:
            self.targets[ver] = f"https://github.com/microsoft/onnxruntime/releases/download/v{ver}/onnxruntime-win-x64-{ver}.zip"
            self.targetInstSrc[ver] = "onnxruntime-win-x64-" + ver
            self.targetDigests[ver] = ("855276cd4be3cda14fe636c69eb038d75bf5bcd552bda1193a5d79c51f436dfe", CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = VERSION


class Package(BinaryPackageBase):
    # This defines which build system your blueprint should use. In this case, we are
    # using the CMake package base, but there are a lot of options for specific use cases,
    # such as Meson, Perl, QMake, and Binary ones. See
    # https://invent.kde.org/packaging/craft/-/tree/master/bin/Package
    # for details on which package base options are available. For KDE projects, however
    # you will almost certainly be using CMake, and the others are commonly more useful
    # for when you are creating blueprints for new dependencies.
    def __init__(self, **kwargs):
        # Always remember to just initialize the package base like so
        super().__init__(**kwargs)

    def install(self):
        super().install()
        utils.mergeTree(self.sourceDir() / "lib", self.installDir() / "lib")
        utils.mergeTree(self.sourceDir() / "include", self.installDir() / "include")
        return True
