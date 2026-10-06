!include MUI2.nsh

!ifndef BUILD_UNINSTALLER
LangString MindbattleShortcutText 1033 "Create a desktop shortcut"
LangString MindbattleShortcutText 1049 "Создать ярлык на рабочем столе"
LangString MindbattleShortcutError 1033 "Could not create the desktop shortcut. Please run the installer again."
LangString MindbattleShortcutError 1049 "Не удалось создать ярлык. Запустите установщик ещё раз."

!macro customFinishPage
Function MindbattleCreateShortcut
  ; All-users installation: the Public Desktop is visible to every user.
  SetShellVarContext all
  ClearErrors
  CreateShortCut "$DESKTOP\${SHORTCUT_NAME}.lnk" "$INSTDIR\${PRODUCT_FILENAME}.exe" "" "$INSTDIR\${PRODUCT_FILENAME}.exe" 0 "" "" "${APP_DESCRIPTION}"
  ${If} ${Errors}
    MessageBox MB_OK|MB_ICONEXCLAMATION "$(MindbattleShortcutError)"
    Return
  ${EndIf}
  WinShell::SetLnkAUMI "$DESKTOP\${SHORTCUT_NAME}.lnk" "${APP_ID}"
  System::Call 'Shell32::SHChangeNotify(i 0x8000000, i 0, i 0, i 0)'
FunctionEnd

  Function MindbattleStartApp
    ${If} ${isUpdated}
      StrCpy $1 "--updated"
    ${Else}
      StrCpy $1 ""
    ${EndIf}
    ${StdUtils.ExecShellAsUser} $0 "$launchLink" "open" "$1"
  FunctionEnd
  !define MUI_FINISHPAGE_RUN
  !define MUI_FINISHPAGE_RUN_FUNCTION MindbattleStartApp
  ; MUI's second native finish checkbox calls our action instead of opening a README.
  !define MUI_FINISHPAGE_SHOWREADME ""
  !define MUI_FINISHPAGE_SHOWREADME_TEXT "$(MindbattleShortcutText)"
  !define MUI_FINISHPAGE_SHOWREADME_FUNCTION MindbattleCreateShortcut
  !insertmacro MUI_PAGE_FINISH
!macroend

!macro customInstall
  ; Silent installations have no finish page. Honor /no-desktop-shortcut there.
  IfSilent 0 mindbattleInteractive
    ${IfNot} ${isNoDesktopShortcut}
      Call MindbattleCreateShortcut
    ${EndIf}
  mindbattleInteractive:
!macroend
!endif

!macro customUnInstall
  SetShellVarContext all
  WinShell::UninstShortcut "$DESKTOP\${SHORTCUT_NAME}.lnk"
  Delete "$DESKTOP\${SHORTCUT_NAME}.lnk"
!macroend
