try:
    import tablegen.binding as binding
except ImportError: # pragma: no cover
    print("WARNING: Cannot import binding module") # pragma: no cover

from tablegen.unit.record import TypedRecord, TableGenRecord
from tablegen.context import TableGenContext

__all__ = ["binding", "TypedRecord", "TableGenRecord", "TableGenContext"]