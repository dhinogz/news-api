package client

import (
	"encoding/json"
	"errors"
	"net/http"
	"net/url"
)

func (c *Client) LogIn(username, password string) (User, error) {
	// encode to www-form-x-encoded
	data := url.Values{}
	data.Set("username", username)
	data.Set("password", password)

	// create new request to api/login
	req, err := c.NewRequestURLForm(http.MethodPost, "/login/", data)
	if err != nil {
		return User{}, err
	}
	req.Header.Set("accept", "*/*")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	// do request
	resp, err := c.Do(req)
	if err != nil {
		return User{}, errors.New("couldnt do login request")
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return User{}, errors.New("login failed: " + resp.Status)
	}

	// request sets cookie session token
	cookies := resp.Cookies()
	if len(cookies) < 1 {
		return User{}, errors.New("no cookies")
	}
	for _, cookie := range cookies {
		if cookie.Name == "sessionid" {
			c.sessionToken = cookie.Value
		}
	}
	if c.sessionToken == "" {
		return User{}, errors.New("no sessionid cookie")
	}

	// test auth
	u, err := c.GetCurrentUser()
	if err != nil {
		return User{}, err
	}

	// TODO: return something? what error?
	return u, nil
}

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func (c *Client) GetCurrentUser() (User, error) {
	req, err := c.NewRequest(http.MethodGet, "/user/", nil)
	if err != nil {
		return User{}, err
	}
	// add session id cookie
	req.AddCookie(&http.Cookie{
		Name:  "sessionid",
		Value: c.sessionToken,
	})
	// do request
	resp, err := c.Do(req)
	if err != nil {
		return User{}, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusServiceUnavailable {
		return User{}, errors.New("current user not found")
	}

	response := User{}
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return User{}, err
	}

	return response, nil
}
