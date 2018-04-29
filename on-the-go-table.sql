-- Chloe Blazey, Heidi Cho, Eliza McNair

drop table if exists purchaseItems;
drop table if exists purchase;
drop table if exists menu;
drop table if exists student;
drop table if exists distributor;

-- create a table for the distributors
create table distributor (
	did int(10) unsigned auto_increment,
	name varchar(30),
	primary key (did)
)
-- table constraint
ENGINE = InnoDB;

-- create a table for students
create table student (
	bnum int(10) unsigned,
	primary key (bnum),
	name varchar(30),
	username varchar(20),
	password char(60),
	admin int(10) unsigned,
	INDEX(admin),
	-- If the student isn't an admin, admin = NULL. Else, admin = distributor id
	foreign key (admin) references distributor (did) on delete set null
)
-- table constraint
ENGINE = InnoDB;

-- create a table for menu items
create table menu (
	mid int(10) unsigned not null auto_increment,
	primary key (mid),
	name varchar(30),
	price decimal(5,2) unsigned,
	distributor int(10) unsigned,
	description varchar(100),
	INDEX(distributor),
	foreign key (distributor) references distributor(did) on delete set null
)
-- table constraint
ENGINE = InnoDB;

-- create a table for orders
create table purchase (
	pid int(10) unsigned not null auto_increment,
	primary key (pid),
	student int(10) unsigned,
	distributor int(10) unsigned,
	complete int(1), -- if order is complete, complete = 1. Else complete = NULL
	INDEX(distributor),
	INDEX(student),
	foreign key (distributor) references distributor(did) on delete set null,
	foreign key (student) references student(bnum) on delete set null
)
-- table constraint
ENGINE = InnoDB;

-- create a table for the menu items in orders
create table purchaseItems (
	pid int(10) unsigned not null,
	mid int(10) unsigned not null,
	primary key (pid, mid),
	INDEX(pid),
	INDEX(mid),
	foreign key (pid) references purchase(pid),
	foreign key (mid) references menu(mid)
)
-- table constraint
ENGINE = InnoDB;

-- Distributors
INSERT INTO distributor (name) VALUES ('El Table');
INSERT INTO distributor (name) VALUES ('The Hoop');

-- Students
INSERT INTO student (bnum, name, username, password, admin)
VALUES ('20729654', 'Heidi Cho', 'hcho5', '1234567890', '1');
INSERT INTO student (bnum, name, username, password, admin)
VALUES ('20758475', 'Eliza McNair', 'emcnair', '1234567890', '1');
INSERT INTO student (bnum, name, username, password, admin)
VALUES ('20805803', 'Chloe Blazey', 'cblazey', '1234567890', '1');
INSERT INTO student (bnum, name, username, password)
VALUES ('20123456', 'Wendy Wellesley', 'wwellesley', '1234567890');

-- Menus
INSERT INTO menu (name, price, distributor, description)
VALUES ('El Table Club', '7.00', '1', 'bacon, turkey, avocado, tomato,
greens, provolone, and mayo on sourdough bread');
INSERT INTO menu (name, price, distributor, description)
VALUES ('ABCD', '5.50', '1', 'apple, bacon, cheddar, and dijon on wheat
bread');
INSERT INTO menu (name, price, distributor, description)
VALUES ('LGBLT', '4.50', '1', 'lettuce, bacon, tomato, and mayo on
sourdough bread');
INSERT INTO menu (name, price, distributor, description)
VALUES ('The Green Monstah', '5.50', '1', 'avocado, pesto, goat cheese,
provolone, and greens on sourdough bread');

-- Orders
INSERT INTO purchase (student, distributor) VALUES ('20729654', '1');

-- Order items
INSERT INTO purchaseItems (pid, mid) VALUES ('1', '1');
