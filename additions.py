from rich.console import Console
import datetime


console = Console()

def print_text(text1, text2='', text3='', text4='', text5=''):
    now = datetime.datetime.now()
    console.print(f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [green]{text1} {text2} {text3} {text4} {text5}[/green]')

    
def print_error(text):
    now = datetime.datetime.now()
    console.print(f'[bold blue]{now.strftime("%Y-%m-%d %H:%M:%S")}:[/bold blue] [red][bold]ERROR:[/bold] {text}[/red]')
    
    
def print_multiline_text(text):
    console.print(text)