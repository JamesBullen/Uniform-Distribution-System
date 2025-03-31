create database UniformDistributionDB;
use UniformDistributionDB;


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
foreign key(role_id) references tbl_roles(role_id) on delete cascade on update cascade
);

create table tbl_orders(
order_id int not null primary key auto_increment,
order_number int not null,
staff_id int not null,
item_id int not null,
colour_id int,
size varchar(3) not null,
quantity int not null,
bought bool not null,
order_date date not null,
reissue_date date,
constraint staff_id foreign key(staff_id) references tbl_staff(staff_id) on delete cascade on update cascade,
foreign key(item_id) references tbl_uniforms(item_id) on delete cascade on update cascade,
foreign key(colour_id) references tbl_colours(colour_id) on delete cascade on update cascade
);


-- Procedure Creation
delimiter $$
create procedure AddNewStaff(in fullnameInput varchar(40), in sexInput varchar(1), in roleInput int, in hoursInput int)
begin
insert into tbl_staff(fullname, sex, role_id, hours) values (fullnameInput, sexInput, roleInput, hoursInput);
-- to-do: create orders for uniform based off of role, sex, and hours worked
end $$

create procedure PurchaseUniform(in orderInput int, in staffInput int, in itemInput int, in colourInput int, in sizeInput varchar(3), in quantityInput int, in boughtInput bool)
begin
insert into tbl_orders(order_number, staff_id, item_id, colour_id, size, quantity, bought, order_date, reissue_date) values
(orderInput, staffInput, itemId, colourInput, sizeInput, quantityInput, boughtInput, cast(getdate() as date), if(boughtInput=1, dateadd(year, 2, cast(getdate() as date)), null));
end $$

delimiter ;


-- Table Insertion
insert into tbl_roles(role_name) values
('Doctors'),
('Nurses'),
('Health Care Assistants'),
('Housekeeping'),
('Porters'),
('Therapists'),
('Receptionists');

insert into tbl_colours(colour) values
('blue'),
('pink'),
('green'),
('grey'),
('brown'),
('lilac'),
('multicolour');

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
select * from tbl_roles; -- S01_C10 to C-10 and S02_C1 to C10
select * from tbl_colours;
select * from tbl_sizes;
select * from tbl_suppliers;
select * from tbl_uniforms;
select * from tbl_allocations;
select * from tbl_staff;
select * from tbl_orders;