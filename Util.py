
DEFAULT_START_DATE, DEFAULT_END_DATE = 19800101, 20991231

def parse_date(date, asList=False):
    """ Return the YYYY, MM, DD parts of a date as strings """
    date_as_string = str(int(date))
    parsed_date = (date_as_string[:4], date_as_string[4:6], date_as_string[6:])
    if asList: parsed_date = list(parsed_date)
    return parsed_date