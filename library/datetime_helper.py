import datetime

import pytz
import dateutil.parser as dtp
import datetime as dt


class DateTimeHelper:
    @classmethod
    def add_tz(cls, datetime: dt.datetime, tz=pytz.utc):
        udatetime = datetime.replace(tzinfo=tz)
        return udatetime

    @classmethod
    def dt_from_string(cls, dt_str: str, tz=pytz.utc):
        if dt_str is None:
            return None
        datetime = dtp.parse(dt_str)
        udatetime = cls.add_tz(datetime, tz=tz)
        return udatetime

    @classmethod
    def now_datetime_to_string(cls):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')