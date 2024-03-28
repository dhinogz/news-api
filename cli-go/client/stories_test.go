package client

import (
	"errors"
	"log"
	"testing"
)

var (
	URL = "http://localhost:8000/api"
)

func TestStoryFetch(t *testing.T) {
	client := NewClient(nil, URL)
	resp, err := client.FetchStory(8)
	if err != nil {
		t.Error(err)
	}
	log.Println(resp)
}

func TestNonExistingStoryFetch(t *testing.T) {
	client := NewClient(nil, URL)
	resp, err := client.FetchStory(1)
	if err != nil {
		if errors.Is(err, ErrStoryNotFound) {
			log.Println(resp)
			return
		}
		t.Error(err)
	}
	t.Error(errors.New("story exists, but it shouldnt"))
}

func TestStoriesFetch(t *testing.T) {
	client := NewClient(nil, URL)
	filters := StoryFilters{
		Category: "tech",
	}
	resp, err := client.FetchStories(filters)
	if err != nil {
		t.Error(err)
	}
	log.Println(resp)
}
func TestStoriesCreate(t *testing.T) {
	client := NewClient(nil, URL)
	s := Story{
		Category: "tech",
		Details:  "Test details from Golang",
		Headline: "Headline from Golang",
		Region:   "uk",
	}
	resp, err := client.CreateStory(s)
	if err != nil {
		t.Error(err)
	}
	log.Println(resp)
}
