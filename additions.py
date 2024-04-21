from rich.console import Console
import datetime


console = Console()


def print_text(*args):
    text = ""
    for i in args:
        if i != args[-1]:
            text += f"{i}, "
        else:
            text += f"{i}"

    now = datetime.datetime.now()
    console.print(
        f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [green]{text}[/green]'
    )


def print_error(*args):
    text = ""
    for i in args:
        if i != args[-1]:
            text += f"{i}, "
        else:
            text += f"{i}"

    now = datetime.datetime.now()
    console.print(
        f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [red][bold]ERROR:[/bold] {text}[/red]'
    )


def print_multiline_text(text):
    console.print(text)
