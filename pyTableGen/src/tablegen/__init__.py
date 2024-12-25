try:
    import tablegen.binding as binding
except ImportError:
    print("WARNING: Cannot import binding module")

from tablegen.unit.record import TypedRecord, TableGenRecord
from tablegen.context import TableGenContext

__all__ = ["TypedRecord", "TableGenRecord", "TableGenContext"]