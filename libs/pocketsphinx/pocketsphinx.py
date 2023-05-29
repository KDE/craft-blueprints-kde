# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Lightweight speech recognition engine."
        self.webpage = "http://cmusphinx.sourceforge.net/"
        self.displayName = "PocketSphinx"
        self.patchToApply['e40da77a85edbb5d79b92bf1dcb927d94e43e07d'] = [
            ("0001-fix-static-lapack-link.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/sphinxbase"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-shared --disable-static --without-python"

    def configure(self):
        if not super().configure():
            return False
        fileName = os.path.join(self.buildDir(), "Makefile")
        with open(fileName, "rt") as f:
            content = f.read()
        with open(fileName, "wt") as f:
            f.write(re.compile('(SUBDIRS\\s*=.*)\\bdoc\\b').sub('\\1', content))
        return True
