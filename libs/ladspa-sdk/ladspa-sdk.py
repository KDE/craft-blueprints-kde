import info

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets( self ):
        self.description = 'The Linux Audio Developers Plugin API'
        self.webpage = 'http://plugin.org.uk/'
        for ver in ['1.16']:
            self.targets[ ver ] = 'http://www.ladspa.org/download/ladspa_sdk_' + ver +'.tgz'
            self.targetInstSrc[ ver ] =  'ladspa_sdk_' + ver + '/src'
            self.patchToApply[ ver ] = ('ladspa-sdk-cmake.patch', 0)
        self.targetDigests['1.16'] = (['511b237dca0f6c7b993f6be0954215c8f859d6f2a20686b25d082458d763e38b'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.16'

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):

    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
