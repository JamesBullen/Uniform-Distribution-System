create database Uniform_Distribution_DB;
use Uniform_Distribution_DB;


-- Table Creation
create table tbl_roles(
role_id int not null primary key auto_increment,
role_name varchar(40)
);

create table tbl_colours(
colour_id int not null primary key auto_increment,
colour varchar(11) not null
);

create table tbl_sizes(
sizes_id int not null primary key auto_increment,
sizes varchar(40) not null
);

create table tbl_suppliers(
supplier_id int not null primary key auto_increment,
supplier_name varchar(40) not null,
address varchar(60) not null,
phone varchar(12) not null,
email varchar(320) not null
);

create table tbl_uniforms(
item_id int not null primary key auto_increment,
item_name varchar(40) not null,
sex varchar(1) not null,
sizes_id int not null,
supplier_id int not null,
constraint sizes_id foreign key(sizes_id) references tbl_sizes(sizes_id) on delete cascade on update cascade,
constraint supplier_id foreign key(supplier_id) references tbl_suppliers(supplier_id) on delete cascade on update cascade
);

create table tbl_allocations(
allocation_id int not null primary key auto_increment,
role_id int not null,
item_id int not null,
colour_id int,
quantity int not null,
constraint role_id foreign key(role_id) references tbl_roles(role_id) on delete cascade on update cascade,
constraint item_id foreign key(item_id) references tbl_uniforms(item_id) on delete cascade on update cascade,
constraint colour_id foreign key(colour_id) references tbl_colours(colour_id) on delete cascade on update cascade
);

create table tbl_staff(
staff_id int not null primary key auto_increment,
fullname varchar(40) not null,
sex varchar(1) not null,
role_id int not null,
hours int not null,
foreign key(role_id) references tbl_roles(role_id) on delete cascade on update cascade,
check (hours >= 0)
);

create table tbl_orders(
order_id int not null primary key auto_increment,
order_number int not null,
staff_id int not null,
item_id int not null,
colour_id int,
size varchar(3) not null,
quantity int not null,
bought bit(1) not null,
order_date date not null,
reissue_date date,
constraint staff_id foreign key(staff_id) references tbl_staff(staff_id) on delete cascade on update cascade,
foreign key(item_id) references tbl_uniforms(item_id) on delete cascade on update cascade,
foreign key(colour_id) references tbl_colours(colour_id) on delete cascade on update cascade,
check (order_number > 0),
check (quantity > 0)
);


-- Procedure Creation
delimiter $$
create procedure AddStaff(in fullnameInput varchar(40), in sexInput varchar(1), in roleInput int, in hoursInput int)
begin
insert into tbl_staff(fullname, sex, role_id, hours) values (fullnameInput, sexInput, roleInput, hoursInput); -- Adds new staff to table
select max(staff_id) from tbl_staff; -- Returns id of added staff
end $$

create procedure RetireStaff(in staffInput int)
begin
delete from tbl_staff where staff_id = staffInput;
end $$

create procedure AllocatedUniform(in sexInput varchar(1), in roleInput int, in hoursInput int)
begin
select item_name, a.item_id, a.colour_id, sizes_id, ceiling(quantity*(hoursInput/40)) -- Returns needed uniform for interface to loop through to create orders
from tbl_allocations as a
join tbl_uniforms as u on a.item_id = u.item_id
where a.role_id = roleInput and (u.sex = sexInput or u.sex = 'U');
end $$

create procedure NextOrderNumber()
begin
select max(order_number)+1 from tbl_orders;
end $$

create procedure FindStaff(in roleInput int)
begin
select staff_id, fullname, sex, hours from tbl_staff
where role_id = roleInput;
end $$

create procedure PurchaseUniform(in orderInput int, in staffInput int, in itemInput int, in colourInput int, in sizeInput varchar(3), in quantityInput int, in boughtInput bool, in prevOrderInput int) -- Adds uniform item to orders table
begin
insert into tbl_orders(order_number, staff_id, item_id, colour_id, size, quantity, bought, order_date, reissue_date) values
(orderInput, staffInput, itemInput, colourInput, sizeInput, quantityInput, boughtInput, cast(now() as date), if(boughtInput=0, date_add(cast(now() as date), interval 2 year), null));
if prevOrderInput > 0 then
update tbl_orders set reissue_date = null where order_id = prevOrderInput;
end if;
end $$

create procedure AvailableReissues() -- Shows uniforms available for reissues, may also remove as may be more efficient to replace id's with there values in the interface rather than joining tables
begin
select order_id, o.staff_id, o.item_id, o.colour_id, order_number as 'Order', fullname as 'Full Name', ifnull(concat(colour, ' ', item_name), item_name) as 'Uniform', size as 'Size', quantity as 'Quantity'
from tbl_orders as o
join tbl_staff as s on o.staff_id = s.staff_id
join tbl_uniforms as u on o.item_id = u.item_id
left join tbl_colours as c on o.colour_id = c.colour_id
where reissue_date <= cast(now() as date) and bought = 0;
end $$

create procedure StaffInfo(in rowsInput int) -- Returns only the relevant data when displayign staff in GUI
begin
select fullname as 'Full Name', role_name as 'Role', hours as 'Hours'
from tbl_staff as s
join tbl_roles as r on s.role_id = r.role_id
where staff_id >= rowsInput
order by staff_id;
end $$

create procedure OrderInfo(in rowsInput int)
begin
select order_number as 'Order', fullname as 'Full Name', ifnull(concat(colour, ' ', item_name), item_name) as 'Uniform', size as 'Size', quantity as 'Quantity', supplier_name as 'Supplier', order_date as 'Ordered On', reissue_date as 'Reissue Date'
from tbl_orders as o
join tbl_staff as s on o.staff_id = s.staff_id
left join tbl_colours as c on o.colour_id = c.colour_id
join tbl_uniforms as u on o.item_id = u.item_id
join tbl_suppliers as su on u.supplier_id = su.supplier_id
where order_id >= rowsInput
order by order_id;
end $$

create procedure MostOrdered()
begin
select ifnull(concat(colour, ' ', item_name), item_name) as 'Uniform', supplier_name as 'Supplier', sum(quantity) as 'Quantity'
from tbl_orders as o
left join tbl_colours as c on o.colour_id = c.colour_id
join tbl_uniforms as u on o.item_id = u.item_id
join tbl_suppliers as s on u.supplier_id = s.supplier_id
group by item_name, colour, supplier_name
order by sum(quantity) desc;
end $$

create procedure StaffStatistics()
begin
select role_name as 'Role', count(staff_id) as 'Employed'
from tbl_staff as s
join tbl_roles as r on s.role_id = r.role_id
group by role_name with rollup;
end $$

create procedure AllocationTable()
begin
select role_name as 'Role', ifnull(concat(colour, ' ', item_name), item_name) as 'Uniform', sizes as 'Size Options', quantity as 'Max Quantity', supplier_name as 'Supplier'
from tbl_allocations as a
join tbl_roles as r on a.role_id = r.role_id
join tbl_uniforms as u on a.item_id = u.item_id
left join tbl_colours as c on a.colour_id = c.colour_id
join tbl_sizes as s on u.sizes_id = s.sizes_id
join tbl_suppliers as su on u.supplier_id = su.supplier_id
order by role_name;
end $$

create procedure SupplierInfo()
begin
select supplier_name as 'Supplier', address as 'Address', phone as 'Phone', email as 'Email'
from tbl_suppliers;
end $$
delimiter ;


-- Table Insertion
insert into tbl_roles(role_name) values
('Doctor'),
('Nurse'),
('Health Care Assistant'),
('Housekeeping'),
('Porter'),
('Therapist'),
('Receptionist');

insert into tbl_colours(colour) values
('Blue'),
('Pink'),
('Green'),
('Grey'),
('Brown'),
('Lilac'),
('Multicolour');

insert into tbl_sizes(sizes) values
('XXS,XS,S,M,L,XL,XXL,3XL,4XL,5XL'),
('S,M,L,XL,XXL,3XL,4XL,5XL'),
('XXS,XS,S,M,L,XL,XXL,3XL'),
('ONE');

insert into tbl_suppliers(supplier_name, address, phone, email) values
('Bridges', 'Unit 3, Newland Rise, Bamton BM5 3PP', '01995654654', 'sales@bridges.uf.uk'),
('Fashion Lab', 'Old Barn, Heath Maltings, Ennerdale EN17 5PX', '01488132465', 'sales@fashionlab.uk'),
('Ferrôme', 'Rue de Rivoli, 19552 Gonesse, France', '033539782072', 'sales@ferrome.fr'),
('InMotion', 'Unit 26, Acer Business Park, Haven HV3 3GQ', '06578301453', 'sales@inmotion.co.uk'),
('Lofts', 'Battleflats, Priest Moor Road, Cowper Coppice CP6 2BV', '03469265120', 'sales@lofts.org'),
('Therapist One', '26 Lees Holt, Heathfield HF2 0RL', '04516653343', 'sales@tpo.uk');

insert into tbl_uniforms(item_name, sex, sizes_id, supplier_id) values
('White coat', 'U', 1, 1),
('V Neck Tunic', 'F', 1, 3),
('Scrub T shirt', 'M', 1, 3),
('Trousers', 'U', 1, 3),
('Fleece', 'U', 2, 5),
('V Neck Tunic', 'F', 1, 6),
('Scrub T shirt', 'M', 1, 6),
('Trousers', 'U', 1, 6),
('Blouse', 'F', 3, 4),
('HHS Neckerchief Bib', 'F', 4, 2),
('Shirt', 'M', 2, 4),
('HHS Tie', 'F', 4, 2);

insert into tbl_allocations(role_id, item_id, colour_id, quantity) values
(1, 1, null, 3), (1, 2, 1, 5), (1, 3, 1, 3), (1, 4, 1, 5), (1, 5, 1, 1), -- Doctors
(2, 2, 2, 5), (2, 3, 2, 5), (2, 4, 2, 5), (2, 5, 2, 1), -- Nurses
(3, 2, 3, 5), (3, 3, 3, 5), (3, 4, 3, 5), (3, 5, 3, 1), -- HCA
(4, 2, 4, 5), (4, 3, 4, 5), (4, 4, 4, 5), (4, 5, 4, 2), -- HK
(5, 2, 5, 5), (5, 3, 5, 5), (5, 4, 5, 5), (5, 5, 5, 2), -- Porters
(6, 6, 6, 5), (6, 7, 6, 5), (6, 8, 6, 5), (6, 5, 6, 1), -- Therapists
(7, 9, 7, 5), (7, 10, null, 2), (7, 11, 7, 5), (7, 12, null, 2); -- Receptionists


-- Test Cases

-- Procedures
select * from tbl_roles; -- For S01, S02, S03, S04, S05, S06
select * from tbl_colours;
select * from tbl_sizes;
select * from tbl_suppliers;
select * from tbl_uniforms;
select * from tbl_allocations;
select * from tbl_staff;
select * from tbl_orders;

call AddNewStaff('James Bullen', 'M', 1, 40); -- For P01, P04, P09
call AddNewStaff('Matilda Carboni', 'F', 6, 8);

call LastAddedStaff(); -- For P02, & P05

call PurchaseUniform(1, 1, 1, null, 'XS', 3, 0); -- For P03, P06, P07
call PurchaseUniform(2, 1, 1, null, 'XS', 3, 1);
select * from tbl_orders where order_id = (select max(order_id) from tbl_orders);

truncate table tbl_orders; -- P08, P11, P20
call AvailableReissues();
insert into tbl_orders(order_number, staff_id, item_id, colour_id, size, quantity, bought, order_date, reissue_date) values (1, 1, 2, 1, 'S', 1, 0, '2000-12-12', '2002-12-12');
insert into tbl_orders(order_number, staff_id, item_id, colour_id, size, quantity, bought, order_date, reissue_date) values (1, 1, 1, null, 'S', 1, 0, '2000-12-12', '2030-12-12');

call AddStaff('James Bullen', 'M', 1, 40); -- For P09
call AddStaff('Matilda Carboni', 'F', 6, 8);

call PurchaseUniform(1, 1, 1, null, 'XS', 3, 0, 0); -- For P10
call PurchaseUniform(2, 1, 1, null, 'XS', 3, 1, 0);
call PurchaseUniform(2, 1, 1, null, 'XS', 3, 1, 1);
select * from tbl_orders where order_id = (select max(order_id) from tbl_orders);

call RetireStaff(9); -- P12
select * from tbl_staff;

call AllocatedUniform('M', 1, 40); -- P13
call AllocatedUniform('F', 1, 40);
call AllocatedUniform('M', 2, 40);
call AllocatedUniform('M', 2, 8);

call nextOrderNumber(); -- P14

call AddStaff('Matilda Carboni', 'F', 6, 8); -- P15
call StaffInfo(1);
call StaffInfo(2);

call OrderInfo(1); -- P16
call OrderInfo(2);

call MostOrdered(); -- P17

call StaffStatistics(); -- P18

call AllocationTable(); -- P19

call FindStaff(1); -- P21
call AddStaff('Nurse', 'F', 2, 16);
call FindStaff(2);

-- Integridy
call AddNewStaff('Mister James Robert Bullen of Watford, son of Mister Alistair Michael Bullen of Banham', 'M', 1, 40); -- For I01
call AddNewStaff('James Bullen', 'Male', 1, 40);
call AddNewStaff('James Bullen', 'M', 100, 40);
call AddNewStaff('James Bullen', 'M', 1, 400);
call AddNewStaff('James Bullen', 'M', -1, 40);
call AddNewStaff('James Bullen', 'M', 1, -1);
call AddNewStaff('James Bullen', 'M', 0, 40);
call AddNewStaff('James Bullen', 'M', 1, 0);
call AddNewStaff(10, 'M', 1, 40);
call AddNewStaff('James Bullen', 10, 1, 40);
call AddNewStaff('James Bullen', 'M', 'one', 40);
call AddNewStaff('James Bullen', 'M', 1, 'forty');
call AddNewStaff('James Bullen', 'M', '1', 40);
call AddNewStaff(null, 'M', 1, '40');
call AddNewStaff('James Bullen', null, 1, 40);
call AddNewStaff('James Bullen', 'M', null, 40);
call AddNewStaff('James Bullen', 'M', 1, null);

call PurchaseUniform(100, 1, 1, 1, 'XS', 3, 0); -- For I02
call PurchaseUniform(1, 100, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 100, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 100, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XXXS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 100, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 3, 100);
call PurchaseUniform(-1, 1, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, -1, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, -1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, -1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', -1, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 3, -1);
call PurchaseUniform(0, 1, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 0, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 0, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 0, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 0, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 3, 0);
call PurchaseUniform('one', 1, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 'one', 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 'one', 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 'one', 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, 3, 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 'three', 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 3, 'zero');
call PurchaseUniform(null, 1, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, null, 1, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, null, 1, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, null, 'XS', 3, 0);
call PurchaseUniform(1, 1, 1, 1, null, 3, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', null, 0);
call PurchaseUniform(1, 1, 1, 1, 'XS', 3, null);
call PurchaseUniform(1, 1, 1, 1, 'Hi', 3, 0);

call AddStaff('Mister James Robert Bullen of Watford, son of Mister Alistair Michael Bullen of Banham', 'M', 1, 40); -- I03
call AddStaff('James Bullen', 'Male', 1, 40);
call AddStaff('James Bullen', 'M', 100, 40);
call AddStaff(1, 'M', 1, 40);
call AddStaff('James Bullen', 1, 1, 40);
call AddStaff('James Bullen', 'M', 'one', 40);
call AddStaff('James Bullen', 'M', 1, 'forty');
call AddStaff(null, 'M', 1, 40);
call AddStaff('James Bullen', null, 1, 40);
call AddStaff('James Bullen', 'M', null, 40);
call AddStaff('James Bullen', 'M', 1, null);

call RetireStaff(10); -- I04
call RetireStaff('one');
call RetireStaff(null);

call AllocatedUniform('Male', 1, 40); -- I05
call AllocatedUniform('M', 100, 40);
call AllocatedUniform('M', 'one', 40);
call AllocatedUniform('M', 1, 'forty');
call AllocatedUniform(null, 1, 40);
call AllocatedUniform('M', null, 40);
call AllocatedUniform('M', 1, null);

call FindStaff(100); -- I06
call FindStaff('one');
call FindStaff(null);

call PurchaseUniform(1, 10, 2, 1, 'XS', 1, 0, 0); -- For I07
call PurchaseUniform(1, 1, 20, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, 2, 100, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XXXS', 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, 3, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, 0, 10);
call PurchaseUniform('one', 1, 2, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 'one', 2, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, 'two', 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 1, 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 'one', 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, 'zero', 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, 0, 'zero');
call PurchaseUniform(null, 1, 2, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, null, 2, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, null, 1, 'XS', 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, null, 1, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', null, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, null, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 1, 0, null);

call StaffInfo(10); -- I08
call StaffInfo('one');
call StaffInfo(null);

call OrderInfo(10);  -- I09
call OrderInfo('one');
call OrderInfo(null);


-- Fetch
set profiling = 1;
show profiles;
call AddStaff('James Bullen', 'M', 1, 40);
call RetireStaff(500);
call AllocatedUniform('M', 1, 40);
call NextOrderNumber();
call FindStaff(rand()*(7-1)+1);
call PurchaseUniform(1, 1, 2, 1, 'XS', 3, 0, 0);
call PurchaseUniform(1, 1, 2, 1, 'XS', 3, 0, rand()*(100-1)+1);
call AvailableReissues();
call StaffInfo(1);
call OrderInfo(1);
call MostOrdered();
call StaffStatistics();
call AllocationTable();
call SupplierInfo();