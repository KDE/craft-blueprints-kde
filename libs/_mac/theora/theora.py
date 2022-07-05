# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.1.1']:
            self.targets[ver] = 'https://downloads.xiph.org/releases/theora/libtheora-' + ver + '.tar.bz2'
            self.archiveNames[ver] = "libtheora-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'libtheora-' + ver
        self.description = 'Open video compression format'
        self.defaultTarget = '1.1.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
       	self.subinfo.options.configure.bootstrap = True
       	self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += " --disable-dependency-tracking" \
        " --prefix=" + prefix + \
        " --disable-oggtest" + \
        " --disable-vorbistest" + \
        " --disable-examples"







