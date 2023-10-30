import pandas as pd


# Data source: https://static.crates.io/db-dump.tar.gz
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
    df = pd.read_csv("data/package_version_downloads.csv")
    # df = pd.read_csv("data/downloads.csv")
    index = pd.to_datetime(df["downloaded_at"])
    df.set_index(index, inplace=True)
    df = df.resample("M")["downloads"].sum()
    df = df.cumsum().reset_index()
    df = df.rename(columns=dict(downloaded_at="date", downloads="count"))
    df.to_csv("data/crate-downloads-per-month.csv", index=False)


def create_start_count():
    df = pd.read_csv("data/rust-star-history-raw.csv", header=None)
    df["date"] = df[1]
    df["count"] = df[2]
    df = df[["date", "count"]]
    print(df)

# create_crates_per_month()
create_download_count()
# create_start_count()
