package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func swapFixture(t *testing.T) (Plan, Manifest) {
	t.Helper()
	root, err := filepath.EvalSymlinks(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}
	user := filepath.Join(root, "profile")
	tx := filepath.Join(user, "shell", "transactions", strings.Repeat("a", 64))
	candidate := filepath.Join(tx, "candidate")
	target := filepath.Join(root, "Mindbattle.app")
	p := Plan{Target: target, Candidate: candidate, Backup: target + ".backup-" + strings.Repeat("a", 64), Root: tx, Manifest: filepath.Join(tx, "release.json"), Journal: filepath.Join(tx, "journal.json"), ACK: filepath.Join(tx, "ready"), Started: filepath.Join(tx, "started"), Token: strings.Repeat("a", 64), Parent: 1, UserData: user, Timeout: 5}
	identityBytes, _ := json.Marshal(map[string]string{"product": product, "pin": pinnedKey})
	files := map[string][]byte{"Contents/Resources/mindbattle-installation.json": identityBytes, "Contents/MacOS/Mindbattle": []byte("new version"), "Contents/Resources/mindbattle-layout.json": []byte(`{"paths":["Contents/MacOS/Mindbattle","Contents/Resources/mindbattle-installation.json"]}`)}
	m := Manifest{Platform: "darwin-universal"}
	for name, data := range files {
		for _, dir := range []string{candidate, target} {
			file := filepath.Join(dir, filepath.FromSlash(name))
			if err = os.MkdirAll(filepath.Dir(file), 0755); err != nil {
				t.Fatal(err)
			}
			content := data
			if dir == target && name == "Contents/MacOS/Mindbattle" {
				content = []byte("old version")
			}
			if err = os.WriteFile(file, content, 0644); err != nil {
				t.Fatal(err)
			}
		}
		hash := sha256.Sum256(data)
		m.Files = append(m.Files, File{Path: name, Size: int64(len(data)), SHA256: hex.EncodeToString(hash[:]), Mode: 0644})
	}
	if err = os.WriteFile(filepath.Join(candidate, "untrusted.exe"), []byte("unsigned"), 0644); err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(target, "installer-owned.txt"), []byte("preserved"), 0644); err != nil {
		t.Fatal(err)
	}
	return p, m
}
func TestSwapCopiesVerifiedPayloadPreservesInstalledExtrasAndRollsBack(t *testing.T) {
	p, m := swapFixture(t)
	if err := swapFiles(p, m, false); err != nil {
		t.Fatal(err)
	}
	content, _ := os.ReadFile(filepath.Join(p.Target, "Contents/MacOS/Mindbattle"))
	if string(content) != "new version" {
		t.Fatal("new version missing")
	}
	if _, err := os.Stat(filepath.Join(p.Target, "untrusted.exe")); !os.IsNotExist(err) {
		t.Fatal("unsigned candidate extras copied")
	}
	if content, err := os.ReadFile(filepath.Join(p.Target, "installer-owned.txt")); err != nil || string(content) != "preserved" {
		t.Fatal("installed extra lost")
	}
	if err := swapFiles(p, m, true); err != nil {
		t.Fatal(err)
	}
	content, _ = os.ReadFile(filepath.Join(p.Target, "Contents/MacOS/Mindbattle"))
	if string(content) != "old version" {
		t.Fatal("last good not restored")
	}
}
func TestCorruptCandidateDoesNotChangeWorkingInstallation(t *testing.T) {
	p, m := swapFixture(t)
	if err := os.WriteFile(filepath.Join(p.Candidate, "Contents/MacOS/Mindbattle"), []byte("corrupt"), 0644); err != nil {
		t.Fatal(err)
	}
	if err := swapFiles(p, m, false); err == nil {
		t.Fatal("corrupt candidate accepted")
	}
	content, _ := os.ReadFile(filepath.Join(p.Target, "Contents/MacOS/Mindbattle"))
	if string(content) != "old version" {
		t.Fatal("old version damaged")
	}
}
