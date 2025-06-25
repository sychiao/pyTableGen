class A <int _x> {
    int x = _x;
}

class B <int _y> {
    int y = _y;
}

class Box<int a, int b> : A<a>, B<b> {
    int value = !add(a, b);
}

class C<string name> {
    string n = name;
}

class CBox<string n> :C<n>, Box<1, 2>;

