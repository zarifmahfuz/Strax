from datetime import datetime

def get_date(timestamp):
    """
        Constructs a date object in ISO 8601 format.

        Parameters:
            timestamp (str): datetime string in ISO 8601 format e.g. 2018-11-13T20:20:39+00:00

        Returns:
            dt (datetime.datetime): datetime object
    """
    formatter = "%Y-%m-%dT%H:%M:%S%z"
    dt = datetime.strptime(timestamp, formatter)
    return dt

timestamp = "2022-01-13T20:20:39+00:00"
print(get_date(timestamp))