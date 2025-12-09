import pymysql # type: ignore

pymysql.install_as_MySQLdb()

import MySQLdb # type: ignore
setattr(MySQLdb, 'version_info', (2, 2, 6, 'final', 0))
MySQLdb.__version__ = '2.2.6'