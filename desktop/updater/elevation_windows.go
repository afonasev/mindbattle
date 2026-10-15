package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"strings"
	"syscall"
)

func psQuote(v string) string { return "'" + strings.ReplaceAll(v, "'", "''") + "'" }
func elevatedSwap(p Plan, rollback bool) error {
	exe, err := os.Executable()
	if err != nil {
		return err
	}
	plan := filepath.Join(p.Root, "plan.json")
	raw, err := os.ReadFile(plan)
	if err != nil {
		return err
	}
	var current Plan
	if json.Unmarshal(raw, &current) != nil || !reflect.DeepEqual(current, p) {
		return errors.New("Update plan changed before elevation")
	}
	hash := sha256.Sum256(raw)
	mode := "--files-only=swap"
	if rollback {
		mode = "--files-only=rollback"
	}
	args := syscall.EscapeArg(mode) + " " + syscall.EscapeArg(plan) + " " + syscall.EscapeArg(hex.EncodeToString(hash[:]))
	command := "$ErrorActionPreference='Stop'; $p=Start-Process -FilePath " + psQuote(exe) + " -ArgumentList " + psQuote(args) + " -Verb RunAs -WindowStyle Hidden -Wait -PassThru; exit $p.ExitCode"
	// Only the file worker requests UAC; the broker and game retain the user's token.
	cmd := exec.Command(filepath.Join(os.Getenv("SystemRoot"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe"), "-NoProfile", "-NonInteractive", "-Command", command)
	cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
	if err = cmd.Run(); err != nil {
		return errors.New("Не удалось применить обновление: системное подтверждение отменено или файлы недоступны.")
	}
	return nil
}
