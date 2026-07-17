# SPDX-FileCopyrightText: 2026 Melvin Keskin <melvo@olomono.de>
#
# SPDX-License-Identifier: CC0-1.0

import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://gitlab.freedesktop.org/gstreamer/gstreamer.git"
        for ver in ["1.28.4"]:
            self.targets[ver] = f"https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"gstreamer-{ver}"
        self.targetDigests["1.28.4"] = (["f5adc7e8f448c10260b3b25aa101c9d540674c8d9a54c2b77a86d04f2b3b50dd"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.28.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["libs/glib"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Dexamples=disabled",
            f"-Dtests={self.subinfo.options.dynamic.buildTests.asEnabledDisabled}",
        ]
        self.subinfo.options.configure.ldflags += " -lintl"

    def postInstall(self):
        if not super().postInstall():
            return False
        if CraftCore.compiler.isMacOS:
            # GStreamer installs its plugins to lib/gstreamer-1.0. When the app is bundled,
            # craft moves the whole lib/ directory into the .app's Contents/Frameworks, where
            # codesign --deep rejects the plain plugin directory ("bundle format unrecognized,
            # invalid, or unsuitable"). Move the plugins to plugins/ so they end up in
            # Contents/PlugIns/gstreamer-1.0 instead (like Qt's plugins, which sign fine).
            # Consumers must point GST_PLUGIN_SYSTEM_PATH at that directory at runtime.
            plugins = self.imageDir() / "lib/gstreamer-1.0"
            if plugins.is_dir():
                if not utils.mergeTree(plugins, self.imageDir() / "plugins/gstreamer-1.0"):
                    return False
        return True
