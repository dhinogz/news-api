package client

import (
	"log"
	"testing"
)

func TestAuthGet(t *testing.T) {
	client := NewClient(nil, URL)
	resp, err := client.LogIn("admin", "admin")
	// resp, err := client.GetCurrentUser()
	if err != nil {
		t.Error(err)
	}
	log.Println(resp)
}
