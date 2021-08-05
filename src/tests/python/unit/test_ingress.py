from datetime import datetime
import pytest
import myfitnesspal as mfp
from pandas import DataFrame
from ingress import MyFitnessPal

START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2021, 1, 3)
USER_NAME = "test_user"


@pytest.fixture(name="mock_client")
def get_mock_client(mocker):
    client = mocker.MagicMock(spec=mfp.Client)
    mock_day = mocker.MagicMock(totals={"foo": "bar"})
    client.get_date.return_value = mock_day
    yield client


@pytest.fixture(name="mock_myfitnesspal")
def get_mock_myfitnesspasl(mock_client):
    yield MyFitnessPal(mock_client, USER_NAME, START_DATE, END_DATE)


def test_date_range(mock_myfitnesspal):
    date_range = mock_myfitnesspal.date_range
    assert isinstance(date_range, list)
    assert len(date_range) == 3
    assert date_range[0] == datetime(2021, 1, 1)
    assert date_range[1] == datetime(2021, 1, 2)
    assert date_range[2] == datetime(2021, 1, 3)


def test_get_nutrition_summary_dataframe(mock_myfitnesspal):
    result = mock_myfitnesspal.get_nutrition_summary_dataframe()
    assert isinstance(result, DataFrame)
    assert result.to_dict() == {
        "Date": {
            0: datetime(2021, 1, 1),
            1: datetime(2021, 1, 2),
            2: datetime(2021, 1, 3),
        },
        "foo": {0: "bar", 1: "bar", 2: "bar"},
    }
