from typing import List
from copy import deepcopy
from datetime import datetime

from pandas import date_range, DataFrame
import myfitnesspal as mfp


class MyFitnessPal:
    def __init__(
        self,
        client: mfp.Client,
        user_name: str,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        self.client = client
        self.user_name = user_name
        self.start_date = start_date
        self.end_date = end_date

    @property
    def date_range(self) -> List[datetime]:
        dates = list(date_range(start=self.start_date, end=self.end_date, freq="D"))
        return [date.to_pydatetime() for date in dates]

    def get_nutrition_summary_dataframe(self) -> DataFrame:
        summary = []
        for date in self.date_range:
            totals = self.client.get_date(date, user_name=self.user_name).totals
            totals_copy = deepcopy(totals)
            totals_copy.update({"Date": date})
            summary.append(totals_copy)
        df_summary = DataFrame(
            summary,
            columns=[
                "Date",
                "protein",
                "fat",
                "carbohydrates",
                "sodium",
                "sugar",
                "calories",
            ],
        )
        formated_columns = {str(col): str(col).title() for col in df_summary.columns}
        df_summary = df_summary.rename(columns=formated_columns).fillna(0)
        return df_summary
