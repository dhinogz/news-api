package main

import (
	"fmt"
	"log"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/dhinogz/news-client/client"
)

type model struct {
	newsClient client.Client
	cursor     int
	selected   map[int]struct{}
	stories    []client.StoryResponse
}

var baseURL = "http://localhost:8000/api"

func initialModel() model {
	m := model{
		newsClient: *client.NewClient(nil, baseURL),
		selected:   make(map[int]struct{}),
	}
	s, err := m.newsClient.FetchStories(client.StoryFilters{})
	if err != nil {
		log.Fatal(err)
	}
	m.stories = s

	return m
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	// Is it a key press?
	case tea.KeyMsg:

		// Cool, what was the actual key pressed?
		switch msg.String() {

		// These keys should exit the program.
		case "ctrl+c", "q":
			return m, tea.Quit

		// The "up" and "k" keys move the cursor up
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}

		// The "down" and "j" keys move the cursor down
		case "down", "j":
			if m.cursor < len(m.stories)-1 {
				m.cursor++
			}

		// The "enter" key and the spacebar (a literal space) toggle
		// the selected state for the item that the cursor is pointing at.
		case "enter", " ":
			_, ok := m.selected[m.cursor]
			if ok {
				delete(m.selected, m.cursor)
			} else {
				m.selected[m.cursor] = struct{}{}
			}
		}
	}

	// Return the updated model to the Bubble Tea runtime for processing.
	// Note that we're not returning a command.
	return m, nil
}

func (m model) View() string {
	s := "Select a news to view\n\n"

	for i, story := range m.stories {
		cursor := " "
		if m.cursor == i {
			if _, ok := m.selected[i]; ok {
				cursor = "v"
			} else {
				cursor = ">"
			}
		}

		s += fmt.Sprintf("%s %s\n", cursor, story.Headline)
		storyDetails := ""
		if _, ok := m.selected[i]; ok {
			storyDetails = fmt.Sprintf("\tAuthor: %s\n\tDate: %s\n\tCategory: %s\n\tDetails: %s\n", story.Author, story.StoryDate, story.StoryCat, story.StoryDetails)
			s += storyDetails
		}
	}
	s += "\nPress q to quit\n"

	return s
}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
