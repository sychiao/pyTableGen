"""
pybind11 example plugin
"""
from __future__ import annotations
import typing
__all__ = ['BinOpInit', 'BinaryOp', 'BitInit', 'BitRecTy', 'BitsInit', 'BitsRecTy', 'DagInit', 'DagRecTy', 'DefInit', 'Init', 'InitKind', 'InitVector', 'IntInit', 'IntRecTy', 'ListInit', 'ListRecTy', 'OpInit', 'ParseTableGen', 'RecTy', 'RecTyKind', 'Record', 'RecordKeeper', 'RecordMap', 'RecordRecTy', 'RecordVal', 'RecordValVector', 'RecordVector', 'SMLoc', 'SMLocVector', 'SMRange', 'StringFormat', 'StringInit', 'StringInitVector', 'StringRecTy', 'StringVector', 'SuperClassVector', 'TernOpInit', 'TypedInit', 'UnOpInit', 'UnaryOp', 'UnsetInit', 'VarBitInit', 'VarInit', 'getLLVMSourceLoc']
class BinOpInit(OpInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLHS(self) -> Init:
        ...
    def getOpcode(self) -> BinaryOp:
        ...
    def getRHS(self) -> Init:
        ...
class BinaryOp:
    """
    Members:
    
      ADD
    
      SUB
    
      MUL
    
      OR
    
      AND
    
      XOR
    
      SHL
    
      SRA
    
      SRL
    
      LISTCONCAT
    
      STRCONCAT
    
      EQ
    
      NE
    
      LT
    
      LE
    
      GT
    
      GE
    """
    ADD: typing.ClassVar[BinaryOp]  # value = <BinaryOp.ADD: 0>
    AND: typing.ClassVar[BinaryOp]  # value = <BinaryOp.AND: 3>
    EQ: typing.ClassVar[BinaryOp]  # value = <BinaryOp.EQ: 14>
    GE: typing.ClassVar[BinaryOp]  # value = <BinaryOp.GE: 18>
    GT: typing.ClassVar[BinaryOp]  # value = <BinaryOp.GT: 19>
    LE: typing.ClassVar[BinaryOp]  # value = <BinaryOp.LE: 16>
    LISTCONCAT: typing.ClassVar[BinaryOp]  # value = <BinaryOp.LISTCONCAT: 9>
    LT: typing.ClassVar[BinaryOp]  # value = <BinaryOp.LT: 17>
    MUL: typing.ClassVar[BinaryOp]  # value = <BinaryOp.MUL: 2>
    NE: typing.ClassVar[BinaryOp]  # value = <BinaryOp.NE: 15>
    OR: typing.ClassVar[BinaryOp]  # value = <BinaryOp.OR: 4>
    SHL: typing.ClassVar[BinaryOp]  # value = <BinaryOp.SHL: 6>
    SRA: typing.ClassVar[BinaryOp]  # value = <BinaryOp.SRA: 7>
    SRL: typing.ClassVar[BinaryOp]  # value = <BinaryOp.SRL: 8>
    STRCONCAT: typing.ClassVar[BinaryOp]  # value = <BinaryOp.STRCONCAT: 11>
    SUB: typing.ClassVar[BinaryOp]  # value = <BinaryOp.SUB: 1>
    XOR: typing.ClassVar[BinaryOp]  # value = <BinaryOp.XOR: 5>
    __members__: typing.ClassVar[dict[str, BinaryOp]]  # value = {'ADD': <BinaryOp.ADD: 0>, 'SUB': <BinaryOp.SUB: 1>, 'MUL': <BinaryOp.MUL: 2>, 'OR': <BinaryOp.OR: 4>, 'AND': <BinaryOp.AND: 3>, 'XOR': <BinaryOp.XOR: 5>, 'SHL': <BinaryOp.SHL: 6>, 'SRA': <BinaryOp.SRA: 7>, 'SRL': <BinaryOp.SRL: 8>, 'LISTCONCAT': <BinaryOp.LISTCONCAT: 9>, 'STRCONCAT': <BinaryOp.STRCONCAT: 11>, 'EQ': <BinaryOp.EQ: 14>, 'NE': <BinaryOp.NE: 15>, 'LT': <BinaryOp.LT: 17>, 'LE': <BinaryOp.LE: 16>, 'GT': <BinaryOp.GT: 19>, 'GE': <BinaryOp.GE: 18>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BitInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getBit(self, arg0: int) -> Init:
        ...
    def getValue(self) -> bool:
        ...
    def isConcrete(self) -> bool:
        ...
class BitRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class BitsInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def allInComplete(self) -> bool:
        ...
    def getAsString(self) -> str:
        ...
    def getBit(self, arg0: int) -> Init:
        ...
    def getNumBits(self) -> int:
        ...
    def isComplete(self) -> bool:
        ...
    def isConcrete(self) -> bool:
        ...
class BitsRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getNumBits(self) -> int:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class DagInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getArg(self, arg0: int) -> Init:
        ...
    def getArgName(self, arg0: int) -> StringInit:
        ...
    def getArgNames(self) -> StringInitVector:
        ...
    def getArgs(self) -> InitVector:
        ...
    def getName(self) -> StringInit:
        ...
    def getNameStr(self) -> str:
        ...
    def getNumArgs(self) -> int:
        ...
    def getOperator(self) -> Init:
        ...
class DagRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
class DefInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getDef(self) -> Record:
        ...
    def isConcrete(self) -> bool:
        ...
class Init:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getBit(self, arg0: int) -> Init:
        ...
    def getKind(self) -> InitKind:
        ...
    def isConcrete(self) -> bool:
        ...
class InitKind:
    """
    Members:
    
      IK_First
    
      IK_FirstTypedInit
    
      IK_BitInit
    
      IK_BitsInit
    
      IK_DagInit
    
      IK_DefInit
    
      IK_FieldInit
    
      IK_IntInit
    
      IK_ListInit
    
      IK_FirstOpInit
    
      IK_BinOpInit
    
      IK_TernOpInit
    
      IK_UnOpInit
    
      IK_LastOpInit
    
      IK_CondOpInit
    
      IK_FoldOpInit
    
      IK_IsAOpInit
    
      IK_ExistsOpInit
    
      IK_AnonymousNameInit
    
      IK_StringInit
    
      IK_VarInit
    
      IK_VarBitInit
    
      IK_VarDefInit
    
      IK_LastTypedInit
    
      IK_UnsetInit
    """
    IK_AnonymousNameInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_AnonymousNameInit: 18>
    IK_BinOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_BinOpInit: 10>
    IK_BitInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_BitInit: 2>
    IK_BitsInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_BitsInit: 3>
    IK_CondOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_CondOpInit: 14>
    IK_DagInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_DagInit: 4>
    IK_DefInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_DefInit: 5>
    IK_ExistsOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_ExistsOpInit: 17>
    IK_FieldInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_FieldInit: 6>
    IK_First: typing.ClassVar[InitKind]  # value = <InitKind.IK_First: 0>
    IK_FirstOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_FirstOpInit: 9>
    IK_FirstTypedInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_FirstTypedInit: 1>
    IK_FoldOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_FoldOpInit: 15>
    IK_IntInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_IntInit: 7>
    IK_IsAOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_IsAOpInit: 16>
    IK_LastOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_LastOpInit: 13>
    IK_LastTypedInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_LastTypedInit: 24>
    IK_ListInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_ListInit: 8>
    IK_StringInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_StringInit: 19>
    IK_TernOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_TernOpInit: 11>
    IK_UnOpInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_UnOpInit: 12>
    IK_UnsetInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_UnsetInit: 25>
    IK_VarBitInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_VarBitInit: 22>
    IK_VarDefInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_VarDefInit: 23>
    IK_VarInit: typing.ClassVar[InitKind]  # value = <InitKind.IK_VarInit: 20>
    __members__: typing.ClassVar[dict[str, InitKind]]  # value = {'IK_First': <InitKind.IK_First: 0>, 'IK_FirstTypedInit': <InitKind.IK_FirstTypedInit: 1>, 'IK_BitInit': <InitKind.IK_BitInit: 2>, 'IK_BitsInit': <InitKind.IK_BitsInit: 3>, 'IK_DagInit': <InitKind.IK_DagInit: 4>, 'IK_DefInit': <InitKind.IK_DefInit: 5>, 'IK_FieldInit': <InitKind.IK_FieldInit: 6>, 'IK_IntInit': <InitKind.IK_IntInit: 7>, 'IK_ListInit': <InitKind.IK_ListInit: 8>, 'IK_FirstOpInit': <InitKind.IK_FirstOpInit: 9>, 'IK_BinOpInit': <InitKind.IK_BinOpInit: 10>, 'IK_TernOpInit': <InitKind.IK_TernOpInit: 11>, 'IK_UnOpInit': <InitKind.IK_UnOpInit: 12>, 'IK_LastOpInit': <InitKind.IK_LastOpInit: 13>, 'IK_CondOpInit': <InitKind.IK_CondOpInit: 14>, 'IK_FoldOpInit': <InitKind.IK_FoldOpInit: 15>, 'IK_IsAOpInit': <InitKind.IK_IsAOpInit: 16>, 'IK_ExistsOpInit': <InitKind.IK_ExistsOpInit: 17>, 'IK_AnonymousNameInit': <InitKind.IK_AnonymousNameInit: 18>, 'IK_StringInit': <InitKind.IK_StringInit: 19>, 'IK_VarInit': <InitKind.IK_VarInit: 20>, 'IK_VarBitInit': <InitKind.IK_VarBitInit: 22>, 'IK_VarDefInit': <InitKind.IK_VarDefInit: 23>, 'IK_LastTypedInit': <InitKind.IK_LastTypedInit: 24>, 'IK_UnsetInit': <InitKind.IK_UnsetInit: 25>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class InitVector:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Init) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: InitVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> InitVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Init:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: InitVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Init]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: InitVector) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Init) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: InitVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Init) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Init) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: InitVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Init) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Init:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Init:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Init) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class IntInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getBit(self, arg0: int) -> Init:
        ...
    def getValue(self) -> int:
        ...
    def isConcrete(self) -> bool:
        ...
class IntRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class ListInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def empty(self) -> bool:
        ...
    def getAsString(self) -> str:
        ...
    def getBit(self, arg0: int) -> Init:
        ...
    def getElement(self, arg0: int) -> Init:
        ...
    def getElementAsRecord(self, arg0: int) -> Record:
        ...
    def getElementType(self) -> RecTy:
        ...
    def getValues(self) -> InitVector:
        ...
    def isComplete(self) -> bool:
        ...
    def isConcrete(self) -> bool:
        ...
    def size(self) -> int:
        ...
class ListRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getElementType(self) -> RecTy:
        ...
    def typeIsA(self, arg0: RecTy) -> bool:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class OpInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getNumOperands(self) -> int:
        ...
class RecTy:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getRecTyKind(self) -> RecTyKind:
        ...
    def getRecordKeeper(self) -> RecordKeeper:
        ...
    def typeIsA(self, arg0: RecTy) -> bool:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class RecTyKind:
    """
    Members:
    
      BitRecTyKind
    
      BitsRecTyKind
    
      IntRecTyKind
    
      StringRecTyKind
    
      ListRecTyKind
    
      DagRecTyKind
    
      RecordRecTyKind
    """
    BitRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.BitRecTyKind: 0>
    BitsRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.BitsRecTyKind: 1>
    DagRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.DagRecTyKind: 5>
    IntRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.IntRecTyKind: 2>
    ListRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.ListRecTyKind: 4>
    RecordRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.RecordRecTyKind: 6>
    StringRecTyKind: typing.ClassVar[RecTyKind]  # value = <RecTyKind.StringRecTyKind: 3>
    __members__: typing.ClassVar[dict[str, RecTyKind]]  # value = {'BitRecTyKind': <RecTyKind.BitRecTyKind: 0>, 'BitsRecTyKind': <RecTyKind.BitsRecTyKind: 1>, 'IntRecTyKind': <RecTyKind.IntRecTyKind: 2>, 'StringRecTyKind': <RecTyKind.StringRecTyKind: 3>, 'ListRecTyKind': <RecTyKind.ListRecTyKind: 4>, 'DagRecTyKind': <RecTyKind.DagRecTyKind: 5>, 'RecordRecTyKind': <RecTyKind.RecordRecTyKind: 6>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Record:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getDefInit(self) -> DefInit:
        ...
    def getFieldLoc(self, arg0: str) -> SMLoc:
        ...
    def getForwardDeclarationLocs(self) -> SMLocVector:
        ...
    def getID(self) -> int:
        ...
    def getLoc(self) -> SMLocVector:
        ...
    def getName(self) -> str:
        ...
    def getNameInit(self) -> Init:
        ...
    def getRecords(self) -> RecordKeeper:
        ...
    def getSuperClasses(self) -> SuperClassVector:
        ...
    def getTemplateArgs(self) -> InitVector:
        ...
    def getType(self) -> RecordRecTy:
        ...
    def getValue(self, arg0: str) -> RecordVal:
        ...
    def getValueAsBitsInit(self, arg0: str) -> BitsInit:
        ...
    def getValueAsListInit(self, arg0: str) -> ListInit:
        ...
    def getValueAsString(self, arg0: str) -> str:
        ...
    def getValueInit(self, arg0: str) -> Init:
        ...
    def getValues(self) -> RecordValVector:
        ...
    def isAnonymous(self) -> bool:
        ...
    @typing.overload
    def isSubClassOf(self, arg0: Record) -> bool:
        ...
    @typing.overload
    def isSubClassOf(self, arg0: str) -> bool:
        ...
    def isTemplateArg(self, arg0: Init) -> bool:
        ...
    def isValueUnset(self, arg0: str) -> bool:
        ...
    @property
    def isClass(self) -> bool:
        ...
class RecordKeeper:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    @typing.overload
    def getAllDerivedDefinitions(self, arg0: str) -> RecordVector:
        ...
    @typing.overload
    def getAllDerivedDefinitions(self, arg0: StringVector) -> RecordVector:
        ...
    @typing.overload
    def getAllDerivedDefinitions(self, *args) -> RecordVector:
        ...
    def getClass(self, arg0: str) -> Record:
        ...
    def getClasses(self) -> RecordMap:
        ...
    def getDef(self, arg0: str) -> Record:
        ...
    def getDefs(self) -> RecordMap:
        ...
    def getInputFilename(self) -> str:
        ...
class RecordMap:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> Record:
        ...
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator[str]:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: Record) -> None:
        ...
    def items(self) -> typing.ItemsView:
        ...
    def keys(self) -> typing.KeysView:
        ...
    def values(self) -> typing.ValuesView:
        ...
class RecordRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getClasses(self) -> RecordVector:
        ...
    def isSubClassOf(self, arg0: Record) -> bool:
        ...
    def typeIsA(self, arg0: RecTy) -> bool:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class RecordVal:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getName(self) -> str:
        ...
    def getNameInit(self) -> Init:
        ...
    def getType(self) -> RecTy:
        ...
    def getTypeName(self) -> str:
        ...
    def getValue(self) -> Init:
        ...
    def isTemplateArg(self) -> bool:
        ...
    def isUsed(self) -> bool:
        ...
class RecordValVector:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, s: slice) -> RecordValVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> RecordVal:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RecordValVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[RecordVal]:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: RecordVal) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RecordValVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: RecordVal) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: RecordValVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: RecordVal) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> RecordVal:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> RecordVal:
        """
        Remove and return the item at index ``i``
        """
class RecordVector:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Record) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: RecordVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> RecordVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Record:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: RecordVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Record]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: RecordVector) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Record) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: RecordVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Record) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Record) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: RecordVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Record) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Record:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Record:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Record) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class SMLoc:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getPointer(self) -> str:
        ...
    def isValid(self) -> bool:
        ...
class SMLocVector:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: SMLoc) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: SMLocVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> SMLocVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> SMLoc:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: SMLocVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[SMLoc]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: SMLocVector) -> bool:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: SMLoc) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: SMLocVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: SMLoc) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: SMLoc) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: SMLocVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: SMLoc) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> SMLoc:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> SMLoc:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: SMLoc) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class SMRange:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class StringFormat:
    """
    Members:
    
      SF_String
    
      SF_Code
    """
    SF_Code: typing.ClassVar[StringFormat]  # value = <StringFormat.SF_Code: 1>
    SF_String: typing.ClassVar[StringFormat]  # value = <StringFormat.SF_String: 0>
    __members__: typing.ClassVar[dict[str, StringFormat]]  # value = {'SF_String': <StringFormat.SF_String: 0>, 'SF_Code': <StringFormat.SF_Code: 1>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class StringInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getAsUnquotedString(self) -> str:
        ...
    def getFormat(self) -> StringFormat:
        ...
    def getValue(self) -> str:
        ...
    def isConcrete(self) -> bool:
        ...
class StringInitVector:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: StringInit) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StringInitVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StringInitVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> StringInit:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StringInitVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[StringInit]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StringInitVector) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: StringInit) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StringInitVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: StringInit) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: StringInit) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StringInitVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: StringInit) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> StringInit:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> StringInit:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: StringInit) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class StringRecTy(RecTy):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def typeIsConvertibleTo(self, arg0: RecTy) -> bool:
        ...
class StringVector:
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: str) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: StringVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> StringVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> str:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: StringVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[str]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: StringVector) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: str) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StringVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: str) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: str) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: StringVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: str) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> str:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> str:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: str) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class SuperClassVector:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, s: slice) -> SuperClassVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> tuple[Record, SMRange]:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: SuperClassVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[tuple[Record, SMRange]]:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: tuple[Record, SMRange]) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: SuperClassVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: tuple[Record, SMRange]) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    @typing.overload
    def extend(self, L: SuperClassVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: tuple[Record, SMRange]) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> tuple[Record, SMRange]:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> tuple[Record, SMRange]:
        """
        Remove and return the item at index ``i``
        """
class TernOpInit(OpInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLHS(self) -> Init:
        ...
    def getMHS(self) -> Init:
        ...
    def getOpcode(self) -> ...:
        ...
    def getRHS(self) -> Init:
        ...
class TypedInit(Init):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def classof(arg0: Init) -> bool:
        ...
    def getType(self) -> RecTy:
        ...
class UnOpInit(OpInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getOpcode(self) -> UnaryOp:
        ...
    def getOperand(self) -> Init:
        ...
class UnaryOp:
    """
    Members:
    
      CAST
    
      NOT
    
      HEAD
    
      TAIL
    
      SIZE
    
      EMPTY
    
      GETDAGOP
    """
    CAST: typing.ClassVar[UnaryOp]  # value = <UnaryOp.CAST: 0>
    EMPTY: typing.ClassVar[UnaryOp]  # value = <UnaryOp.EMPTY: 5>
    GETDAGOP: typing.ClassVar[UnaryOp]  # value = <UnaryOp.GETDAGOP: 6>
    HEAD: typing.ClassVar[UnaryOp]  # value = <UnaryOp.HEAD: 2>
    NOT: typing.ClassVar[UnaryOp]  # value = <UnaryOp.NOT: 1>
    SIZE: typing.ClassVar[UnaryOp]  # value = <UnaryOp.SIZE: 4>
    TAIL: typing.ClassVar[UnaryOp]  # value = <UnaryOp.TAIL: 3>
    __members__: typing.ClassVar[dict[str, UnaryOp]]  # value = {'CAST': <UnaryOp.CAST: 0>, 'NOT': <UnaryOp.NOT: 1>, 'HEAD': <UnaryOp.HEAD: 2>, 'TAIL': <UnaryOp.TAIL: 3>, 'SIZE': <UnaryOp.SIZE: 4>, 'EMPTY': <UnaryOp.EMPTY: 5>, 'GETDAGOP': <UnaryOp.GETDAGOP: 6>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UnsetInit(Init):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
class VarBitInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getBitNum(self) -> int:
        ...
    def getBitVar(self) -> Init:
        ...
class VarInit(TypedInit):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getAsString(self) -> str:
        ...
    def getName(self) -> str:
        ...
    def getNameInit(self) -> Init:
        ...
    def getNameInitAsString(self) -> str:
        ...
@typing.overload
def ParseTableGen(arg0: str) -> RecordKeeper:
    ...
@typing.overload
def ParseTableGen(arg0: str, arg1: StringVector) -> RecordKeeper:
    ...
@typing.overload
def ParseTableGen(arg0: str, arg1: StringVector, arg2: StringVector) -> RecordKeeper:
    ...
def getLLVMSourceLoc() -> str:
    ...
