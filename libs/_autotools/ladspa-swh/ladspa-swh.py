import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = 'The SWH Plugins package for the LADSPA plugin system'
        self.webpage = 'http://plugin.org.uk/'
        self.svnTargets["master"] = "https://github.com/swh/ladspa.git"
        self.defaultTarget = "master"

    def setDependencies( self ):
        self.runtimeDependencies["libs/libfftw"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )

