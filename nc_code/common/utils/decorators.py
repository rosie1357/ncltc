

def add_attrib(cls):
    """
    function add_attrib to be used to decorate class to add method get_attrib()
    
    """
    
    def get_attrib(self, key, default):
        """
        function get_attrib to return value of key IF exists as attrib on class instance, otherwise default
        params:
            key: name of key to attempt to return (attribute of class instance)
            default: default value to return if not exists on instance
        """
    
        return self.__dict__.get(key) or default
    
    setattr(cls, 'get_attrib', get_attrib)
    return cls