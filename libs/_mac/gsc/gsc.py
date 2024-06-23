# -*- coding: utf-8 -*-

# Notes - This recipe is for building the GSC executable and its associated data files for use with the CCD Simulator in INDI.
# This also allows KStars to have stars when using the CCD Simulator for various testing purposes and to give users practice with the software.
# On MacOS, we do not bundle the GSC data files in the KStars App, because it increases the size by 200 MB and not all users want to use the simulator.
# So there is a function in KStars that allows Mac users to download and install the GSC data files in their KStars data directory.
# But, on MacOS, for proper distribution of KStars with code signing etc, the GSC executable needs to be copied into the App bundle.
# Since we do not want to take extra time and resources just to produce this small file, the file is stored with several similar files
# in the KStars-Mac-Files GitHub repository - https://github.com/rlancaste/kstars-mac-files and the KStars recipe automatically includes that file.
# The GSC data directory produced by this recipe is stored on indilib at http://www.indilib.org/jdownloads/Mac/gsc.zip.
# If there are any changes to GSC, this recipe should be run and the resulting executable and data directory should be uploaded to their locations online.
# While this recipe is needed by KStars and INDI on MacOS, it is not a direct dependency of KStars because the results of running this recipe are stored online.

import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3"]:
            self.targets[ver] = "http://www.indilib.org/jdownloads/kstars/gsc-1.3.tar.gz"
            self.archiveNames[ver] = "gsc-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "gsc"
        self.description = "The Hubble Guide Star Catalog I version 1.3.  This provides stars for the CCD Simulator in INDI."
        self.defaultTarget = "1.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)