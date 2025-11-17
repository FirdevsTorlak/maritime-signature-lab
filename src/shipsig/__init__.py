"""shipsig - Maritime Signature Lab toolkit.

Provides helpers to initialise the database, import sample data and
perform basic analyses on acoustic, magnetic, RCS and IR signatures.
"""

from . import config
from . import db
from . import loaders
from . import analysis

__all__ = ["config", "db", "loaders", "analysis"]