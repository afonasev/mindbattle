package main

import (
	"crypto/ed25519"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"time"
)

var pinnedKey string

const product = "tech.afonasev.mindbattle"

type File struct {
	Path   string `json:"path"`
	SHA256 string `json:"sha256"`
	Size   int64  `json:"size"`
	Mode   int    `json:"mode"`
}
type Link struct {
	Path   string `json:"path"`
	Target string `json:"target"`
}
type Manifest struct {
	Format   int    `json:"format"`
	Product  string `json:"product"`
	Sequence int64  `json:"sequence"`
	Version  string `json:"version"`
	Platform string `json:"platform"`
	Helper   int    `json:"helper"`
	Entry    string `json:"entry"`
	Files    []File `json:"files"`
	Links    []Link `json:"links"`
}
type Envelope struct {
	Payload   string `json:"payload"`
	Signature string `json:"signature"`
}
type Plan struct {
	Target    string `json:"target"`
	Candidate string `json:"candidate"`
	Backup    string `json:"backup"`
	Root      string `json:"root"`
	Manifest  string `json:"manifest"`
	Journal   string `json:"journal"`
	ACK       string `json:"ack"`
	Started   string `json:"started"`
	Token     string `json:"token"`
	Parent    int    `json:"parent"`
	UserData  string `json:"userData"`
	Timeout   int    `json:"timeout"`
}
type Journal struct {
	Phase   string `json:"phase"`
	Version string `json:"version"`
	Target  string `json:"target"`
	Backup  string `json:"backup"`
	Error   string `json:"error,omitempty"`
}

func atomicJSON(name string, v any) error {
	b, e := json.Marshal(v)
	if e != nil {
		return e
	}
	f, e := os.OpenFile(name+".tmp", os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0600)
	if e != nil {
		return e
	}
	if _, e = f.Write(b); e == nil {
		e = f.Sync()
	}
	ce := f.Close()
	if e == nil {
		e = ce
	}
	if e != nil {
		return e
	}
	if e = os.Rename(name+".tmp", name); e != nil {
		return e
	}
	if d, e := os.Open(filepath.Dir(name)); e == nil {
		_ = d.Sync()
		_ = d.Close()
	}
	return nil
}
func safePath(v string) bool {
	if v == "" || strings.ContainsAny(v, "\\:\x00\r\n\t") || strings.HasPrefix(v, "/") {
		return false
	}
	for _, s := range strings.Split(v, "/") {
		if s == "" || s == "." || s == ".." || strings.HasSuffix(s, ".") || strings.HasSuffix(s, " ") {
			return false
		}
	}
	return true
}
func within(root, name string) bool {
	rel, e := filepath.Rel(root, name)
	return e == nil && rel != ".." && !strings.HasPrefix(rel, ".."+string(filepath.Separator)) && !filepath.IsAbs(rel)
}
func verifyManifest(raw []byte) (Manifest, error) {
	var env Envelope
	var m Manifest
	if len(raw) > 8*1024*1024 {
		return m, errors.New("manifest too large")
	}
	if e := json.Unmarshal(raw, &env); e != nil {
		return m, e
	}
	der, e := base64.StdEncoding.DecodeString(pinnedKey)
	if e != nil {
		return m, e
	}
	pk, e := x509.ParsePKIXPublicKey(der)
	if e != nil {
		return m, e
	}
	key, ok := pk.(ed25519.PublicKey)
	if !ok {
		return m, errors.New("invalid pin")
	}
	sig, e := base64.StdEncoding.DecodeString(env.Signature)
	if e != nil || !ed25519.Verify(key, []byte(env.Payload), sig) {
		return m, errors.New("invalid shell signature")
	}
	if e = json.Unmarshal([]byte(env.Payload), &m); e != nil {
		return m, e
	}
	expected := "darwin-universal"
	if runtime.GOOS == "windows" {
		expected = "win32-x64"
	}
	if !regexp.MustCompile(`^\d+\.\d+\.\d+$`).MatchString(m.Version) || m.Format != 1 || m.Product != product || m.Helper != 1 || m.Sequence < 1 || m.Platform != expected || len(m.Files) == 0 || len(m.Files) > 20000 || !safePath(m.Entry) {
		return m, errors.New("incompatible shell manifest")
	}
	names := map[string]bool{}
	var total int64
	for _, f := range m.Files {
		if !safePath(f.Path) || names[f.Path] || len(f.SHA256) != 64 || f.Size < 0 || f.Size > 1024*1024*1024 || (f.Mode != 0644 && f.Mode != 0755) {
			return m, errors.New("invalid shell file")
		}
		if _, e = hex.DecodeString(f.SHA256); e != nil {
			return m, e
		}
		names[f.Path] = true
		total += f.Size
	}
	if total > 3*1024*1024*1024 || !names[m.Entry] {
		return m, errors.New("invalid shell size/entry")
	}
	for _, l := range m.Links {
		if !safePath(l.Path) || names[l.Path] || l.Target == "" || filepath.IsAbs(l.Target) || strings.ContainsAny(l.Target, "\\:\x00\r\n\t") {
			return m, errors.New("invalid shell link")
		}
		resolved := filepath.Clean(filepath.Join(filepath.Dir(l.Path), l.Target))
		if !within(".", resolved) {
			return m, errors.New("link escapes shell")
		}
		names[l.Path] = true
	}
	return m, nil
}
func verifyTree(root string, m Manifest) error {
	actual, e := filepath.EvalSymlinks(root)
	if e != nil || actual != filepath.Clean(root) {
		return errors.New("candidate is not canonical")
	}
	for _, f := range m.Files {
		name := filepath.Join(root, filepath.FromSlash(f.Path))
		actual, e = filepath.EvalSymlinks(name)
		if e != nil || actual != name || !within(root, actual) {
			return fmt.Errorf("unsafe file %s", f.Path)
		}
		info, e := os.Stat(name)
		if e != nil || !info.Mode().IsRegular() || info.Size() != f.Size {
			return fmt.Errorf("file size %s", f.Path)
		}
		file, e := os.Open(name)
		if e != nil {
			return e
		}
		h := sha256.New()
		_, e = io.Copy(h, file)
		_ = file.Close()
		if e != nil || hex.EncodeToString(h.Sum(nil)) != f.SHA256 {
			return fmt.Errorf("file hash %s", f.Path)
		}
		if runtime.GOOS != "windows" && int(info.Mode().Perm()) != f.Mode {
			return fmt.Errorf("file mode %s", f.Path)
		}
	}
	for _, l := range m.Links {
		target, e := os.Readlink(filepath.Join(root, filepath.FromSlash(l.Path)))
		if e != nil || target != l.Target {
			return fmt.Errorf("link mismatch %s", l.Path)
		}
		actual, e = filepath.EvalSymlinks(filepath.Join(root, filepath.FromSlash(l.Path)))
		if e != nil || !within(root, actual) {
			return fmt.Errorf("link escapes %s", l.Path)
		}
	}
	return nil
}
func validatePlan(p Plan) error {
	if len(p.Token) != 64 {
		return errors.New("invalid token")
	}
	if _, e := hex.DecodeString(p.Token); e != nil {
		return e
	}
	for _, v := range []string{p.Target, p.Candidate, p.Backup, p.Root, p.Manifest, p.Journal, p.ACK, p.Started, p.UserData} {
		if !filepath.IsAbs(v) || filepath.Clean(v) != v {
			return errors.New("noncanonical transaction path")
		}
	}
	if p.Parent < 1 || p.Timeout < 5 || p.Timeout > 120 || filepath.Dir(p.Candidate) != filepath.Dir(p.Target) || p.Candidate != p.Target+".candidate-"+p.Token || p.Backup != p.Target+".backup-"+p.Token {
		return errors.New("invalid target transaction")
	}
	if !within(p.UserData, p.Root) || !within(p.Root, p.Manifest) || !within(p.Root, p.Journal) || !within(p.Root, p.ACK) || !within(p.Root, p.Started) {
		return errors.New("invalid journal path")
	}
	if runtime.GOOS == "darwin" && (!strings.HasSuffix(p.Target, ".app") || strings.Contains(p.Target, "/Volumes/") || strings.Contains(p.Target, "/AppTranslocation/")) {
		return errors.New("unsupported installation")
	}
	return nil
}
func identity(root string) error {
	rel := "resources/mindbattle-installation.json"
	if runtime.GOOS == "darwin" {
		rel = "Contents/Resources/mindbattle-installation.json"
	}
	b, e := os.ReadFile(filepath.Join(root, filepath.FromSlash(rel)))
	if e != nil {
		return e
	}
	var v struct {
		Product string `json:"product"`
		Pin     string `json:"pin"`
	}
	if e = json.Unmarshal(b, &v); e != nil {
		return e
	}
	if v.Product != product || v.Pin != pinnedKey {
		return errors.New("installation identity mismatch")
	}
	return nil
}
func run(p Plan, m Manifest) error {
	j := Journal{Phase: "prepared", Version: m.Version, Target: p.Target, Backup: p.Backup}
	save := func(phase string, e error) error {
		j.Phase = phase
		j.Error = ""
		if e != nil {
			j.Error = e.Error()
		}
		return atomicJSON(p.Journal, j)
	}
	if e := validatePlan(p); e != nil {
		return e
	}
	if e := identity(p.Target); e != nil {
		return e
	}
	if e := identity(p.Candidate); e != nil {
		return e
	}
	if e := verifyTree(p.Candidate, m); e != nil {
		return e
	}
	if _, e := os.Lstat(p.Backup); !os.IsNotExist(e) {
		return errors.New("backup already exists")
	}
	if e := save("prepared", nil); e != nil {
		return e
	}
	if e := os.WriteFile(p.Started, []byte(p.Token), 0600); e != nil {
		return e
	}
	if e := waitParent(p.Parent, 30*time.Second); e != nil {
		return e
	}
	if e := os.Rename(p.Target, p.Backup); e != nil {
		return e
	}
	rollback := func(cause error, child *os.Process) error {
		if child != nil {
			stopChild(child)
			waitGone(child, 5*time.Second)
		}
		failed := p.Candidate + ".failed"
		_ = os.RemoveAll(failed)
		if _, e := os.Stat(p.Target); e == nil {
			if e = os.Rename(p.Target, failed); e != nil {
				_ = save("recovery-required", e)
				return e
			}
		}
		if e := os.Rename(p.Backup, p.Target); e != nil {
			_ = save("recovery-required", e)
			return e
		}
		if e := identity(p.Target); e != nil {
			_ = save("recovery-required", e)
			return e
		}
		_ = save("rolled-back", cause)
		cmd := exec.Command(filepath.Join(p.Target, filepath.FromSlash(m.Entry)), "--user-data-dir="+p.UserData)
		cmd.Dir = p.UserData
		cmd.Env = os.Environ()
		_ = cmd.Start()
		return cause
	}
	if e := save("old-moved", nil); e != nil {
		return rollback(e, nil)
	}
	if e := os.Rename(p.Candidate, p.Target); e != nil {
		return rollback(e, nil)
	}
	if e := save("new-moved", nil); e != nil {
		return rollback(e, nil)
	}
	cmd := exec.Command(filepath.Join(p.Target, filepath.FromSlash(m.Entry)), "--user-data-dir="+p.UserData)
	cmd.Dir = p.UserData
	cmd.Env = append(os.Environ(), "MINDBATTLE_SHELL_ACK="+p.ACK, "MINDBATTLE_SHELL_TOKEN="+p.Token)
	if e := cmd.Start(); e != nil {
		return rollback(e, nil)
	}
	exited := make(chan error, 1)
	go func() { exited <- cmd.Wait() }()
	deadline := time.Now().Add(time.Duration(p.Timeout) * time.Second)
	for time.Now().Before(deadline) {
		b, e := os.ReadFile(p.ACK)
		if e == nil && string(b) == p.Token {
			return save("confirmed", nil)
		}
		select {
		case <-exited:
			return rollback(errors.New("new shell exited before startup acknowledgement"), nil)
		default:
		}
		time.Sleep(100 * time.Millisecond)
	}
	return rollback(errors.New("new shell did not acknowledge startup"), cmd.Process)
}
func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "expected transaction file and hash")
		os.Exit(2)
	}
	raw, e := os.ReadFile(os.Args[1])
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
	hash := sha256.Sum256(raw)
	if hex.EncodeToString(hash[:]) != os.Args[2] {
		fmt.Fprintln(os.Stderr, "transaction hash mismatch")
		os.Exit(1)
	}
	var p Plan
	if e = json.Unmarshal(raw, &p); e == nil {
		e = validatePlan(p)
	}
	validPlan := e == nil
	var m Manifest
	if e == nil {
		var b []byte
		b, e = os.ReadFile(p.Manifest)
		if e == nil {
			m, e = verifyManifest(b)
		}
	}
	if e == nil {
		e = run(p, m)
	}
	if e != nil {
		if validPlan {
			var j Journal
			b, _ := os.ReadFile(p.Journal)
			_ = json.Unmarshal(b, &j)
			if j.Phase != "rolled-back" && j.Phase != "recovery-required" {
				_ = atomicJSON(p.Journal, Journal{Phase: "error", Version: m.Version, Target: p.Target, Backup: p.Backup, Error: e.Error()})
			}
		}
		fmt.Fprintln(os.Stderr, e)
		os.Exit(1)
	}
}
