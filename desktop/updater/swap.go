package main

import (
	"encoding/json"
	"errors"
	"io"
	"io/fs"
	"os"
	"path/filepath"
)

// The broker remains unelevated. A privileged worker only copies verified files
// and swaps the installation; it never starts the game or writes player data.
func replaceInstallation(p Plan, m Manifest, rollback bool) error {
	if err := swapFiles(p, m, rollback); err != nil {
		if errors.Is(err, fs.ErrPermission) {
			return elevatedSwap(p, rollback)
		}
		return err
	}
	return nil
}
func copyRegular(from, to string, mode fs.FileMode) error {
	info, err := os.Lstat(from)
	if err != nil {
		return err
	}
	if !info.Mode().IsRegular() {
		return errors.New("nonregular update source")
	}
	if err = os.MkdirAll(filepath.Dir(to), 0755); err != nil {
		return err
	}
	in, err := os.Open(from)
	if err != nil {
		return err
	}
	defer in.Close()
	out, err := os.OpenFile(to, os.O_CREATE|os.O_EXCL|os.O_WRONLY, mode)
	if err != nil {
		return err
	}
	_, err = io.Copy(out, in)
	if err == nil {
		err = out.Sync()
	}
	closeErr := out.Close()
	if err != nil {
		return err
	}
	return closeErr
}
func swapFiles(p Plan, m Manifest, rollback bool) error {
	if err := validatePlan(p); err != nil {
		return err
	}
	if rollback {
		if err := identity(p.Backup); err != nil {
			return err
		}
		if err := identity(p.Target); err != nil {
			return err
		}
		failed := p.Target + ".failed-" + p.Token
		if _, err := os.Lstat(failed); !os.IsNotExist(err) {
			return errors.New("failed installation path occupied")
		}
		if err := os.Rename(p.Target, failed); err != nil {
			return err
		}
		if err := os.Rename(p.Backup, p.Target); err != nil {
			_ = os.Rename(failed, p.Target)
			return err
		}
		return nil
	}
	if err := identity(p.Target); err != nil {
		return err
	}
	if err := identity(p.Candidate); err != nil {
		return err
	}
	if err := verifyTree(p.Candidate, m); err != nil {
		return err
	}
	incoming := p.Target + ".incoming-" + p.Token
	if err := os.Mkdir(incoming, 0700); err != nil {
		return err
	}
	installed := false
	defer func() {
		if !installed {
			_ = os.RemoveAll(incoming)
		}
	}()
	next := map[string]bool{}
	for _, f := range m.Files {
		next[f.Path] = true
		if err := copyRegular(filepath.Join(p.Candidate, filepath.FromSlash(f.Path)), filepath.Join(incoming, filepath.FromSlash(f.Path)), fs.FileMode(f.Mode)); err != nil {
			return err
		}
	}
	for _, l := range m.Links {
		next[l.Path] = true
		to := filepath.Join(incoming, filepath.FromSlash(l.Path))
		if err := os.MkdirAll(filepath.Dir(to), 0755); err != nil {
			return err
		}
		if err := os.Symlink(l.Target, to); err != nil {
			return err
		}
	}
	// Preserve installer-owned extras from the actual old installation only.
	// Never trust unsigned extra files in the user-writable candidate directory.
	resources := "resources"
	if m.Platform == "darwin-universal" {
		resources = "Contents/Resources"
	}
	layoutPath := filepath.Join(p.Target, filepath.FromSlash(resources+"/mindbattle-layout.json"))
	raw, err := os.ReadFile(layoutPath)
	if err != nil {
		return err
	}
	var layout struct {
		Paths []string `json:"paths"`
	}
	if err = json.Unmarshal(raw, &layout); err != nil {
		return err
	}
	owned := map[string]bool{resources + "/mindbattle-layout.json": true}
	for _, name := range layout.Paths {
		owned[name] = true
	}
	err = filepath.WalkDir(p.Target, func(name string, d fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if d.IsDir() {
			return nil
		}
		rel, e := filepath.Rel(p.Target, name)
		if e != nil {
			return e
		}
		rel = filepath.ToSlash(rel)
		if owned[rel] || next[rel] {
			return nil
		}
		if !safePath(rel) || d.Type()&os.ModeSymlink != 0 {
			return errors.New("unsupported installation extra")
		}
		info, e := d.Info()
		if e != nil {
			return e
		}
		return copyRegular(name, filepath.Join(incoming, filepath.FromSlash(rel)), info.Mode().Perm())
	})
	if err != nil {
		return err
	}
	if err = identity(incoming); err != nil {
		return err
	}
	if err = verifyTree(incoming, m); err != nil {
		return err
	}
	if _, err = os.Lstat(p.Backup); !os.IsNotExist(err) {
		return errors.New("backup path occupied")
	}
	if err = os.Rename(p.Target, p.Backup); err != nil {
		return err
	}
	if err = os.Rename(incoming, p.Target); err != nil {
		_ = os.Rename(p.Backup, p.Target)
		return err
	}
	installed = true
	return nil
}
