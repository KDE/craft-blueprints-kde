# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 by Gilles Caulier <caulier dot gilles at gmail dot com>
# Copyright (c) 2019-2020 by Ben Cooksley <bcooksley at kde dot org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# NOTE: see relevant phabricator entry https://phabricator.kde.org/T12071

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = 'https://anongit.kde.org/digikam.git'
        self.defaultTarget = "master"
        self.displayName = "digiKam"
        self.webpage = "https://www.digikam.org"
        self.description = "Professional Photo Management with the Power of Open Source"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        # digiKam mediaPlayer is not yet fully ported to FFMPEG 5 API
        self.runtimeDependencies["libs/ffmpeg"] = "4.4"
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/x265"] = None
        self.runtimeDependencies["libs/tiff"] = None
        # do not force boost deps (see: https://phabricator.kde.org/T12071#212690)
#        self.runtimeDependencies["libs/boost/boost-system"] = "default"
#        self.runtimeDependencies["libs/boost"] = None 
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["libs/lensfun"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/openal-soft"] = None
        self.runtimeDependencies["libs/pthreads"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtimageformats"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/libusb"] = None

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = None         # mingw-based builds need this
            self.runtimeDependencies["libs/qt5/qtwebkit"] = None    # QtWebEngine do not compile with MinGW
        else:
            self.runtimeDependencies["libs/qt5/qtwebengine"] = None

        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies['kde/frameworks/tier3/kio'] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/applications/marble"] = None        # install libmarble, plugins and data for geolocation

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=ON"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

    def createPackage(self):
        self.defines["productname"] = "digiKam"
        self.defines["website"] = "https://www.digikam.org"
        self.defines["company"] = "digiKam.org"
        self.defines["executable"] = "bin\\digikam.exe"                         # Windows-only, mac is handled implicitly
        self.defines["icon"] = os.path.join(self.packageDir(), "digikam.ico")   # Windows-only

        self.defines["shortcuts"] = [{"name" : "digiKam", "target":"bin/digikam.exe", "description" : self.subinfo.description, "icon" : "$INSTDIR\\digikam.ico" },
                                     {"name" : "Showfoto", "target":"bin/showfoto.exe", "description" : "digiKam stand alone Image Editor", "icon" : "$INSTDIR\\showfoto.ico" },
                                     {"name" : "AVPlayer", "target":"bin/avplayer.exe", "description" : "digiKam stand alone Media Player", "icon" : "$INSTDIR\\avplayer.ico" }]     # Windows-only

        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        if CraftCore.compiler.isMSVC():

            # TODO: for MSVC, manage files:

            # see bug #455232
            # - move astro.dll to digiKam/bin/
            # - move marbledeclarative.dll to digiKam/bin/
            # - move marblewidget-qt5.dll to digiKam/bin/
            # - remove marble-qt.exe                        (done - blacklist)

            # - remove setup_vars_opencv4.cmd               (done - blacklist)
            # - remove LICENSE                              (done - blacklist)

            archiveDir = self.archiveDir()
            binPath = os.path.join(archiveDir, "bin")

            utils.moveFile(os.path.join(archiveDir, "astro.dll"),
                           os.path.join(binPath, "astro.dll"))

            utils.moveFile(os.path.join(archiveDir, "marbledeclarative.dll"),
                           os.path.join(binPath, "marbledeclarative.dll"))

            utils.moveFile(os.path.join(archiveDir, "marblewidget-qt5.dll"),
                           os.path.join(binPath, "marblewidget-qt5.dll"))

            # - move bin/digikam to plugins/digikam

            pluginsPath = os.path.join(archiveDir, "plugins")
            utils.createDir(pluginsPath)

            utils.moveFile(os.path.join(archiveDir, "bin", "digikam"),
                           os.path.join(pluginsPath, "digikam"))

            # - move bin/*marble_plugins* to plugins/

            utils.moveFile(os.path.join(archiveDir, "bin", "AnnotatePlugin.dll"),
                           os.path.join(pluginsPath, "AnnotatePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "AprsPlugin.dll"),
                           os.path.join(pluginsPath, "AprsPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "AtmospherePlugin.dll"),
                           os.path.join(pluginsPath, "AtmospherePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "CachePlugin.dll"),
                           os.path.join(pluginsPath, "CachePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "CompassFloatItem.dll"),
                           os.path.join(pluginsPath, "CompassFloatItem.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "CrosshairsPlugin.dll"),
                           os.path.join(pluginsPath, "CrosshairsPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "CycleStreetsPlugin.dll"),
                           os.path.join(pluginsPath, "CycleStreetsPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "EarthquakePlugin.dll"),
                           os.path.join(pluginsPath, "EarthquakePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "EclipsesPlugin.dll"),
                           os.path.join(pluginsPath, "EclipsesPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "ElevationProfileFloatItem.dll"),
                           os.path.join(pluginsPath, "ElevationProfileFloatItem.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "ElevationProfileMarker.dll"),
                           os.path.join(pluginsPath, "ElevationProfileMarker.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "FlightGearPositionProviderPlugin.dll"),
                           os.path.join(pluginsPath, "FlightGearPositionProviderPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "FoursquarePlugin.dll"),
                           os.path.join(pluginsPath, "FoursquarePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GeoUriPlugin.dll"),
                           os.path.join(pluginsPath, "GeoUriPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GosmoreReverseGeocodingPlugin.dll"),
                           os.path.join(pluginsPath, "GosmoreReverseGeocodingPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GosmoreRoutingPlugin.dll"),
                           os.path.join(pluginsPath, "GosmoreRoutingPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GpsbabelPlugin.dll"),
                           os.path.join(pluginsPath, "GpsbabelPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GpsInfo.dll"),
                           os.path.join(pluginsPath, "GpsInfo.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GpxPlugin.dll"),
                           os.path.join(pluginsPath, "GpxPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "GraticulePlugin.dll"),
                           os.path.join(pluginsPath, "GraticulePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "HostipPlugin.dll"),
                           os.path.join(pluginsPath, "HostipPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "JsonPlugin.dll"),
                           os.path.join(pluginsPath, "JsonPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "KmlPlugin.dll"),
                           os.path.join(pluginsPath, "KmlPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "LatLonPlugin.dll"),
                           os.path.join(pluginsPath, "LatLonPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "License.dll"),
                           os.path.join(pluginsPath, "License.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "LocalDatabasePlugin.dll"),
                           os.path.join(pluginsPath, "LocalDatabasePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "LocalOsmSearchPlugin.dll"),
                           os.path.join(pluginsPath, "LocalOsmSearchPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "LocalOsmSearchPlugin.dll"),
                           os.path.join(pluginsPath, "LocalOsmSearchPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "MapQuestPlugin.dll"),
                           os.path.join(pluginsPath, "MapQuestPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "MapScaleFloatItem.dll"),
                           os.path.join(pluginsPath, "MapScaleFloatItem.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "MeasureTool.dll"),
                           os.path.join(pluginsPath, "MeasureTool.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "MonavPlugin.dll"),
                           os.path.join(pluginsPath, "MonavPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "NavigationFloatItem.dll"),
                           os.path.join(pluginsPath, "NavigationFloatItem.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "NominatimReverseGeocodingPlugin.dll"),
                           os.path.join(pluginsPath, "NominatimReverseGeocodingPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "NominatimSearchPlugin.dll"),
                           os.path.join(pluginsPath, "NominatimSearchPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "NotesPlugin.dll"),
                           os.path.join(pluginsPath, "NotesPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "OpenLocationCodeSearchPlugin.dll"),
                           os.path.join(pluginsPath, "OpenLocationCodeSearchPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "OpenRouteServicePlugin.dll"),
                           os.path.join(pluginsPath, "OpenRouteServicePlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "OsmPlugin.dll"),
                           os.path.join(pluginsPath, "OsmPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "OSRMPlugin.dll"),
                           os.path.join(pluginsPath, "OSRMPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "OverviewMap.dll"),
                           os.path.join(pluginsPath, "OverviewMap.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "Pn2Plugin.dll"),
                           os.path.join(pluginsPath, "Pn2Plugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "PntPlugin.dll"),
                           os.path.join(pluginsPath, "PntPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "PositionMarker.dll"),
                           os.path.join(pluginsPath, "PositionMarker.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "PostalCode.dll"),
                           os.path.join(pluginsPath, "PostalCode.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "ProgressFloatItem.dll"),
                           os.path.join(pluginsPath, "ProgressFloatItem.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "RoutingPlugin.dll"),
                           os.path.join(pluginsPath, "RoutingPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "RoutinoPlugin.dll"),
                           os.path.join(pluginsPath, "RoutinoPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "SatellitesPlugin.dll"),
                           os.path.join(pluginsPath, "SatellitesPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "Speedometer.dll"),
                           os.path.join(pluginsPath, "Speedometer.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "StarsPlugin.dll"),
                           os.path.join(pluginsPath, "StarsPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "SunPlugin.dll"),
                           os.path.join(pluginsPath, "SunPlugin.dll"))

            utils.moveFile(os.path.join(archiveDir, "bin", "YoursPlugin.dll"),
                           os.path.join(pluginsPath, "YoursPlugin.dll"))

        return True
