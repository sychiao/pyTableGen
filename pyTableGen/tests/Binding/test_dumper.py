from tablegen.Context import TableGenLoader
import os

def test_dump1():
    root = os.path.dirname(__file__)
    ctx = TableGenLoader().load(f'{root}/B.td')
    with open("tmpB.td", "w") as f:
        f.write(ctx.__dump__())

    rectx= TableGenLoader().load('tmpB.td')
    assert ctx == rectx
