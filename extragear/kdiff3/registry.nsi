    !define DIFF_EXT_CLSID "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
    !define DIFF_EXT_ID "Diff-ext for KDiff3"
    !define DIFF_EXT_DLL "kdiff3ext.dll"
    
    SetRegView 64
    ;remove old diff-ext settings
    DeleteRegKey HKCU  "Software\KDiff3"

    WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}" "" "${DIFF_EXT_ID}"
    WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "" "$INSTDIR\bin\${DIFF_EXT_DLL}"
    WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "ThreadingModel" "Apartment"
    WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
    WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}" "${DIFF_EXT_ID}"
    WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
    WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"

    SetRegView 32

    ;remove old diff-ext settings
    DeleteRegKey HKCU  "Software\KDiff3"
    ;Maybe left behind due to a bug in previous installers.
    DeleteRegKey SHCTX  "Software\KDE\KDiff3"
    DeleteRegKey /ifempty SHCTX  "Software\KDE\"
    
    WriteRegStr HKCU  "${regkey}\diff-ext" "" ""
    WriteRegStr HKCU "${regkey}\diff-ext" "InstallDir" "$INSTDIR\bin"
    WriteRegStr HKCU "${regkey}\diff-ext" "diffcommand" "$INSTDIR\bin\kdiff3.exe"
