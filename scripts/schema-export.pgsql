-- Raw DDL export for information only

-- Tables

create table if not exists public.spaces
(
	id bigserial not null
		constraint pk_spaces
			primary key,
	name varchar(100) not null
		constraint uq_spaces_name
			unique,
	created_at timestamp with time zone default now(),
	updated_at timestamp with time zone default now()
);

alter table public.spaces owner to density;

create index if not exists ix_spaces_updated_at
	on public.spaces (updated_at);

create table if not exists public.doorways
(
	id bigserial not null
		constraint pk_doorways
			primary key,
	name varchar(100) not null
		constraint uq_doorways_name
			unique,
	ingress_space_id bigint
		constraint fk_doorways_ingress_space_id_spaces
			references public.spaces,
	egress_space_id bigint
		constraint fk_doorways_egress_space_id_spaces
			references public.spaces,
	created_at timestamp with time zone default now(),
	updated_at timestamp with time zone default now()
);

alter table public.doorways owner to density;

create index if not exists ix_doorways_updated_at
	on public.doorways (updated_at);

create table if not exists public.dpus
(
	id bigserial not null
		constraint pk_dpus
			primary key,
	doorway_id bigint
		constraint fk_dpus_doorway_id_doorways
			references public.doorways,
	created_at timestamp with time zone default now(),
	updated_at timestamp with time zone default now()
);

alter table public.dpus owner to density;

create index if not exists ix_dpus_updated_at
	on public.dpus (updated_at);

create table if not exists public.readings
(
	id bigserial not null,
	dpu_id bigint
		constraint fk_readings_dpu_id_dpus
			references public.dpus,
	timestamp timestamp with time zone not null,
	direction smallint not null,
	created_at timestamp with time zone default now(),
	updated_at timestamp with time zone default now()
);

alter table public.readings owner to density;

create index if not exists ix_readings_updated_at
	on public.readings (updated_at);

create index if not exists readings_timestamp_idx
	on public.readings (timestamp desc);

create index if not exists readings_dpu_id_timestamp_idx
	on public.readings (dpu_id asc, timestamp desc);


SELECT create_hypertable('readings', 'timestamp');


-- Sequences
create sequence public.spaces_id_seq;

alter sequence public.spaces_id_seq owner to density;

create sequence public.doorways_id_seq;

alter sequence public.doorways_id_seq owner to density;

create sequence public.dpus_id_seq;

alter sequence public.dpus_id_seq owner to density;

create sequence public.readings_id_seq;

alter sequence public.readings_id_seq owner to density;


--  Views

create or replace view public.direct_space_counts(space_id, space, timestamp, count) as
	select
    space_count.space_id,
    space_count.space,
    space_count."timestamp",
    sum(sum(space_count.direction)) over (order by space_count."timestamp") as count
from (select
          r."timestamp",
          r.direction,
          spaces.name as space,
          spaces.id as space_id
      from readings r
               left join dpus d on r.dpu_id = d.id
               left join doorways d2 on d.doorway_id = d2.id
               left join spaces spaces on d2.ingress_space_id = spaces.id) space_count
group by space_count.space_id, space_count.space, space_count."timestamp";

alter table public.direct_space_counts owner to density;

create or replace view public.inferred_space_counts(space_id, space, timestamp, count) as
	select
    space_count.space_id,
    space_count.space,
    space_count."timestamp",
    sum(sum(space_count.direction)) over (order by space_count."timestamp") as count
from (select
          r."timestamp",
          r.direction * '-1'::integer as direction,
          spaces.name as space,
          spaces.id as space_id
      from readings r
               left join dpus d on r.dpu_id = d.id
               left join doorways d2 on d.doorway_id = d2.id
               left join spaces spaces on d2.egress_space_id = spaces.id
      where spaces.id is not null) space_count
group by space_count.space_id, space_count.space, space_count."timestamp"
order by space_count.space_id, space_count."timestamp";

alter table public.inferred_space_counts owner to density;

create or replace view public.space_counts(space_id, space, timestamp, count) as
	select
    direct_space_counts.space_id,
    direct_space_counts.space,
    direct_space_counts."timestamp",
    direct_space_counts.count
from direct_space_counts
union
select
    inferred_space_counts.space_id,
    inferred_space_counts.space,
    inferred_space_counts."timestamp",
    inferred_space_counts.count
from inferred_space_counts
order by 1, 3;

alter table public.space_counts owner to density;
