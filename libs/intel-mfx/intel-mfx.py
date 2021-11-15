import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = 'Autotooled version of the opensource Intel media sdk dispatcher'
        for ver in ['1.35']:
            self.targets[ ver ] = f'https://github.com/lu-zero/mfx_dispatch/archive/refs/tags/{ver}.tar.gz'
            self.targetInstSrc[ ver ] =  'mfx_dispatch-' + ver
            self.patchToApply[ ver ] = ('', 0)
        self.targetDigests['1.35'] = (['0790ff82158837124150ab4034db37433a92caac0f145f249d2f194d8ccba3ca'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.35'

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libva"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):

    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
