# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.0"]:
            self.targets[ver] = f"https://github.com/CJCombrink/SpellChecker-Plugin/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qtc-SpellChecker-Plugin-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"SpellChecker-Plugin-{ver}"
        self.targetDigests["1.3.0"] = (['338737c378d3de22da6c257dfb55dc8917286de684b640c8e4cb22913e698093'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.3.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/hunspell"] = None
        self.runtimeDependencies["qt-apps/qtcreator/qtcreator"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


    def configure(self, configureDefines=""):
        qtc = CraftPackageObject.get("qtcreator").instance
        with open(os.path.join(self.sourceDir(), "spellchecker_local_paths.pri"), "wt") as f:
            f.write(f"LOCAL_QTCREATOR_SOURCES={qtc.sourceDir()}\n")
            f.write(f"LOCAL_IDE_BUILD_TREE={qtc.buildDir()}\n")
            f.write(f"LOCAL_HUNSPELL_LIB_DIR={os.path.join(CraftCore.standardDirs.craftRoot(),'lib')}\n")
            f.write(f"LOCAL_HUNSPELL_SRC_DIR={os.path.join(CraftCore.standardDirs.craftRoot(),'include')}\n")
        return super().configure()