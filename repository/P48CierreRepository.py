import sqlite3
import os

from cicles.P48CierreCicles import P48CierreCicles

class P48CierreRepository():
    
    def __init__(self, cicles):
        self.pathdb = "C:/ESIOS/p48cierre/p48cierre.db"
        self.cicles = cicles
    
    def create_db_file_and_table(self):
        f = open(self.pathdb, 'w')
        f.close()
        con = sqlite3.connect(self.pathdb)
        cur = con.cursor()
        cur.execute('CREATE TABLE P48Cierre (Ciclo TEXT, Fecha TEXT, Hora INTEGER CHECK(Hora <= 24 AND Hora >= 1), Produccion TEXT,PRIMARY KEY(Ciclo,Fecha,Produccion,Hora))')
        con.commit()
        cur.close()
        con.close()
    

    
    def insert(self, data):
        # Hacemos la conexión a la base de datos, si existe el fichero
        if not os.path.exists(self.pathdb):
            self.create_db_file_and_table()
        
        try:
            con = sqlite3.connect(self.pathdb)
            cur = con.cursor()
            rows = 0
            for cicle in self.cicles:
                try:	
                    for i in range(len(data[cicle])):
                        # Hacemos los inserts a la base de datos
                        cur.execute("INSERT INTO P48Cierre values (?,?,?,?)", (cicle, data["date"], i+1, data[cicle][i+1]))
                        rows+=1	
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
            con = sqlite3.connect(self.pathdb)
            cur = con.cursor()
            for cicle in data['cicles']:
                # Hacemos los inserts a la base de datos
                cur.execute("SELECT Hora, Produccion FROM P48Cierre WHERE Ciclo=? AND Fecha=? ORDER BY Hora", (cicle, data['date']))
                rows = cur.fetchall()
                data[cicle] = {}
                for row in rows:
                    data[cicle][row[0]] = row[1]
        except sqlite3.Error:
            raise Exception("Error de base de datos: problema al consultar los datos")
        finally:
            cur.close()
            con.close()

        return data