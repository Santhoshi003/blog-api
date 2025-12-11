import sys
print("cwd (sys.path[0]) =", sys.path[0])
try:
    import app
    print("import app OK")
except Exception as e:
    print("IMPORT ERROR:", repr(e))
