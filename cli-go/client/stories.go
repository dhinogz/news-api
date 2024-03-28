package client

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

type StoryResponse struct {
	ID           int    `json:"id"`
	Headline     string `json:"headline"`
	StoryDetails string `json:"story_details"`
	StoryCat     string `json:"story_cat"`
	StoryRegion  string `json:"story_region"`
	StoryDate    string `json:"story_date"`
	Author       string `json:"author"`
}

type Story struct {
	Category string `json:"category"`
	Details  string `json:"details"`
	Headline string `json:"headline"`
	Region   string `json:"region"`
}

func (c *Client) FetchStory(id int) (*StoryResponse, error) {
	resource := fmt.Sprintf("/stories/%d", id)
	req, err := c.NewRequest(http.MethodGet, resource, nil)
	if err != nil {
		return nil, err
	}
	resp, err := c.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// TODO: handle error codes
	if resp.StatusCode == http.StatusNotFound {
		return nil, ErrStoryNotFound
	}

	response := StoryResponse{}
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, err
	}
	return &response, nil
}

type StoryFilters struct {
	Category string
	Region   string
	Date     string
}

func (c *Client) FetchStories(sf StoryFilters) ([]StoryResponse, error) {
	resource := "/stories"
	params := url.Values{}
	if sf.Category != "" {
		params.Add("story_cat", sf.Category)
	}
	if sf.Region != "" {
		params.Add("story_region", sf.Region)
	}
	if sf.Date != "" {
		params.Add("story_date", sf.Date)
	}
	if len(params) > 0 {
		resource += "?" + params.Encode()
	}

	req, err := c.NewRequest(http.MethodGet, resource, nil)
	if err != nil {
		return nil, err
	}
	resp, err := c.Do(req)
	if err != nil {
		// TODO: handle error codes
		return nil, err
	}
	defer resp.Body.Close()

	response := map[string][]StoryResponse{}
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, err
	}
	return response["stories"], nil
}

func (c *Client) CreateStory(s Story) (string, error) {
	resource := "/stories"

	req, err := c.NewRequest(http.MethodPost, resource, s)
	if err != nil {
		return "", err
	}
	resp, err := c.Do(req)
	if err != nil {
		// TODO: handle error codes
		return "", err
	}
	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	responseString := string(responseBody)

	return responseString, nil
}
