""" create timescaledb tables and continuous aggregates:
        - readings
        - direct_space_counts
        - inferred_space_counts
        - space_counts



Revision ID: 578752be4543
Revises: 1b91ec5245fc
Create Date: 2020-07-29 20:33:07.205120+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "578752be4543"
down_revision = "1b91ec5245fc"
branch_labels = None
depends_on = None


def upgrade():

    # defined in scripts/timescaledb_schemas.pgsql
    op.execute(
        """
        create table if not exists readings
        (
            id bigserial not null,
            dpu_id bigint
                constraint fk_readings_dpu_id_dpus
                    references dpus,
            timestamp timestamp with time zone not null,
            direction smallint not null,
            created_at timestamp with time zone default now(),
            updated_at timestamp with time zone default now()
        );

        create index if not exists ix_readings_updated_at
            on readings (updated_at);

        create index if not exists readings_timestamp_idx
            on readings (timestamp desc);

        create index if not exists readings_dpu_id_timestamp_idx
            on readings (dpu_id asc, timestamp desc);
    """
    )

    op.execute("SELECT create_hypertable('readings', 'timestamp');")
    op.execute(
        """
        create view direct_space_counts as
        select
            space_id,
            space,
            timestamp,
            sum(sum(direction)) over(order by timestamp)::int as count
        from (
        select
            timestamp,
            direction,
            spaces.name as space,
            spaces.id as space_id
        from readings r
        left join dpus d on r.dpu_id = d.id
        left join doorways d2 on d.doorway_id = d2.id
        left join spaces spaces on d2.ingress_space_id = spaces.id
            ) as space_count
        group by space_id, space, timestamp;
    """
    )
    op.execute(
        """
        create view inferred_space_counts as
        select
            space_id,
            space,
            timestamp,
            sum(sum(direction)) over(order by timestamp)::int as count
        from (
        select
            timestamp,
            direction * -1 as direction,
            spaces.name as space,
            spaces.id as space_id
        from readings r
        left join dpus d on r.dpu_id = d.id
        left join doorways d2 on d.doorway_id = d2.id
        left join spaces spaces on d2.egress_space_id = spaces.id
        where spaces.id is not null
            ) as space_count
        group by space_id, space, timestamp
        order by space_id, timestamp;
     """
    )
    op.execute(
        """
        create view space_counts as
        select
            space_id,
            space,
            timestamp,
            count
        from direct_space_counts
        union
        select
            space_id,
            space,
            timestamp,
            count
        from inferred_space_counts
        order by space_id, timestamp;
     """
    )


def downgrade():

    op.execute("drop view space_counts;")
    op.execute("drop view direct_space_counts;")
    op.execute("drop view inferred_space_counts;")
    op.execute("drop table readings cascade;")
