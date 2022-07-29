import sqlite3
import os

from cicles.p48cicles import p48cicles

class p48repository():
    def __init__(self):
        self.pathdb = "C:/ESIOS/p48cierre/p48cierre.db"
    
    def create_db_file_and_table(self):
        f = open(self.pathdb, 'w')
        f.close()
        con = sqlite3.connect(self.pathdb)
        cur = con.cursor()
        cur.execute('CREATE TABLE P48Cierre (Ciclo TEXT, Fecha TEXT, Hora INTEGER CHECK(Hora <= 24 AND Hora >= 1), Produccion REAL,PRIMARY KEY(Ciclo,Fecha,Produccion,Hora))')
        con.commit()
        cur.close()
        con.close()
    

    
    def insert(self, data):
        # Hacemos la conexión a la base de datos, si existe el fichero
        if not os.path.exists(self.pathdb):
            self.create_db_file_and_table()
        
        con = sqlite3.connect(self.pathdb)
        cur = con.cursor()
        try:
            rows = 0
            for cicle in p48cicles().list:
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