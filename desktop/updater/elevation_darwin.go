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
	"strconv"
	"strings"
)

func shellQuote(v string) string { return "'" + strings.ReplaceAll(v, "'", "'\\''") + "'" }
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
		return errors.New("Update plan changed before authorization")
	}
	hash := sha256.Sum256(raw)
	mode := "--files-only=swap"
	if rollback {
		mode = "--files-only=rollback"
	}
	command := shellQuote(exe) + " " + shellQuote(mode) + " " + shellQuote(plan) + " " + shellQuote(hex.EncodeToString(hash[:]))
	// Authorization is confined to the signed file transaction. The broker launches
	// the game itself afterwards, using the original ordinary-user process token.
	script := "do shell script " + strconv.Quote(command) + " with administrator privileges"
	if err = exec.Command("/usr/bin/osascript", "-e", script).Run(); err != nil {
		return errors.New("Не удалось применить обновление: системное подтверждение отменено или файлы недоступны.")
	}
	return nil
}
