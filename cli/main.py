import typer
import client
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from richer.table import ListTable

app = typer.Typer(no_args_is_help=True)


@app.command()
def login(url: str):
    username = typer.prompt("Username")
    password = typer.prompt("Password")
    c = client.Client()
    c.login(url, username, password)

    print("successful login")


@app.command()
def logout():
    c = client.Client()
    c.logout()

    print("Logout successfully!")


@app.command()
def news(
    id: str = "*",
    cat: str = "*",
    reg: str = "*",
    date: str = "*"
):
    """
        Fetch news from a specific agency or from a random sample (20 agencies)

        OPTIONS:

            id: agency code that a news agency identifies with. Use "MINE" if you want to fetch only current session's stories.

            cat: filters by story category

            reg: filters by story region

            date: filters stories after given story date
    """

    c = client.Client()
    sf = client.StoryFilters(
        story_cat=cat,
        story_region=reg,
        story_date=date,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Getting latest stories...")

        stories = c.get_stories(id, sf)

    console = Console()
    if not stories:
        print("No news found")
        return

    console.print(ListTable(stories))


@app.command()
def post():
    headline = typer.prompt("Headline")
    category = typer.prompt("Category")
    region = typer.prompt("Region")
    details = typer.prompt("Details")

    story = client.Story(
        category=category,
        details=details,
        headline=headline,
        region=region,
    )

    c = client.Client()
    msg = c.create_story(story)
    print(msg)


@app.command()
def list():
    c = client.Client()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Getting agencies...")
        a = c.get_agencies()
    console = Console()
    console.print(ListTable(a))


@app.command()
def delete(story_key: str):
    c = client.Client()
    is_deleted = c.delete_story(story_key)
    if not is_deleted:
        print("could not delete story")
        return
    print("successfully deleted story")


if __name__ == "__main__":
    app()
