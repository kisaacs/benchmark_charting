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
        self.create_charts_table()
        self.create_data_points_table()
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

    def create_charts_table(self):
        return self.create_table_if_not_exist("charts",
                                              "uuid         VARCHAR(40)  PRIMARY KEY, "
                                              "create_time  TIMESTAMP    NOT NULL, "
                                              "user         VARCHAR(40)  DEFAULT NULL, "
                                              "chart_name   VARCHAR(200) DEFAULT NULL, "
                                              "x_title      VARCHAR(200) DEFAULT NULL, "
                                              "y_title      VARCHAR(200) DEFAULT NULL, "
                                              "legends      VARCHAR(200) DEFAULT NULL")

    def create_data_points_table(self):
        return self.create_table_if_not_exist("data_points",
                                              "uuid        VARCHAR(40) PRIMARY KEY, "
                                              "chart_id    VARCHAR(40),"
                                              "create_time TIMESTAMP, "
                                              "platform    VARCHAR(200) DEFAULT NULL, "
                                              "x_value     VARCHAR(200) DEFAULT NULL, "
                                              "y_value     VARCHAR(200) DEFAULT NULL, "
                                              "legends     TEXT DEFAULT NULL, "
                                              "FOREIGN KEY(chart_id) REFERENCES charts(uuid)")

    def create_settings_table(self):
        return self.create_table_if_not_exist("settings",
                                              "key   VARCHAR(40), "
                                              "value TEXT DEFAULT NULL")

    def add_settings(self, key, value):
        self.open_database()
        if self.cursor.execute("SELECT 1 FROM settings WHERE key = '" + key + "'").fetchone():
            self.cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
        else:
            self.cursor.execute("INSERT INTO settings VALUES (?,?)", (key, value))
        self.close_database()

    def create_chart(self, name, x_title=None, y_title=None, legends=None, n_uid=None, user=None):
        self.open_database()
        if n_uid is None:
            n_uid = str(uuid.uuid4())
        self.cursor.execute("REPLACE INTO charts (uuid, create_time, user, chart_name, x_title, y_title, legends) VALUES (?,?, ?,?, ?,?,?)",
                            (n_uid, datetime.datetime.now(), user, name, x_title, y_title, legends))
        self.close_database()
        return n_uid

    def add_new_datapoint(self, c_id, platform=None):
        self.open_database()
        n_uid = str(uuid.uuid4())
        self.cursor.execute("INSERT INTO data_points (uuid, chart_id, create_time, platform) VALUES (?,?,?,?)",
                            (n_uid, c_id, datetime.datetime.now(), platform))
        self.close_database()
        return n_uid

    def update_datapoint_x(self, c_id, value):
        self.open_database()
        if self.cursor.execute("SELECT 1 FROM data_points WHERE chart_id = '" + c_id + "'").fetchone():
            self.cursor.execute("UPDATE data_points SET x_value = ? WHERE chart_id = ?", (value, c_id))
        else:
            n_uid = str(uuid.uuid4())
            self.cursor.execute("INSERT INTO data_points (uuid, chart_id, create_time, x_value) VALUES (?,?,?,?)",
                                (n_uid, c_id, datetime.datetime.now(), value))
        self.close_database()

    def update_datapoint_y(self, c_id, value):
        self.open_database()
        self.cursor.execute("UPDATE data_points SET y_value = ? WHERE chart_id = ?", (value, c_id))
        self.close_database()

    def update_datapoint_legends(self, c_id, key, value, end=None, interval=None):
        if interval is None:
            interval = 1
        if end is None:
            end = value
        self.open_database()
        nv = {key: value}
        old_legends = self.cursor.execute("SELECT * FROM data_points WHERE chart_id = '" + c_id + "'").fetchall()
        for row in old_legends:
            if row[6] is not None:
                nv = json.loads(row[6])
            for x in range(value, end+1, interval):
                nv[key] = x
                if x == value:
                    self.cursor.execute("REPLACE INTO data_points (uuid, chart_id, create_time, legends, platform, x_value, y_value) VALUES (?,?,?,?, ?,?,?)",
                                        (row[0], c_id, datetime.datetime.now(), json.dumps(nv), row[3], row[4], row[5]))
                else:
                    self.cursor.execute("INSERT INTO data_points (uuid, chart_id, create_time, legends, platform, x_value, y_value) VALUES (?,?,?,?, ?,?,?)",
                                        (str(uuid.uuid4()), c_id, datetime.datetime.now(), json.dumps(nv), row[3], row[4], row[5]))

        if not old_legends:
            for x in range(value, end+1, interval):
                nv[key] = x
                n_uid = str(uuid.uuid4())
                self.cursor.execute("INSERT INTO data_points (uuid, chart_id, create_time, legends) VALUES (?,?,?,?)",
                                    (n_uid, c_id, datetime.datetime.now(), json.dumps(nv)))
        self.close_database()


class ChartWrapper:
    def __init__(self, c_name="Plot", x=None, y=None, u=None):
        self.chart_name = c_name
        self.chart_id = 'c5e912aa-32d5-4f07-b73f-7cf3da5fd0d9'
        self.create_time = None
        self.user = u
        self.x_title = x
        self.y_title = y
        self.legends = None # this is in json

    def update_chart_values(self, db):
        self.chart_id = db.create_chart(self.chart_name, self.x_title, self.y_title, self.legends, self.chart_id, self.user)

    def add_chart_legends(self, db, key, value, end=None, interval=None):
        self.update_chart_values(db)
        if key == self.x_title:
            db.update_datapoint_x(self.chart_id, value)
        elif key == self.y_title:
            db.update_datapoint_y(self.chart_id, value)
        else: # it will always go to legends
            # no need to check if already exist first
            db.update_datapoint_legends(self.chart_id, key, value, end, interval)
