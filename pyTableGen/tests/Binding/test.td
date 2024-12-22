class A {
    int a = 1;
    bits<4> b = 13;
}

def xA : A;

class B {
    int a = 1;
    bits<4> b = 12;
    bit c = 1;
    list<int> x = [1, 2, 3];
    dag y =(xA 1, 2, 3);
}
