# -*- coding: utf-8 -*-
import info
from Package.MesonPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # needs cp
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotWindows

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["python-modules/lxml"] = None
        self.buildDependencies["python-modules/pygments"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["data/docbook-xsl"] = None
        self.runtimeDependencies["data/docbook-dtd"] = None
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "GTK-Doc is used to document C code. It is typically used to document the public API of libraries, such as the GTK+ and GNOME libraries, but it can also be used to document application code."
        self.svnTargets["master"] = "https://gitlab.gnome.org/GNOME/gtk-doc.git"
        for ver in ["1.33.2"]:
            self.targets[ver] = f"https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/{ver}/gtk-doc-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gtk-doc-{ver}"
        self.targetDigests["1.33.2"] = (["2d1b0cbd26edfcb54694b2339106a02a81d630a7dedc357461aeb186874cc7c0"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.33.2"


class Package(MesonPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-Dyelp_manual=false"]
