from tablegen.legacy._Context import TableGenLoader
import os

def test_dump1():
    pre, ext = os.path.splitext(__file__)
    ctx = TableGenLoader().load(f'{pre}.td')
    with open("tmpB.td", "w") as f:
        f.write(ctx.__dump__())
    
    rectx= TableGenLoader().load('tmpB.td')
    assert ctx == rectx
    os.unlink("tmpB.td")
