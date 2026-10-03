package main

import (
	"errors"
	"os"
	"syscall"
	"time"
)

func waitParent(pid int, timeout time.Duration) error {
	end := time.Now().Add(timeout)
	for time.Now().Before(end) {
		e := syscall.Kill(pid, 0)
		if e == syscall.ESRCH {
			return nil
		}
		if e != nil {
			return e
		}
		time.Sleep(100 * time.Millisecond)
	}
	return errors.New("game did not exit")
}
func waitGone(p *os.Process, t time.Duration) { _ = waitParent(p.Pid, t) }

func stopChild(p *os.Process) { _ = p.Kill() }
