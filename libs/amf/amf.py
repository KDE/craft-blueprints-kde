import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AMD library for accelerated H.264 and HEVC(only windows) encoding on hardware with Video Coding Engine (VCE)"
        for ver in ['1.4.29']:
            self.targets[ ver ] = f"https://github.com/GPUOpen-LibrariesAndSDKs/AMF/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] =  'AMF-' + ver
        self.targetDigests['1.4.29'] = (['be42e4acd973fc7a228f087313bee9eaca08df031ec4596f14fb2eabef528628'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.4.29'

from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase ):
    
    def install(self):
        utils.createDir(self.installDir()/"include/AMF")
        return utils.copyDir(self.sourceDir()/"amf/public/include", self.installDir()/"include/AMF")