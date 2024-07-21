class myRecord;

class myRecord {
  int x = 123;
}

class Base {
  string _name = "empty";
}

class Inst<int z> : Base {
  int Z = z;
  list<int> lst = [1, 2, 3];
}

class Template<int x> {
  int xx;
  int vv = x;
}

def rec1 : myRecord {
  int a = 1;
  int b = 2;
}

def rec2 : myRecord, Inst<123> {
  int a = 2;
  bit b = 0b1;
}

def XX {
  dag x  = (rec2 1, 2, 3);
}

def YY : Inst<3>;
