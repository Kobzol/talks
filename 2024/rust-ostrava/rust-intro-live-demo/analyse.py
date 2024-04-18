import gc
import glob

import pandas as pd
from tqdm import tqdm


# Data source: https://static.crates.io/db-dump.tar.gz
# Package download source: https://springernature.figshare.com/articles/dataset/Full_dataset/21345990?backTo=/collections/Evolving_Collaboration_Dependencies_and_Use_in_the_Rust_Open_Source_Software_Ecosystem/5983534
# lib.rs source: http://lib.rs/data/downloads_csv.zip
# https://hackaday.com/2019/03/07/make-xkcd-style-plots-from-python/


def create_crates_per_month():
    df = pd.read_csv("data/crates.csv")
    index = pd.to_datetime(df["created_at"])
    df.set_index(index, inplace=True)
    count_per_month = df.groupby([
        df.index.year,
        df.index.month
    ])["name"].count()
    accum_count_per_month = count_per_month.cumsum().reset_index(0).rename(
        columns=dict(created_at="year", name="count")).reset_index().rename(
        columns=dict(created_at="month")
    )
    accum_count_per_month["date"] = accum_count_per_month.apply(lambda r: f"{r['year']}-{r['month']}-01", axis=1)
    accum_count_per_month = accum_count_per_month[["date", "count"]]
    accum_count_per_month.to_csv("data/crates-per-month.csv", index=False)


def create_download_count():
    def aggregate(path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        if "downloaded_at" in df.columns:
            index = pd.to_datetime(df["downloaded_at"])
            df.set_index(index, inplace=True)
            df = df.resample("M")["downloads"].sum()
            df = df.cumsum().reset_index()
            df = df.rename(columns=dict(downloaded_at="date", downloads="count"))
        else:
            df = df.groupby("date")["downloads"].sum().cumsum().reset_index()
            df = df.rename(columns=dict(downloads="count"))
        return df

    df = aggregate("data/package_version_downloads.csv")
    gc.collect()
    max = df["count"].max()
    df2 = aggregate("data/version_downloads.csv")
    df2["count"] = df2["count"] + max

    df = pd.concat((df, df2))
    df.to_csv("data/crate-downloads-per-month.csv", index=False)


def create_download_count_librs():
    tables = []
    for file in tqdm(sorted(glob.glob("data/librs_crate_downloads/*.csv"))):
        df = pd.read_csv(file)
        df.drop(columns=["crate_name", "version"], inplace=True)
        df = df.fillna(0).transpose()
        df = df.sum(axis=1)
        df = df.reset_index()
        df = df.rename(columns={"index": "date", 0: "count"})
        tables.append(df)

    df = pd.concat(tables)
    df["count"] = df["count"].cumsum()
    df.to_csv("data/crate-downloads-per-month.csv", index=False)


# create_crates_per_month()
# create_download_count()
create_download_count_librs()
