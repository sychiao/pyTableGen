import foo

ret = foo.ParseTableGen("A.td")
print(ret.getClass("Record").getName())
