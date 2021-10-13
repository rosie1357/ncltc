def expand_range(codes):
    """
    Function expand_range to take in either one code or a range of codes to return the individual codes within range
    params:
        codes str: individual or range of values (as strings) - e.g. '99214' or '99214-99220'
        
    returns:
        list: either individual code in list or list with each individual expanded code
    """
    if not '-' in codes:
        return [codes]
        
    else:
        start, stop = codes.split('-')
        return [str(i) for i in range(int(start), int(stop) + 1)]