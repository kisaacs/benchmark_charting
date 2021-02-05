import datetime
import json
import sqlite3
import uuid


class ChartingDataModel:
    def __init__(self):
        self.database_name = "test"
        self.connection = None
        self.cursor = None
        self.open_database()
        self.create_benchmark_log_table()
        self.create_settings_table()
        self.close_database()

    def open_database(self):
        self.connection = sqlite3.connect(self.database_name + ".db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()

    def close_database(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def create_table_if_not_exist(self, table_name, schema):
        self.cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
        if self.cursor.fetchone()[0] == 1:
            print(table_name + ' table exists.')
            return False
        self.cursor.execute("CREATE TABLE " + table_name + " (" + schema + ")")
        print(table_name + ' table does not exist.')
        return True

    def create_benchmark_log_table(self):
        return self.create_table_if_not_exist("benchmark_log",
                                              "uuid        VARCHAR(40) PRIMARY KEY, "
                                              "create_time TIMESTAMP, "
                                              "user        VARCHAR(40) DEFAULT NULL, "
                                              "m_flag      INT DEFAULT 0,"
                                              "table_id    VARCHAR(200) DEFAULT NULLs")

    def create_settings_table(self):
        return self.create_table_if_not_exist("settings",
                                              "uuid  VARCHAR(40) PRIMARY KEY, "
                                              "key   VARCHAR(40), "
                                              "value TEXT DEFAULT NULL")

    def add_settings(self, key, value):
        self.open_database()
        # if self.cursor.execute("SELECT 1 FROM settings WHERE key = '" + key + "'").fetchone():
        #     self.cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
        # else:
        self.cursor.execute("INSERT INTO settings VALUES (?,?,?)", (str(uuid.uuid4()), key, value))
        self.close_database()

    def add_new_datapoint(self, c_id, platform=None):
        self.open_database()
        n_uid = str(uuid.uuid4())
        t_uid = str(uuid.uuid4())
        user = "admin"
        self.cursor.execute("INSERT INTO benchmark_log (uuid, create_time, table_id) VALUES (?,?,?,?)",
                            (n_uid, datetime.datetime.now(), t_uid))
        self.close_database()
        return t_uid

    def update_log(self, n_uid=None, user=None, m_flag=0):
        self.open_database()
        if n_uid is None:
            n_uid = str(uuid.uuid4())
        t_uid = str(uuid.uuid4())
        self.cursor.execute("REPLACE INTO benchmark_log (uuid, create_time, user, m_flag, table_id) VALUES (?,?, ?,?,?)",
                            (n_uid, datetime.datetime.now(), user, m_flag, t_uid))
        self.close_database()
        return n_uid, t_uid


class ChartingDataManager:
    def __init__(self, u=None):
        self.log_id = None
        self.create_time = None
        self.user = u
        self.m_flag = 0
        self.table_id = None

    def update_log_values(self, db):
        self.log_id, self.table_id = db.update_log(m_flag=self.m_flag)
        print(self.log_id)
        print(self.table_id)

    def add_new_measurements(self, db, param_list, flag):
        self.m_flag = flag
        for i, param in enumerate(param_list):
            for v in param["values"]:
                db.add_settings(param["name"], v)
        self.update_log_values(db)

