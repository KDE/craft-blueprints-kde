import info

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets( self ):
        self.description = 'The Linux Audio Developers Plugin API'
        self.webpage = 'http://plugin.org.uk/'
        for ver in ['1.17']:
            self.targets[ ver ] = 'http://www.ladspa.org/download/ladspa_sdk_' + ver +'.tgz'
            self.targetInstSrc[ ver ] =  'ladspa_sdk_' + ver + '/src'
            self.patchToApply[ ver ] = ('ladspa-sdk-cmake.patch', 0)
        self.targetDigests['1.17'] = (['d9d596171d93f9c226fcdb7e27c6f917422ac487efe2c05e0a18094df4268061'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.17'

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):

    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
