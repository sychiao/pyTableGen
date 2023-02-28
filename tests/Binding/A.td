class myRecord {
  int x = 123;
}

class Base {
  string _name = "empty";
}

class Inst : Base {
  int Z = 123;
  list<int> lst = [1, 2, 3];
}

def rec1 : myRecord {
  int a = 1;
  int b = 2;
}

def rec2 : myRecord, Inst {
  int a = 2;
  bit b = 0b1;
}

def XX ;

def YY : Inst;
