import os
import sqlite3


class P48CierreRepository:

    def __init__(self, cycles):
        self.path_db = "C:/ESIOS/p48cierre/p48cierre.db"
        self.cycles = cycles

    def create_db_file_and_table(self):
        f = open(self.path_db, 'w')
        f.close()
        con = sqlite3.connect(self.path_db)
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE P48Cierre (Ciclo TEXT, Fecha TEXT, Hora INTEGER CHECK(Hora <= 24 AND Hora >= 1), Produccion '
            'TEXT,PRIMARY KEY(Ciclo,Fecha,Produccion,Hora))')
        con.commit()
        cur.close()
        con.close()

    def insert(self, data):
        # Hacemos la conexión a la base de datos, si existe el fichero
        if not os.path.exists(self.path_db):
            self.create_db_file_and_table()

        try:
            con = sqlite3.connect(self.path_db)
            cur = con.cursor()
            rows = 0
            for cycle in self.cycles:
                try:
                    for i in range(len(data[cycle])):
                        # Hacemos los inserts a la base de datos
                        cur.execute("INSERT INTO P48Cierre values (?,?,?,?)",
                                    (cycle, data["date"], i + 1, data[cycle][i + 1]))
                        rows += 1
                except KeyError:
                    continue
            con.commit()

        except sqlite3.Error:
            con.rollback()
            raise Exception("Error de base de datos: probablemente datos ya añadidos")
        finally:
            cur.close()
            con.close()
        return rows

    def find(self, data):
        try:
            con = sqlite3.connect(self.path_db)
            cur = con.cursor()
            for cycle in data['cycles']:
                # Hacemos los inserts a la base de datos
                cur.execute("SELECT Hora, Produccion FROM P48Cierre WHERE Ciclo=? AND Fecha=? ORDER BY Hora",
                            (cycle, data['date']))
                rows = cur.fetchall()
                data[cycle] = {}
                for row in rows:
                    data[cycle][row[0]] = row[1]
        except sqlite3.Error:
            raise Exception("Error de base de datos: problema al consultar los datos")
        finally:
            cur.close()
            con.close()

        return data
