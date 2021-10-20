from dateutil.parser import parserinfo, parser
import pandas as pd

class parserinfo_century(parserinfo):
    """
    class parserinfo_century to update date parser to set 2-digit years to
    specific century (20th or 21st) based on 2-digit year of '21' cutoff,
    i.e. any 2-digit year between 22 and 99 will be set as 1922 - 1999, respectively,
         and any 2-digit year between 0 and 21 will be set as 2000 - 2021, respectively.
    
    """
    def convertyear(self, year, century_specified=False):
        if not century_specified:
            if 21 < year < 100:
                year += 1900
            elif year < 100:
                year += 2000
        return year

def parse_century(timestr, **kwargs):
    """
    Function parse_century to apply parserinfo_century class to parser and return date with 4-digit year as defined above
    """
    return parser(parserinfo_century()).parse(timestr, **kwargs)


def attempt_parse(value, return_raw=False):
    """
    Function attempt_parse to attempt to parse a field to a date, otherwise return empty date or raw value
    params:
        value str/date
        return_raw bool: if set to False (default), will return pd.NaT (missing datetime)
            if set to True will return raw value

    returns:
        value as date if parses else input value
    """

    try:
        return parser.parse(value)
    except:
        if return_raw:
            return value
        else:
            return pd.NaT