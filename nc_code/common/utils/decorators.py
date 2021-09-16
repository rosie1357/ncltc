
import types

class copyattributes(object):
    """
    class copyattributes to copy attributes from passed class and add to decorated class
    
    """
    def __init__(self, source):
        self.source = source

    def __call__(self, target):
        for attr, value in self.source.__dict__.items():
            if attr.startswith('__'):
                continue
            if isinstance(value, (property, types.FunctionType)):
                continue
            setattr(target, attr, value)
        return target