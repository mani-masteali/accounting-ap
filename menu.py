import time
from rich.console import Console
from rich.text import Text
from colors import blue, red, green, yellow, purple, cyan, magenta, white, black, gray
if __name__ == "__main__":
    startTime = time.time()  # Start menu and app usage time recording
    endTime = time.time()
Console().print(Text("Total time:", style=yellow), Text(
    f"{endTime - startTime:.2f}", style=magenta), Text("seconds", style=yellow))
