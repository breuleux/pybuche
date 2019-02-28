
import sys
from .buche import *
from .repr import *
from .event import *
from .debug import *
from .repl import *


def _print_flush(x):
    print(x, flush=True)


hrepr = HRepr()
H = hrepr.H
master = MasterBuche(hrepr, _print_flush)
buche = Buche(master, '/')
stdbuche = Buche(master, '/stdout')
reader = Reader(sys.stdin)
read = reader.read
repl = Repl(buche, reader)
breakpoint = BucheDb(repl).set_trace
