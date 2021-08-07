from time import sleep
from myfitnesspal import Client
import xlwings as xw
from pandas import to_datetime

from src.main.python.ingress import MyFitnessPal

MY_ACCOUNT_NAME_LOC = "B1"
MY_ACCOUNT_PASSWORD_LOC = "B2"
MY_ACCOUNT_SETTINGS_SHEET_NAME = "My Account Settings"

OUTPUT_LOC = "A8"
USER_NAME_LOC = "B3"
START_DATE_LOC = "B5"
END_DATE_LOC = "B6"


def get_my_account_client(workbook):
    try:
        sheet = workbook.sheets[MY_ACCOUNT_SETTINGS_SHEET_NAME]
        return Client(
            username=sheet.range(MY_ACCOUNT_NAME_LOC).value,
            password=sheet.range(MY_ACCOUNT_PASSWORD_LOC).value,
        )
    except Exception:
        raise ValueError("Invalid My Account Settings.") from None


def get_inputs_from_sheet(active_sheet):
    try:
        return (
            to_datetime(active_sheet.range(START_DATE_LOC).value),
            to_datetime(active_sheet.range(END_DATE_LOC).value),
            active_sheet.range(USER_NAME_LOC).value,
        )
    except Exception:
        raise ValueError("Invalid input(s) or wrong input location(s).") from None


def main():
    workbook = xw.Book.caller()
    active_sheet = workbook.sheets.active
    if active_sheet.name == "_xlwings.conf":
        raise RuntimeError("This is a protected sheet.")
    start_date, end_date, user_name = get_inputs_from_sheet(active_sheet)
    print(f"Start fetching data for {user_name} between {start_date} and {end_date}...")
    mfp = MyFitnessPal(
        client=get_my_account_client(workbook),
        start_date=start_date,
        end_date=end_date,
        user_name=user_name,
    )
    active_sheet.range(OUTPUT_LOC).options(
        index=False, dtype=None
    ).value = mfp.get_nutrition_summary_dataframe()
    print("Success!")
    sleep(1)

if __name__ == "__main__":
    xw.Book("ReportTracker.xlsm").set_mock_caller()
    main()
