import os
from dataclasses import dataclass, asdict

import requests
from urllib.parse import urljoin, urlencode

import json
import random


@dataclass
class StoryResponse:
    key: str
    headline: str
    date: str
    author: str
    details: str
    category: str
    region: str
    code: str = ""


@dataclass
class Story:
    category: str
    details: str
    headline: str
    region: str


@dataclass
class StoryFilters:
    story_cat: str = "*"
    story_region: str = "*"
    story_date: str = "*"


@dataclass
class Agency:
    agency_name: str
    url: str
    code: str


SESSION_FILE_PATH = "session.txt"
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_TOKEN = ""
MAX_RANDOM_AGENCIES = 20
MAX_STORY_PER_AGENCY = 3


class Client(requests.Session):
    def __init__(self) -> None:
        super().__init__()

        self.baseurl = DEFAULT_BASE_URL
        self.session_token = ""

        self.directory_url = \
            "https://newssites.pythonanywhere.com/api/directory/"

    def _load_session_data(self):
        try:
            with open(SESSION_FILE_PATH, 'r') as file:
                session_file = file.read()
                data = session_file.split("\n")
                self.baseurl = data[0]
                self.session_token = data[1]

        except FileNotFoundError:
            print("User is not logged in, restricted access for cli")
            print("Using default url: ", DEFAULT_BASE_URL)
            self.baseurl = DEFAULT_BASE_URL
            self.session_token = DEFAULT_TOKEN

    def login(self, url: str, username: str, password: str) -> bool:
        data = {
            "username": username,
            "password": password,
        }
        if url[-1] == "/":
            url = url[:-1]
        resp = self.post(f"{url}/api/login/", data)
        if resp.status_code != 200:
            return False
        for c in resp.cookies:
            if c.name == "sessionid":
                token = c.value

        with open(SESSION_FILE_PATH, 'w+') as file:
            file.write(f"{url}\n{token}")

        self.baseurl = url
        self.session_token = token

        print("session.txt file created with auth details")
        return True

    def logout(self) -> None:
        self._load_session_data()
        url = f"{self.baseurl}/api/logout/"
        self.post(url)
        if os.path.exists(SESSION_FILE_PATH):
            os.remove(SESSION_FILE_PATH)

    def get_stories(self, code: str, filters: StoryFilters) -> list[StoryResponse]:
        stories = []
        if code != "*":
            url = self._get_agency_url_by_code(code)
            if url == "":
                return []
            if url[-1] != "/":
                url += "/"
            url = f"{url}api/stories?{urlencode(asdict(filters))}"

            resp = self.get(url)
            if resp.status_code != 200:
                return []
            obj = resp.json()
            for s in obj["stories"]:
                stories.append(
                    StoryResponse(
                        key=str(s["key"]),
                        category=s["story_cat"],
                        details=s["story_details"],
                        headline=s["headline"],
                        region=s["story_region"],
                        date=s["story_date"],
                        author=s["author"],
                        code=code,
                    )
                )
        else:
            agencies = self._get_random_agencies()
            for a in agencies:
                try:
                    url = a.url
                    if url == "":
                        continue
                    if url[-1] != "/":
                        url += "/"
                    url = f"{url}api/stories?{urlencode(asdict(filters))}"

                    resp = self.get(url)
                    if resp.status_code != 200:
                        continue
                    obj = resp.json()
                    story_count = 0
                    for s in obj["stories"]:
                        if story_count >= MAX_STORY_PER_AGENCY:
                            continue
                        stories.append(
                            StoryResponse(
                                key=str(s["key"]),
                                category=s["story_cat"],
                                details=s["story_details"],
                                headline=s["headline"],
                                region=s["story_region"],
                                date=s["story_date"],
                                author=s["author"],
                                code=a.code,
                            )
                        )
                        story_count += 1
                except Exception:
                    continue

        return stories

    def create_story(self, story: Story) -> str:
        self._load_session_data()
        url = f"{self.baseurl}/api/stories"
        if "localhost" in self.baseurl:
            url = "http://" + url
        data = json.dumps(asdict(story))
        resp = self.post(url, data)
        if resp.status_code != 201:
            return resp.content
        return resp.content

    def get_agencies(self) -> list[Agency]:
        resp = self.get(self.directory_url)
        obj = resp.json()
        agencies = []
        for a in obj:
            agencies.append(
                Agency(
                    agency_name=a["agency_name"],
                    url=a["url"],
                    code=a["agency_code"],
                )
            )
        return agencies

    def delete_story(self, story_key) -> bool:
        self._load_session_data()
        resp = self.delete(f"http://{self.baseurl}/api/stories/{story_key}")
        return resp.status_code == 200

    def _get_random_agencies(self) -> list[Agency]:
        resp = self.get(self.directory_url)
        obj = resp.json()
        agencies = []
        for a in obj:
            agencies.append(
                Agency(
                    agency_name=a["agency_name"],
                    url=a["url"],
                    code=a["agency_code"],
                )
            )
        random.shuffle(agencies)

        return agencies[:MAX_RANDOM_AGENCIES]

    def _get_agency_url_by_code(self, code: str) -> str:
        resp = self.get(self.directory_url)
        obj = resp.json()
        for a in obj:
            if a["agency_code"] == code:
                return a["url"]
        return ""

    def request(self, method, url, *args, **kwargs):
        full_url = urljoin(self.baseurl, url)

        if 'cookies' not in kwargs:
            kwargs['cookies'] = {}

        kwargs['cookies']['sessionid'] = self.session_token

        return super().request(method, full_url, *args, **kwargs)
