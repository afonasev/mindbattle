package main

import (
	"reflect"
	"testing"
)

func TestAppLaunchArgsPreservesMutedLaunch(t *testing.T) {
	got := appLaunchArgs(Plan{UserData: "/profile", LaunchMuted: true})
	want := []string{"--user-data-dir=/profile", "--muted"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("appLaunchArgs() = %#v, want %#v", got, want)
	}
}
