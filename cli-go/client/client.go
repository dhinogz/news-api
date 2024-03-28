package client

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/url"
	"strings"
)

// Client manages communication with the BPOST API.
type Client struct {
	// HTTP client to communicate with the request API.
	*http.Client

	// Base URL for API requests.
	baseURL string

	// Session token stored in memory, used in all requests
	sessionToken string
}

// NewClient returns a new New API client.
func NewClient(httpClient *http.Client, url string) *Client {
	if httpClient == nil {
		httpClient = http.DefaultClient
	}
	// TODO: default cookie jar uses sessionid cookie with default username and password
	c := &Client{
		Client:  httpClient,
		baseURL: url,
	}
	return c
}

func (c *Client) NewRequest(method, url string, body interface{}) (*http.Request, error) {
	reqURL := url

	reqURL = c.baseURL + reqURL

	buf := &bytes.Buffer{}
	if err := json.NewEncoder(buf).Encode(&body); err != nil {
		return nil, err
	}

	req, err := http.NewRequest(method, reqURL, buf)
	if err != nil {
		return nil, err
	}

	return req, nil
}

func (c *Client) NewRequestURLForm(method, url string, v url.Values) (*http.Request, error) {
	reqURL := url

	reqURL = c.baseURL + reqURL

	req, err := http.NewRequest(method, reqURL, strings.NewReader(v.Encode()))
	if err != nil {
		return nil, err
	}

	return req, nil
}
