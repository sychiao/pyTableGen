class Base {
    int id = 0;
    string name = "";
}

class Object: Base {
    int value = 0;
    let id = 1;
    let name = "Object";
}

class Object2: Base {
    int value = 0;
    let id = 2;
    let name = "Object2";
}

class __Args_Instruction<string instname>  {
    string __Arg_Instruction_instname = instname;
}

class Instruction<string instname>: __Args_Instruction<instname>, Object {
    let id = 3;
    let name = "Instruction";
    string instruction = instname;
}
class __Args_XInstruction<string instname, int _id>  {
    string __Arg_XInstruction_instname = instname;
    int __Arg_XInstruction__id = _id;
}
// class XInstruction<string instname, int _id> : __Args_XInstruction<instname, !add(_id, 1)>, Instruction<instname>
class XInstruction<string instname, int _id>: __Args_XInstruction<instname, !add(_id, 1)>, Instruction<instname> {
    let id = _id;
    let name = "XInstruction";
    let instruction = instname;
    bit isX = 1;
}

def Value : Object2 {
    let id = 4;
    let name = "Value";
    let value = 1;
}

class Magic {
    int magic_num = 12;
}

def  : Instruction<"FA">, Magic;

def  Inst : XInstruction<"inst", 33>, Magic {
    let id = 5;
    int addition = 37;
}
