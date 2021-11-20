import cx_Oracle

ip = 'localhost'
port = 1521
SID = 'XE'
username = 'sys'
password = 'labii'
dsn = cx_Oracle.makedsn(ip, port, SID)
