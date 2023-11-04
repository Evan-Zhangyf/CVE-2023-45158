import re

from .._gae import gae
from ..helpers._internals import Dispatcher


class Adapters(Dispatcher):
    def register_for(self, *uris):
        def wrap(dispatch_class):
            for uri in uris:
                self._registry_[uri] = dispatch_class
            return dispatch_class

        return wrap

    def get_for(self, uri):
        try:
            return self._registry_[uri]
        except KeyError:
            raise SyntaxError("Adapter not found for %s" % uri)


adapters = Adapters("adapters")


class AdapterMeta(type):
    """Metaclass to support manipulation of adapter classes.

    At the moment is used to intercept `entity_quoting` argument passed to DAL.
    """

    def __call__(cls, *args, **kwargs):
        uploads_in_blob = kwargs.get("adapter_args", {}).get(
            "uploads_in_blob", cls.uploads_in_blob
        )
        cls.uploads_in_blob = uploads_in_blob

        entity_quoting = kwargs.get("entity_quoting", True)
        if "entity_quoting" in kwargs:
            del kwargs["entity_quoting"]

        obj = super(AdapterMeta, cls).__call__(*args, **kwargs)

        regex_ent = r"(\w+)"
        if not entity_quoting:
            obj.dialect.quote_template = "%s"
        else:
            regex_ent = obj.dialect.quote_template % regex_ent
        # FIXME: this regex should NOT be compiled
        obj.REGEX_TABLE_DOT_FIELD = re.compile(r"^%s\.%s$" % (regex_ent, regex_ent))

        return obj


def with_connection(f):
    def wrap(*args, **kwargs):
        if args[0].connection:
            return f(*args, **kwargs)
        return None

    return wrap


def with_connection_or_raise(f):
    def wrap(*args, **kwargs):
        if not args[0].connection:
            if len(args) > 1:
                raise ValueError(args[1])
            raise RuntimeError("no connection available")
        return f(*args, **kwargs)

    return wrap


from .base import NoSQLAdapter, SQLAdapter
from .couchdb import CouchDB
from .db2 import DB2
from .firebird import FireBird
from .google import GoogleSQL
from .informix import Informix
from .ingres import Ingres
from .mongo import Mongo
from .mssql import MSSQL
from .mysql import MySQL
from .oracle import Oracle
from .postgres import Postgre, PostgrePsyco
from .sap import SAPDB
from .snowflake import Snowflake
from .sqlite import SQLite
from .teradata import Teradata
