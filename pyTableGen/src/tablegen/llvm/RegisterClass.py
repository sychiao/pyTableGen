from .SetTheory import SetTheory
from ..unit.record import TableGenRecord
from ..wrapper.recordkeeper import RecordKeeper
from typing import Iterable
from functools import lru_cache

class RegisterClassSet(SetTheory):
    
    def expandRegisterClass(self, member: TableGenRecord) -> Iterable[str]:
        return self.expand(member.MemberList)

    def expandRegister(self, member: TableGenRecord) -> Iterable[str]:
        return [member.defname]

    def expandRegisterTuples(self, member: TableGenRecord) -> Iterable[str]:
        if member.RegAsmNames:
            return member.RegAsmNames
        v = [self.expand(subReg) for subReg in member.SubRegs]
        return list("_".join(e) for e in zip(*v))

class CodeGenRegister:

    def __init__(self, recs: RecordKeeper):
        self.recs = recs
        self.regs = dict()
        self.handleRegisterClass()

    def handleRegisterClass(self):
        for regcls in self.recs.getDefs("RegisterClass"):
            self.regs[regcls.defname] = RegisterClassSet(self.recs).expand(regcls.MemberList)
    
    @lru_cache
    def getSubRegisterClass(self, regclsname: str | TableGenRecord) -> set[str]:
        if isinstance(regclsname, TableGenRecord):
            regclsname = regclsname.defname
        try:
            subregs = list()
            for subregclsname, regs in self.regs.items():
                if  regs.issubset(self.regs[regclsname]):
                    subregs.append(subregclsname)
            return set(subregs)
        except KeyError:
            raise ValueError(f"RegisterClass {regclsname} not found")