"""
To be used like:

from .integrations import get_integrator, Brand

print(get_integrator(Brand.TRADER_JOES).hello("Jerry"))
> "Howdy, Jerry"
print(get_integrator(Brand.KROGER).hello("Jerry"))
> "Hello, Jerry"

Register the function in the associated integrator's __init__.py like:
from .hello import hello
"""
from ..model.brand import Brand
from . import kroger
from . import trader_joes

class IntegratorException(Exception):
    pass

def get_integrator(integrator: Brand):
    match integrator:
        case Brand.KROGER:
            return kroger
        case Brand.TRADER_JOES:
            return trader_joes
        case _:
            raise IntegratorException(f"Integrator {integrator} not found.")
