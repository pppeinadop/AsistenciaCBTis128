create table public.attendance_records (
    attendance_date date not null,
    group_name text not null,
    student_registration text not null,
    student_name text not null,
    status text not null check (status in ('Presente', 'Falta')),
    recorded_by uuid not null default auth.uid() references auth.users(id),
    recorded_at timestamptz not null default now(),
    primary key (attendance_date, group_name, student_registration)
);

alter table public.attendance_records enable row level security;

create policy "Authenticated staff can read attendance"
on public.attendance_records for select
to authenticated
using (true);

create policy "Authenticated staff can create attendance"
on public.attendance_records for insert
to authenticated
with check (recorded_by = (select auth.uid()));

create policy "Authenticated staff can correct attendance"
on public.attendance_records for update
to authenticated
using (true)
with check (true);
