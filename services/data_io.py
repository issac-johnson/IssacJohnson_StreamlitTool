import polars as pl
import pandas as pd
from typing import Union, Dict, List

DFLike = Union[pl.LazyFrame, pl.DataFrame, pd.DataFrame]

def load_csv(file) -> tuple[pl.LazyFrame, None]:
    lf = pl.read_csv(file).lazy()
    return lf, None

def to_pandas(lf: pl.LazyFrame) -> pd.DataFrame:
    try:
        schema = lf.collect_schema()
    except Exception:
        schema = lf.collect().schema
    struct_cols = [col for col, dtype in schema.items() if isinstance(dtype, pl.Struct)]
    if struct_cols:
        print(f"Dropping struct columns: {struct_cols}")
        lf = lf.drop(struct_cols)
    return lf.collect().to_pandas()

def to_csv_bytes(df: pl.DataFrame) -> bytes:
    return df.write_csv().encode("utf-8")

def head(lf: pl.LazyFrame, n: int = 5) -> pl.DataFrame:
    return lf.limit(n).collect()

def ensure_lazy(df: DFLike) -> pl.LazyFrame:
    if isinstance(df, pl.LazyFrame):
        return df
    if isinstance(df, pl.DataFrame):
        return df.lazy()
    if isinstance(df, pd.DataFrame):
        return pl.from_pandas(df).lazy()
    raise TypeError("Unsupported df type")

def drop_na(lf: pl.LazyFrame, subset: List[str] | None = None) -> pl.LazyFrame:
    return lf.drop_nulls(subset=subset)

def drop_duplicates(lf: pl.LazyFrame, subset: List[str] | None = None) -> pl.LazyFrame:
    return lf.unique(subset=subset)

def convert_types(lf: pl.LazyFrame, casts: Dict[str, str]) -> pl.LazyFrame:
    return lf.with_columns([pl.col(k).cast(v) for k, v in casts.items()])

def normalize(lf: pl.LazyFrame, cols: List[str]) -> pl.LazyFrame:
    exprs = [(pl.col(c) - pl.col(c).mean()) / pl.col(c).std() for c in cols]
    return lf.with_columns(exprs)

def filter_rows(lf: pl.LazyFrame, expr: str) -> pl.LazyFrame:
    return lf.filter(eval(expr))
