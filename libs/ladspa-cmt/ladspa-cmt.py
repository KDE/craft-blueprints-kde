import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = 'The Computer Music Toolkit LADSPA plugin collection'
        self.webpage = 'http://ladspa.org/'
        for ver in ['1.17']:
            self.targets[ ver ] = 'http://www.ladspa.org/download/cmt_' + ver +'.tgz'
            self.targetInstSrc[ ver ] =  'cmt_' + ver + '/src'
            self.patchToApply[ ver ] = ('ladspa-cmt-cmake.patch', 0)
        self.targetDigests['1.17'] = (['eb56d7abebfdf8a6d0ad65d012238c9fc394dd41eeca11900812a8cb6b07ad1f'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.17'

    def setDependencies( self ):
        self.buildDependencies["libs/ladspa-sdk"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
