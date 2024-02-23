import sqlite3

conn = sqlite3.connect('myApp.db')
cur = conn.cursor()

print ("Opened database successfully")

conn.execute('''CREATE TABLE CLIENT
	(id		INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
	name		TEXT,
	phone		TEXT,
	address		TEXT
	);''')

conn.execute('''CREATE TABLE SELLER
	(id		INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
	name		TEXT,
	phone		TEXT,
	email		TEXT
	);''')

conn.execute('''CREATE TABLE PRODUCT
	(id		INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
	name		TEXT,
	code		TEXT,
	price		REAL,
	warehouse	TEXT
	);''')

conn.execute('''CREATE TABLE DEVICE
	(id		INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
	serial		TEXT,
	name		TEXT,
	ipv6		TEXT,
	lastreport	TEXT,
	swver		TEXT,
	devtype		TEXT,
	devrole		TEXT
	);''')

print ("Table created successfully")

#############################
# Insert Data into table CLIENT
#############################

client = [
        {'id':1, 'name': 'Atomuli Yadalato', 'phone': '+5010674373431', 'address': 'Syracuse, 2528  Oak Street'},
        {'id':2, 'name': 'Sovseiduri Oherachu', 'phone': '+2290504407434', 'address': '2671  Oakmound Drive'},
        {'id':3, 'name': 'Matzal Cats', 'phone': '+387664683394', 'address': '2172  Ella Street'},
        {'id':4, 'name': 'Yatasuka Nakomode', 'phone': '+380504457494', 'address': '163  Moore Avenue'},
        {'id':5, 'name': 'Fire-Bow de Bleu', 'phone': '+359504467844', 'address': '3813  Kenwood Place'},
        {'id':6, 'name': 'Hans Trachenbürger', 'phone': '+210504455773', 'address': '1008  Broadway Avenue'},
        {'id':7, 'name': 'Bzdashek Zapadlovsky', 'phone': '+2265046234714', 'address': '1083  Woodland Terrace'},
        {'id':8, 'name': 'Thanos Slyunidopolu', 'phone': '+6840504670154', 'address': '2529  Briarhill Lane'},
        {'id':9, 'name': 'Kheranuka Poroyalu', 'phone': '+855504456780', 'address': '4751  Corbin Branch Road'},
        {'id':10, 'name': 'Ushat Pomoev', 'phone': '+235504453457', 'address': '1960  Gore Street'},
        {'id':11, 'name': 'Harem Playboys', 'phone': '+357504462859', 'address': '81  Monroe Avenue'},
        {'id':12, 'name': 'Marazmus Nolemotsiy', 'phone': '+620506379083', 'address': '1245  Duff Avenue'},
        {'id':13, 'name': 'Orido Pota', 'phone': '+200567890432', 'address': '2091  Braxton Street'},
        {'id':14, 'name': 'Olivier Ju yes Swallow', 'phone': '+500453268901', 'address': '4940  Chardonnay Drive'},
        {'id':15, 'name': 'Rucishchito Shirehari', 'phone': '+3585345628972', 'address': '4069  Austin Secret Lane'},
        {'id':16, 'name': 'Stoyana Rakova', 'phone': '+490345246783', 'address': '349  Bombardier Way'},
        {'id':17, 'name': 'Spiro Napolnasrakis', 'phone': '+955412324306', 'address': '130  Smithfield Avenue'},
	{'id':18, 'name': 'Helga Schlucher', 'phone': '+910564738018', 'address': '1199  State Street'}
]

for item in client:
	SQL = 'INSERT INTO CLIENT (id, name, phone, address) VALUES({0}, "{1}", "{2}", "{3}")'.format(item['id'], item['name'], item['phone'], item['address'])
	cur.execute(SQL)

print ("Table 'CLIENT' is done")

#############################
# Insert Data into table SELLER
#############################

seller = [
	{'id':1, 'name': 'Paula Anderson', 'phone': '+5010674373431', 'email': 'paula@gggmail.com'},
	{'id':2, 'name': 'Sibostyan Polin', 'phone': '+2290504407434', 'email': 'polin@gggmail.com'},
	{'id':3, 'name': 'Jhon Malberg', 'phone': '+387664683394', 'email': 'malberg@gggmail.com'},
	{'id':4, 'name': 'Yakuha Manu', 'phone': '+380504457494', 'email': 'manu@gggmail.com'},
	{'id':5, 'name': 'Bella Krakovich', 'phone': '+359504467844', 'email': 'krakovich@gggmail.com'}
]

for item in seller:
	SQL = 'INSERT INTO SELLER (id, name, phone, email) VALUES({0}, "{1}", "{2}", "{3}")'.format(item['id'], item['name'], item['phone'], item['email'])
	cur.execute(SQL)

print ("Table 'SELLER' is done")

#############################
# Insert Data into table PRODUCT
#############################

product = [
	{'id':1, 'name': 'Support shaft assembly', 'code': '106743734317', 'price': 356.30, 'warehouse': '1'},
	{'id':2, 'name': 'Arow plate', 'code': '789798734317', 'price': 1356.00, 'warehouse': '1'},
	{'id':3, 'name': 'Square-ended shaft', 'code': '65448917', 'price': 755.50, 'warehouse': '1'},
	{'id':4, 'name': 'Gland flange', 'code': '45646734317', 'price': 112.70, 'warehouse': '1'},
	{'id':5, 'name': 'Bearing bushing', 'code': '46546434317', 'price': 56.80, 'warehouse': '2'},
	{'id':6, 'name': 'V-ring packing', 'code': '32131734317', 'price': 552.17, 'warehouse': '1'},
	{'id':7, 'name': 'Support shaft assembly', 'code': '10098980317', 'price': 386.30, 'warehouse': '1'},
	{'id':8, 'name': 'Arow plate', 'code': '79809809809', 'price': 856.00, 'warehouse': '1'},
	{'id':9, 'name': 'Square-ended shaft', 'code': '09808917', 'price': 655.50, 'warehouse': '2'},
	{'id':10, 'name': 'Gland flange', 'code': '43543517', 'price': 162.50, 'warehouse': '2'},
	{'id':11, 'name': 'Bearing bushing', 'code': '0980717', 'price': 156.88, 'warehouse': '1'},
	{'id':12, 'name': 'V-ring packing', 'code': '654564654734317', 'price': 172.47, 'warehouse': '1'},
	{'id':13, 'name': 'Support shaft assembly', 'code': '564654734317', 'price': 256.18, 'warehouse': '2'},
	{'id':14, 'name': 'Arow plate', 'code': '987798734317', 'price': 156.50, 'warehouse': '1'},
	{'id':15, 'name': 'Square-ended shaft', 'code': '789789978917', 'price': 355.45, 'warehouse': '1'},
	{'id':16, 'name': 'Gland flange', 'code': '6575666686734317', 'price': 12.70, 'warehouse': '2'},
	{'id':17, 'name': 'Bearing bushing', 'code': '08798746434317', 'price': 67.70, 'warehouse': '1'},
	{'id':18, 'name': 'V-ring packing', 'code': '7600131734317', 'price': 132.23, 'warehouse': '1'},
]

for item in product:
	SQL = 'INSERT INTO PRODUCT (id, name, code, price, warehouse) VALUES({0}, "{1}", "{2}", {3}, "{4}")'.format(item['id'], item['name'], item['code'], item['price'], item['warehouse'])
	cur.execute(SQL)

print ("Table 'PRODUCT' is done")

device = [
	{'id':1, 'serial': '1345234234', 'name': 'Room 10 t. sensor', 'ipv6': 'fda1:98ec:3c8d:a291:167:99e1:b956:56b7', 'lastreport': '2024-02-23 10:14:06', 'swver': 'v0.0.1', 'devtype': 'tmp sensor', 'devrole': 'child'},
	{'id':2, 'serial': '0345289093', 'name': 'Room 11 t. sensor', 'ipv6': 'fda1:98ec:3c8d:a291:167:99e1:b956:56b8', 'lastreport': '2024-02-23 10:14:26', 'swver': 'v0.0.1', 'devtype': 'tmp sensor', 'devrole': 'child'},
	{'id':3, 'serial': '1564366776', 'name': 'Hallway clock', 'ipv6': 'fda1:98ec:3c8d:a291:167:99e1:b956:56b9', 'lastreport': '2024-02-23 10:10:15', 'swver': 'v0.0.3', 'devtype': 'dig. clock', 'devrole': 'router'},
]

for item in device:
	SQL = 'INSERT INTO DEVICE (id, name, serial, ipv6, lastreport, swver, devtype, devrole) VALUES({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}")'\
		.format(item['id'], item['name'], item['serial'], item['ipv6'], item['lastreport'], item['swver'], item['devtype'], item['devrole'])
	cur.execute(SQL)

print ("Table 'DEVICE' is done")

conn.commit()

print ("Commit is done")

conn.close()

print ("Database is closed")
print ("Good luck!")
