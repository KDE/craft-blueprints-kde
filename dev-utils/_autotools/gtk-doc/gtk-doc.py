# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


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
            majorMinorStr = ".".join(ver.split(".")[0:2])
            self.targets[ver] = f"https://download.gnome.org/sources/gtk-doc/{majorMinorStr}/gtk-doc-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"gtk-doc-{ver}"
        self.targetDigests["1.33.2"] = (["cc1b709a20eb030a278a1f9842a362e00402b7f834ae1df4c1998a723152bf43"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.33.2"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Dyelp_manual=false"]
