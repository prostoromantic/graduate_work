import pandas
import sqlite3


data = []
file = pandas.ExcelFile('database.xlsx')
for sheet in file.sheet_names:
    df = pandas.read_excel('database.xlsx', sheet_name=sheet)
    for value in df.values:
        if str(value[0]) != 'nan' and str(value[1]) != 'nan' and str(value[2]) != 'nan' and str(value[3]) != 'nan' and str(value[4]) != 'nan':
            data.append([
                sheet, value[0], value[1], value[2], value[3], value[4], value[5], value[6]
            ])


db = sqlite3.connect('database.sqlite3')
cursor = db.cursor()

for value in data:
    cursor.execute('SELECT * FROM mainpage_counties WHERE county_name == ?', (value[1],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO mainpage_counties VALUES (?, ?)', (None, value[1],))
db.commit()

counties = {}
cursor.execute('SELECT * FROM mainpage_counties')
for value in cursor.fetchall():
    counties[value[1]] = value[0]


for value in data:
    cursor.execute('SELECT * FROM mainpage_material WHERE material_name == ?', (value[0],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO mainpage_material VALUES (?, ?)', (None, value[0],))
db.commit()

materials = {}
cursor.execute('SELECT * FROM mainpage_material')
for value in cursor.fetchall():
    materials[value[1]] = value[0]


for value in data:
    cursor.execute('SELECT * FROM mainpage_fabricator WHERE county_name_id == ? AND material_name_id == ? AND fabricator_name == ? AND location == ?',
                   (counties[value[1]], materials[value[0]], value[2], value[3],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO mainpage_fabricator VALUES (?, ?, ?, ?, ?)',
                       (None, value[2], value[3], counties[value[1]], materials[value[0]]))
db.commit()

fabricators = {}
cursor.execute('SELECT * FROM mainpage_fabricator')
for value in cursor.fetchall():
    fabricators[value[1]] = {value[3]: {value[4]: value[0]}}


for value in data:
    try:
        cursor.execute('SELECT * FROM mainpage_statistic WHERE revenue == ? AND indicative_forces == ? AND workers == ? AND county_id == ? AND fabricator_id == ? AND material_id == ?',
               (value[4], value[5], value[6], counties[value[1]], fabricators[value[2]][counties[value[1]]][materials[value[0]]], materials[value[0]],))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO mainpage_statistic VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                None, value[4], value[5], value[6], None, value[7], counties[value[1]], fabricators[value[2]][counties[value[1]]][materials[value[0]]], materials[value[0]],
            ))
    except Exception as error:
        print(error)
        print('O')


db.commit()
cursor.close()
db.close()