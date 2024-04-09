# -*- coding: utf-8 -*-
import re

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Lightweight speech recognition engine."
        self.webpage = "https://cmusphinx.sourceforge.net/"
        self.displayName = "PocketSphinx"
        self.patchToApply["e40da77a85edbb5d79b92bf1dcb927d94e43e07d"] = [
            ("0001-fix-static-lapack-link.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/sphinxbase"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static", "--without-python"]

    def configure(self):
        if not super().configure():
            return False
        fileName = self.buildDir() / "Makefile"
        with open(fileName, "rt") as f:
            content = f.read()
        with open(fileName, "wt") as f:
            f.write(re.compile("(SUBDIRS\\s*=.*)\\bdoc\\b").sub("\\1", content))
        return True
