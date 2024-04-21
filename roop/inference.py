import core

try:
    core.run()
except Exception as e:
    raise Exception("Error: error in core run file " + str(e))