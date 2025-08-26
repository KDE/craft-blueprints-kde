# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API."
        self.defaultTarget = "master"

        # lxml 6.0.1 does not seem to support libxml2 newer than 2.13.8 as it seems
        # Upstream release notes (https://github.com/lxml/lxml/releases/tag/lxml-6.0.1) say:
        # * Binary wheels use the library version libxml2 2.14.5.
        # * Windows binary wheels continue to use a security patched library version libxml2 2.11.9.
        # So we just use the binary wheels as we don't want to ship an old libxml2 just because of lxml
        self.allowPrebuildBinaries = CraftCore.compiler.isMSVC()

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        if not self.allowPrebuildBinaries:
            self.runtimeDependencies["libs/libxml2"] = None
            self.runtimeDependencies["libs/libxslt"] = None
            self.runtimeDependencies["python-modules/cython"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "--config-settings=--global-option=build_ext",
            f"--config-settings=--global-option=--include-dirs={CraftCore.standardDirs.craftRoot()}/include/libxml2",
        ]
