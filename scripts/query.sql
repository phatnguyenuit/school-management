-- Show users
select id, name, email, updated_at from public.user
where email = 'phatnt.uit@gmail.com'

-- Delete all users
delete from public.user
where email != 'phatnt.uit@gmail.com'


-- Get total users
select count(id) from public.user
