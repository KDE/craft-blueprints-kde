Section "Context Menu Extention" SectionShellPlugin
    
SectionEnd


Section -InstallShellExtention
    !define DIFF_EXT_CLSID "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
    !define DIFF_EXT_ID "Diff-ext for KDiff3"
    !define DIFF_EXT_DLL "kdiff3ext.dll"
    
    SetRegView 64
    
    SectionGetFlags ${SectionShellPlugin} $R0
    IntOp $R0 $R0 & ${SF_SELECTED}

    ${If} $R0 == ${SF_SELECTED}
        MessageBox MB_OK "ShellExt"

        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}" "" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "" "$INSTDIR\bin\${DIFF_EXT_DLL}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "ThreadingModel" "Apartment"
        WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
    ${EndIf}
    SetRegView 32
    
    WriteRegStr HKCU "${regkey}\diff-ext" "" ""
    WriteRegStr HKCU "${regkey}\diff-ext" "InstallDir" "$INSTDIR\bin"
    WriteRegStr HKCU "${regkey}\diff-ext" "diffcommand" "$INSTDIR\bin\kdiff3.exe"
SectionEnd