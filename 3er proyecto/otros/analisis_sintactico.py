import sintactico
import types

ar = [sintactico.__dict__.get(a) for a in dir(sintactico) if isinstance(sintactico.__dict__.get(a), types.FunctionType)]

print ar[5].__name__
