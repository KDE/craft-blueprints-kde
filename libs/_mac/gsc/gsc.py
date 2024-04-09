# -*- coding: utf-8 -*-
import os

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2"]:
            # self.targets[ver] = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?bincats/GSC_' + ver
            self.targets[ver] = "http://www.indilib.org/jdownloads/kstars/gsc-1.2.tar.gz"
            self.archiveNames[ver] = "gsc-%s.tar.gz" % ver
            # self.targetInstSrc[ver] = 'gsc-' + ver
        self.description = "The Guide Star Catalog I"
        self.defaultTarget = "1.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None


from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False

    def configure(self):
        sourcedir = str(self.sourceDir())
        utils.rmtree(os.path.join(sourcedir, "bin-dos"))
        return True

    def make(self):
        sourcedir = str(self.sourceDir())
        sourcesrc = os.path.join(sourcedir, "src")
        os.chdir(sourcesrc)

        f1name = sourcedir + "/src/Makefile"

        f1 = open(f1name, "r")
        filedata = f1.read()
        f1.close()

        filedata = filedata.replace("CC    = cc -I. -O", "CC    = cc -I. -O " + "-Wno-implicit-function-declaration")

        f1 = open(f1name, "w")
        f1.write(filedata)
        f1.close()

        utils.system(" ".join([self.makeProgram, str(self.makeOptions(self.subinfo.options.make.args))]))
        utils.copyFile(os.path.join(sourcesrc, "gsc.exe"), os.path.join(sourcesrc, "gsc"))
        utils.copyFile(os.path.join(sourcesrc, "decode.exe"), os.path.join(sourcesrc, "decode"))

        utils.copyFile(os.path.join(sourcesrc, "gsc.exe"), os.path.join(sourcedir, "bin"))
        utils.copyFile(os.path.join(sourcesrc, "gsc"), os.path.join(sourcedir, "bin"))

        utils.copyFile(os.path.join(sourcesrc, "decode.exe"), os.path.join(sourcedir, "bin"))
        utils.copyFile(os.path.join(sourcesrc, "decode"), os.path.join(sourcedir, "bin"))

        return True

    def install(self):
        sourcedir = str(self.sourceDir())
        sourcesrc = os.path.join(sourcedir, "src")
        craftbindir = os.path.join(CraftCore.standardDirs.craftRoot(), "bin")
        gscdir = os.path.join(self.imageDir(), "gsc")

        self.enterSourceDir()
        utils.copyDir(sourcedir, gscdir)
        utils.rmtree(os.path.join(gscdir, "src"))

        utils.copyFile(os.path.join(os.path.join(gscdir, "bin"), "gsc"), craftbindir)

        return True
