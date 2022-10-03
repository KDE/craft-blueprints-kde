import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AMD library for accelerated H.264 and HEVC(only windows) encoding on hardware with Video Coding Engine (VCE)"
        for ver in ['1.4.23']:
            self.targets[ ver ] = f"https://github.com/GPUOpen-LibrariesAndSDKs/AMF/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] =  'AMF-' + ver
        self.targetDigests['1.4.23'] = (['7c8a5c91bca54e257258e4efcc61925921f2efe432efd34cf77dd9dc1803c38a'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.4.23'

from Package.SourceOnlyPackageBase  import *

class Package(SourceOnlyPackageBase ):
    
    def install(self):
        utils.createDir(self.installDir()/"include/AMF")
        return utils.copyDir(self.sourceDir()/"amf/public/include", self.installDir()/"include/AMF")