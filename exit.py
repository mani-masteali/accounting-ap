import time
import sys
from rich.console import Console
from rich.text import Text


def exit(startTime):
    endTime = time.time()
    Console().print(Text("Total time:", style="yellow"), Text(
        f"{endTime - startTime:.2f}", style="purple"), Text("seconds", style="yellow"))
    Console().print(Text("Exiting ...", style="magenta"))
    time.sleep(1)
    sys.exit()
