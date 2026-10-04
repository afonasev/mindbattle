!include MUI2.nsh
!include nsDialogs.nsh

!ifndef BUILD_UNINSTALLER

Var MindbattleShortcutCheckbox
Var MindbattleShortcutState

!macro customInit
  StrCpy $MindbattleShortcutState ${BST_CHECKED}
!macroend

!macro customPageAfterChangeDir
  Page custom MindbattleOptionsCreate MindbattleOptionsLeave

Function MindbattleOptionsCreate
  ; Updates retain the existing shortcut behavior and do not add another prompt.
  ${If} ${isUpdated}
    Abort
  ${EndIf}
  ${If} $LANGUAGE == 1049
    !insertmacro MUI_HEADER_TEXT "Дополнительные параметры" "Выберите способ быстрого доступа к Mindbattle."
  ${Else}
    !insertmacro MUI_HEADER_TEXT "Additional options" "Choose how to access Mindbattle."
  ${EndIf}
  nsDialogs::Create 1018
  Pop $0
  ${If} $0 == error
    Abort
  ${EndIf}
  ${If} $LANGUAGE == 1049
    ${NSD_CreateCheckbox} 0 0 100% 20u "Создать ярлык на рабочем столе"
  ${Else}
    ${NSD_CreateCheckbox} 0 0 100% 20u "Create a desktop shortcut"
  ${EndIf}
  Pop $MindbattleShortcutCheckbox
  ${NSD_SetState} $MindbattleShortcutCheckbox $MindbattleShortcutState
  nsDialogs::Show
FunctionEnd

Function MindbattleOptionsLeave
  ${NSD_GetState} $MindbattleShortcutCheckbox $MindbattleShortcutState
FunctionEnd
!macroend

!macro customInstall
  ; Use the builder's shortcut creation/uninstallation logic, then honor opt-out.
  ${If} $MindbattleShortcutState == ${BST_UNCHECKED}
    WinShell::UninstShortcut "$newDesktopLink"
    Delete "$newDesktopLink"
  ${EndIf}
!macroend

!endif
