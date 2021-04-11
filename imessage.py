#!/usr/bin/env python3

import sqlite3
import os
from contacts_lookup import lookup_name
from pprint import pprint
from datetime import datetime

with sqlite3.connect(os.path.expanduser('~/Library/Messages/chat.db')) as conn:
	curs = conn.cursor()
	def _get_phonenum(handle_id):
		curs.execute('SELECT id FROM handle WHERE ROWID=?', (handle_id,))
		results = curs.fetchall()
		return [result for (result,) in results][0] if len(results) > 0 else None
	def get_unread():
		curs.execute('SELECT text, handle_id, date FROM message WHERE (is_read=0 AND is_from_me=0 AND is_empty=0 AND is_delivered=1)')
		default_val = 'UNKNOWN'
		for text, handle_id, date in curs.fetchall():
			phone_number = _get_phonenum(handle_id) or default_val
			print(phone_number)
			name = lookup_name(phone_number) or default_val
			yield {'name': name, 'phone_number': phone_number, 'text': text}

	if __name__ == '__main__':
		pprint([*get_unread()])
