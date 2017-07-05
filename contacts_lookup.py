import sqlite3
import os

def _db_path():
	base = os.path.expanduser('~/Library/Application Support/AddressBook/Sources')
	foldername = [name for name in os.listdir(base) if name[0] != '.'][0]
	dbname = 'AddressBook-v22.abcddb'
	return os.path.join(base, foldername, dbname)

def number_format_strings(country_code=True):
	codes = [
		'({ac}) {f3}-{l4}',
		'{ac}{f3}{l4}'
	]
	if country_code:
		codes.extend([
				'{cc}{ac}{f3}{l4}',
				'{cc} ({ac}) {f3}-{l4}',
			])
	return codes

def possible_formats(phone_number):
	if (phone_number[0] == '#' or phone_number[0] == '*' or len(phone_number) < 10): return [phone_number]
	parts = {'cc': ''}
	if len(phone_number) > 10:
		parts['cc'] = phone_number[:-10]
		phone_number = phone_number[2:]
	parts['ac'] = phone_number[:3]
	parts['f3'] = phone_number[3:6]
	parts['l4'] = phone_number[6:]
	return [format_string.format(**parts) for format_string in number_format_strings(len(parts['cc']) > 0)]

with sqlite3.connect(_db_path()) as conn:
	curs = conn.cursor()
	def lookup_id(phone_number):
		results = []
		for formatted_num in possible_formats(phone_number):
			curs.execute('SELECT ZOWNER FROM ZABCDPHONENUMBER WHERE ZFULLNUMBER=?', (formatted_num,))
			results.extend(curs.fetchall())
		return [result for (result,) in results][0] if len(results) > 0 else None
	def lookup_name_id(unique_id):
		curs.execute('SELECT ZFIRSTNAME, ZLASTNAME, ZNICKNAME FROM ZABCDRECORD WHERE Z_PK=?', (unique_id,))
		return curs.fetchall()[0] if len(results) > 0 else None
	def lookup_name(phone_number):
		first, last, nickname = lookup_name_id(lookup_id(phone_number))
		return {'first': first, 'last': last, 'nickname': nickname}