from types import SimpleNamespace
from typing import Any
from ..wrapper.recordkeeper import RecordKeeper

class RecordContext(SimpleNamespace):

    def load(self, Records: RecordKeeper):
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        value.tbl.name = name
        return super().__setattr__(name, value)