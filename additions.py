from rich.console import Console
import datetime


console = Console()

def print_text(text):
    now = datetime.datetime.now()
    console.print(f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [green]{text}[/green]')
    
def print_error(text):
    now = datetime.datetime.now()
    console.print(f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [red][bold]ERROR:[/bold] {text}[/red]')