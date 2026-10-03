package main

import (
	"errors"
	"os"
	"os/exec"
	"strconv"
	"syscall"
	"time"
)

func waitParent(pid int, timeout time.Duration) error {
	h, e := syscall.OpenProcess(0x00100000, false, uint32(pid))
	if e == syscall.Errno(87) {
		return nil
	}
	if e != nil {
		return e
	}
	defer syscall.CloseHandle(h)
	event, e := syscall.WaitForSingleObject(h, uint32(timeout.Milliseconds()))
	if e != nil {
		return e
	}
	if event != 0 {
		return errors.New("game did not exit")
	}
	return nil
}
func waitGone(p *os.Process, t time.Duration) { _ = waitParent(p.Pid, t) }

func stopChild(p *os.Process) {
	_ = exec.Command("taskkill.exe", "/PID", strconv.Itoa(p.Pid), "/T", "/F").Run()
	_ = p.Kill()
}
