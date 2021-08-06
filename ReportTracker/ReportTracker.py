from myfitnesspal import Client
import xlwings as xw
from pandas import to_datetime

from src.main.python.ingress import MyFitnessPal

OUTPUT_LOC = "A8"
USER_NAME_LOC = "B3"
START_DATE_LOC = "B5"
END_DATE_LOC = "B6"


client = Client("Shawnfit1987", password="@Baichidemima1")


def main():
    workbook = xw.Book.caller()
    active_sheet = workbook.sheets.active
    if active_sheet.name == "_xlwings.conf":
        raise RuntimeError("This is a protected sheet.")
    start_date = to_datetime(active_sheet.range(START_DATE_LOC).value)
    end_date = to_datetime(active_sheet.range(END_DATE_LOC).value)
    user_name = active_sheet.range(USER_NAME_LOC).value
    mfp = MyFitnessPal(
        client=client,
        start_date=start_date,
        end_date=end_date,
        user_name=user_name,
    )
    active_sheet.range(OUTPUT_LOC).options(
        index=False, dtype=None
    ).value = mfp.get_nutrition_summary_dataframe()


if __name__ == "__main__":
    xw.Book("ReportTracker.xlsm").set_mock_caller()
    main()
