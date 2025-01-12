# -*- coding: utf-8 -*-
import re

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Common library for sphinx speech recognition."
        self.webpage = "http://cmusphinx.sourceforge.net/"
        self.displayName = "SphinxBase"
        self.patchToApply["057d423ddddea2351678abd0d29b5f1463a343c7"] = [
            ("0001-fix-static-lapack-link.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/lapack"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--without-python"]

    def configure(self):
        if not super().configure():
            return False
        fileName = self.buildDir() / "Makefile"
        with open(fileName, "rt") as f:
            content = f.read()
        with open(fileName, "wt") as f:
            f.write(re.compile("(SUBDIRS\\s*=.*)\\bdoc\\b").sub("\\1", content))
        return True
