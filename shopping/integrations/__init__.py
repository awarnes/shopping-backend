"""
To be used like:

from .integrations import get_integrator, Integrator

print(get_integrator(Integrator.TRADER_JOES).hello("Jerry"))
> "Howdy, Jerry"
print(get_integrator(Integrator.KROGER).hello("Jerry"))
> "Hello, Jerry"

Register the function in the associated integrator's __init__.py like:
from .hello import hello
"""
from enum import Enum
from . import kroger
from . import trader_joes

class IntegratorException(Exception):
    pass

class Integrator(str, Enum):
    KROGER = "KROGER"
    TRADER_JOES = "TRADER_JOES"

def get_integrator(integrator: Integrator):
    match integrator:
        case Integrator.KROGER:
            return kroger
        case Integrator.TRADER_JOES:
            return trader_joes
        case _:
            raise IntegratorException(f"Integrator {integrator} not found.")
