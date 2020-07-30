""" Database table definitions

NOTE: A doorway could likely hold 0, 1, or more sensors, on one or both sides
      of the doorway, in the real world.  I will assume a doorway can only
      hold 0 or 1 sensor for the context of this problem.
"""


# flake8: noqa
from db.models.bases import Base, BaseTable, db

Model = Base


class Space(BaseTable):
    __tablename__ = "spaces"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    uq_name = db.UniqueConstraint("name")


class Doorway(BaseTable):
    __tablename__ = "doorways"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    ingress_space_id = db.Column(db.ForeignKey("spaces.id"))
    egress_space_id = db.Column(db.ForeignKey("spaces.id"))
    uq_name = db.UniqueConstraint("name")


class DPU(BaseTable):
    "Density Processing Units (DPUs) table"
    __tablename__ = "dpus"
    id = db.Column(db.BigInteger, primary_key=True)
    doorway_id = db.Column(db.ForeignKey("doorways.id"))


class Reading(BaseTable):
    __tablename__ = "readings"
    id = db.Column(db.BigInteger, autoincrement=True)
    dpu_id = db.Column(db.ForeignKey("dpus.id"))
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    direction = db.Column(db.SmallInteger(), nullable=False)
    direction_check = db.CheckConstraint(
        "direction = -1 OR direction = 1", name="direction_check"
    )


class SpaceCount(Base):
    __tablename__ = "space_counts"

    space_id = db.Column(db.BigInteger)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    count = db.Column(db.Integer(), nullable=False)
