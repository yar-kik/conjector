import datetime
import pytest

from app_properties import properties


@pytest.fixture
def datetime_class_fixt(request):
    @properties(filename=request.param, root="datetime")
    class DatetimeClass:
        timestamp_datetime_var: datetime.datetime
        keywords_datetime_var: datetime.datetime
        position_datetime_var: datetime.datetime
        text_datetime_var: datetime.datetime

    return DatetimeClass


@pytest.fixture
def date_class_fixt(request):
    @properties(filename=request.param, root="datetime")
    class DateClass:
        keywords_date_var: datetime.date
        position_date_var: datetime.date
        text_date_var: datetime.date

    return DateClass


@pytest.fixture
def time_class_fixt(request):
    @properties(filename=request.param, root="datetime")
    class TimeClass:
        keywords_time_var: datetime.time
        position_time_var: datetime.time
        text_time_var: datetime.time

    return TimeClass


@pytest.fixture
def timedelta_class_fixt(request):
    @properties(filename=request.param, root="datetime")
    class TimedeltaClass:
        keywords_timedelta_var: datetime.timedelta

    return TimedeltaClass


@pytest.mark.parametrize(
    "datetime_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_datetime_field(datetime_class_fixt):
    assert datetime_class_fixt.timestamp_datetime_var == datetime.datetime(
        year=2022, month=12, day=10, hour=20, minute=56, second=24
    )
    assert datetime_class_fixt.keywords_datetime_var == datetime.datetime(
        year=2022, month=12, day=10, hour=22, minute=43, second=0
    )
    assert datetime_class_fixt.position_datetime_var == datetime.datetime(
        year=2022, month=12, day=10, hour=22, minute=44, second=20
    )
    assert datetime_class_fixt.text_datetime_var == datetime.datetime(
        year=2022, month=12, day=10, hour=22, minute=44, second=56
    )


@pytest.mark.parametrize(
    "date_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_date_field(date_class_fixt):
    assert date_class_fixt.keywords_date_var == datetime.date(
        year=2022, month=11, day=11
    )
    assert date_class_fixt.position_date_var == datetime.date(
        year=2022, month=10, day=20
    )
    assert date_class_fixt.text_date_var == datetime.date(
        year=2022, month=11, day=24
    )


@pytest.mark.parametrize(
    "time_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_time_field(time_class_fixt):
    assert time_class_fixt.keywords_time_var == datetime.time(
        hour=2, minute=3, second=0
    )
    assert time_class_fixt.position_time_var == datetime.time(
        hour=10, minute=23, second=20
    )
    assert time_class_fixt.text_time_var == datetime.time(
        hour=8, minute=49, second=56
    )


@pytest.mark.parametrize(
    "timedelta_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_timedelta_field(timedelta_class_fixt):
    assert timedelta_class_fixt.keywords_timedelta_var == datetime.timedelta(
        days=1, hours=12, minutes=42, seconds=34, weeks=1
    )


@pytest.mark.parametrize(
    "filename",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
)
def test_wrong_datetime_value(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="datetime")
        class WrongDatetimeClass:
            wrong_datetime_var: datetime.datetime

    with pytest.raises(ValueError):

        @properties(filename=filename, root="datetime")
        class WrongDateClass:
            wrong_date_var: datetime.date

    with pytest.raises(ValueError):

        @properties(filename=filename, root="datetime")
        class WrongTimeClass:
            wrong_time_var: datetime.time

    with pytest.raises(ValueError):

        @properties(filename=filename, root="datetime")
        class WrongTimedeltaClass:
            wrong_timedelta_var: datetime.timedelta
