import info

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Compiler.All

    def setTargets( self ):
        self.description = 'The Linux Audio Developers Plugin API'
        self.webpage = 'http://plugin.org.uk/'
        for ver in ['1.15']:
            self.targets[ ver ] = 'http://www.ladspa.org/download/ladspa_sdk_' + ver +'.tgz'
            self.targetInstSrc[ ver ] =  'ladspa_sdk_' + ver + '/src'
            self.patchToApply[ ver ] = ('ladspa-sdk-cmake.patch', 0)
        self.targetDigests['1.15'] = (['4229959b09d20c88c8c86f4aa76427843011705df22d9c28b38359fd1829fded'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.15'

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):

    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
