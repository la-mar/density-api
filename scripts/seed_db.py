# from pathlib import Path


import asyncio
from typing import Dict, List

import pandas as pd

import loggers
from db import db
from db.models import DPU, Doorway, Model, Reading, Space
from util.jsontools import to_string

loggers.config(30)


async def seed_model(model: Model, records: List[Dict]) -> List[Dict]:
    objs: List[Model] = await asyncio.gather(*[model.merge(**x) for x in records])
    return [x.to_dict() for x in objs]


async def seed_models():

    await db.startup()

    df: pd.DataFrame = pd.read_csv("docs/dpu_data.csv")

    spaces = await seed_model(model=Space, records=[{"name": "A"}, {"name": "B"}])
    print(f"spaces={to_string(spaces)}\n")
    spaces_df = pd.DataFrame(spaces).set_index("name")

    doorway_records = [
        {"name": "X", "ingress_space_id": spaces_df.loc["A"].id},
        {
            "name": "Z",
            "ingress_space_id": spaces_df.loc["A"].id,
            "egress_space_id": spaces_df.loc["B"].id,
        },
    ]
    doorways = await seed_model(model=Doorway, records=doorway_records)
    print(f"doorways={to_string(doorways)}\n")

    doorway_df = pd.DataFrame(doorways).set_index("name")
    doorway_df = doorway_df.where(doorway_df.notnull(), None)

    df.dpu_id.unique()
    dpu_records = [
        {"id": 283, "doorway_id": doorway_df.loc["X"].id},
        {"id": 423, "doorway_id": doorway_df.loc["Z"].id},
    ]

    dpus = await seed_model(model=DPU, records=dpu_records)
    print(f"dpus={to_string(dpus)}\n")

    df.timestamp = pd.to_datetime(df.timestamp)
    reading_count = await Reading.bulk_insert(df.to_dict(orient="records"))
    print(f"{reading_count=}\n")

    print("Done!")


def run():
    asyncio.run(seed_models())


if __name__ == "__main__":

    run()
