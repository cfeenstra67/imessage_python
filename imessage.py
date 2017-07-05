#!/usr/bin/env python3

import sqlite3
import os

with sqlite3.connect(os.path.expanduser('~/Library/Messages/chat.db')) as conn:
	cursor = conn.cursor()


	if __name__ == '__main__':
		cursor.execute('SELECT * FROM message')
		print(cursor.fetchall()[:10])