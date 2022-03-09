import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = 'The SWH Plugins package for the LADSPA plugin system'
        self.webpage = 'http://plugin.org.uk/'
        #self.targets["0.4.17"] = "https://github.com/swh/ladspa/archive/v0.4.17.tar.gz"
        #self.targetInstSrc['0.4.17'] = 'ladspa-0.4.17'
        #self.targetDigests['0.4.17'] = (['d1b090feec4c5e8f9605334b47faaad72db7cc18fe91d792b9161a9e3b821ce7'], CraftHash.HashAlgorithm.SHA256)
        self.svnTargets["master"] = "https://github.com/swh/ladspa.git"
        self.defaultTarget = "master"

    def setDependencies( self ):
        self.runtimeDependencies["libs/libfftwf"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        #self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        #self.buildDependencies["perl-modules/list-moreutils"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.useShadowBuild = False
        #self.subinfo.options.make.args += f"PERL5LIB={self.shell.toNativePath(CraftCore.standardDirs.craftRoot())}/site/lib"
