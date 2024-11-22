import typer
import yaml
import requests
import os
from whats_for_lunch.Menu import Menu

app = typer.Typer()

@app.command()
def base(
    tomorrow: bool = typer.Option(None, help="Fetch tomorrow's menu"),
    crumble: bool = typer.Option(None, help="Find the day of the next crumble"),
    dump: bool = typer.Option(False, help="If set, save the menu to a file")
):
    """
    Get todays meals and format it
    """
    if tomorrow:
        get_tomorrows_menu()
    elif crumble:
        get_crumble_day()
    elif dump:
        dump_menu()
    else:
        get_todays_menu()

def get_todays_menu():
    endpoint = get_server_address()
    response = make_request(endpoint, "")
    thisMenu = Menu(response)
    typer.echo(str(thisMenu))
    typer.Exit(0)


def make_request(endpoint: str, query: str):
    response = requests.get(f"{endpoint}/{query}")
    if not response.status_code == 200:
        raise ValueError(f"Failed to get data from server. Status code: {response.status_code}")
    return response.json()



def get_tomorrows_menu():
    endpoint = get_server_address()
    response = make_request(endpoint, "tomorrow")
    thisMenu = Menu(response)
    typer.echo(str(thisMenu))
    typer.Exit(0)

def get_crumble_day():
    endpoint = get_server_address()
    response = make_request(endpoint, "crumble-finder")
    days = response["days"]
    if days == "No crumble left this week":
        typer.echo("No crumble served for the rest of this week!")
        typer.Exit(0)
    typer.echo(f"Crumble is served on {days}")
    typer.Exit(0)

def dump_menu():
    raise NotImplementedError("Not implemented yet")
    endpoint = get_server_address()
    response = make_request(endpoint, "dump-week")
    wc = response.pop("wc")
    typer.echo(f"Menu for week commencing {wc}")
    for day in response:
        thisMenu = Menu(response[day])
        typer.echo(str(thisMenu))
    typer.Exit(0)
    


def get_server_address():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["serverAddress"]