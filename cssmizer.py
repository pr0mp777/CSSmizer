import sys
import os
import time
import signal
import argparse
import re
from rich.console import Console
from rich.progress import Progress
from rich.text import Text
import logging

console = Console()

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

null_handler = NullHandler()
logging.getLogger().addHandler(null_handler)
logging.getLogger().setLevel(logging.CRITICAL)

def signal_handler(sig, frame):
    console.print("\n[INFO] Minification process cancelled.", style="bold yellow")
    sys.exit(1)

banner = """
.d8888b.   .d8888b.   .d8888b.                d8b                            
d88P  Y88b d88P  Y88b d88P  Y88b               Y8P                            
888    888 Y88b.      Y88b.                                                   
888         "Y888b.    "Y888b.   88888b.d88b.  888 88888888  .d88b.  888d888  
888            "Y88b.     "Y88b. 888 "888 "88b 888    d88P  d8P  Y8b 888P"    
888    888       "888       "888 888  888  888 888   d88P   88888888 888      
Y88b  d88P Y88b  d88P Y88b  d88P 888  888  888 888  d88P    Y8b.     888      
 "Y8888P"   "Y8888P"   "Y8888P"  888  888  888 888 88888888  "Y8888  888      
"""

def print_banner():
    console.print(Text(banner, style="bold bright_magenta"))
    console.print("\nCreated by [bold bright_magenta]Pr0mp7[/bold bright_magenta]\n", style="bold bright_white")

def is_css_file(filepath):
    return filepath.endswith('.css')

def minify_css(css):
    css = re.sub(r'/\*.*?\*/|//.*?\n', '', css, flags=re.DOTALL)
    css = re.sub(r'\s*\n\s*', '\n', css)
    css = re.sub(r'\s{2,}', ' ', css)
    css = re.sub(r'\s*([{}:;>+~()])\s*', r'\1', css)
    return css.strip()

def minify_and_combine_css(file_paths, output_file='minified_output.css'):
    combined_css = ''
    valid_files = []

    for path in file_paths:
        if not os.path.exists(path):
            console.print(f"[red][ERROR] The file '{path}' does not exist. Please check the path.[/red]")
            continue
        if not is_css_file(path):
            console.print(f"[red][ERROR] The file '{path}' is not a CSS file. Skipping...[/red]")
            continue
        valid_files.append(path)

    if not valid_files:
        console.print("[red][ERROR] No valid CSS files provided. Aborting process.[/red]")
        return

    with Progress() as progress:
        task_read = progress.add_task("[cyan]Reading CSS files...", total=len(valid_files))
        for path in valid_files:
            try:
                with open(path, 'r') as file:
                    combined_css += file.read() + '\n'
                progress.update(task_read, advance=1)
            except Exception as e:
                console.print(f"[red][ERROR] Failed to read '{path}': {e}[/red]")
                return

    if combined_css.strip() == "":
        console.print("[red][ERROR] No valid CSS content found. Aborting minification.[/red]")
        return

    console.print("\n[INFO] Starting CSS minification process...\n", style="cyan")
    time.sleep(0.2)

    try:
        minified_css_str = minify_css(combined_css)

        with open(output_file, 'w') as output:
            output.write(minified_css_str)

        original_size = len(combined_css.encode('utf-8'))
        minified_size = len(minified_css_str.encode('utf-8'))

        improvement = ((original_size - minified_size) / original_size) * 100 if original_size > 0 else 0

        console.print(f"[green][+] CSS minified successfully and saved as '{output_file}'.[/green]\n")
        console.print(f"[INFO] Original size: {original_size} bytes")
        console.print(f"[INFO] Minified size: {minified_size} bytes")
        console.print(f"[INFO] Performance improvement: {improvement:.2f}%")

    except Exception as e:
        console.print(f"[red][ERROR] CSS minification failed: {e}")

def show_help():
    print_banner()
    console.print("CSSmizer is a tool that minifies and combines CSS files.", style="bold yellow")
    console.print("[INFO] Usage: [bold blue]python[/bold blue] cssmizer.py [[bold blue]-o[/bold blue] [bold bright_magenta]<output_file>[/bold bright_magenta]] [bold blue]<path/to/css_file1.css>[/bold blue]")

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        console.print(f"[red][ERROR] {message}[/red]")
        show_help()
        print()
        sys.exit(2)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    parser = CustomArgumentParser(description="CSSmizer: A tool for minifying and combining CSS files.", add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-o', '--output', type=str, default='minified_output.css', help='Output file name (default: minified_output.css)')
    parser.add_argument('files', nargs='*', help='CSS files to minify and combine')

    args = parser.parse_args()

    if args.help:
        show_help()
    elif not args.files:
        console.print(f"[red][ERROR] No CSS files provided.[/red]")
        show_help()
    else:
        print_banner()
        minify_and_combine_css(args.files, args.output)

    print()