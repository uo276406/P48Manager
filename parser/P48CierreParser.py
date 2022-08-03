import xml.etree.ElementTree as ET
import os

class P48CierreParser():

    def __init__(self, cicles):
        self.cicles = cicles

    def parse(self, filepath):
        try:
            root = ET.parse(filepath).getroot()
            res = {}
            res["date"] = self.get_file_date(filepath)
            for serie in root:
                for cicle in serie:
                    if cicle.tag == '{urn:sios.ree.es:p48cierre:1:0}UPEntrada':
                        if cicle.attrib['v'] in self.cicles:
                            name_cicle = cicle.attrib['v']
                            for cicle in serie:
                                if cicle.tag == '{urn:sios.ree.es:p48cierre:1:0}Periodo':
                                    sum_cuarter = 0.
                                    is_cuarter = 0
                                    hour = 0
                                    data = {}
                                    for intervalo in cicle:
                                        for value in intervalo:
                                            if value.tag =='{urn:sios.ree.es:p48cierre:1:0}Ctd':
                                                sum_cuarter += float(value.attrib['v'])
                                                is_cuarter += 1
                                        if is_cuarter % 4 == 0 and is_cuarter != 0:
                                            hour += 1
                                            sum_cuarter = str(sum_cuarter).replace('.', ',')
                                            data[hour] = sum_cuarter
                                            sum_cuarter = 0
                            res[name_cicle] = data
                    elif cicle.tag == '{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}UPEntrada':
                        if cicle.attrib['v'] in self.cicles:
                            name_cicle = cicle.attrib['v']
                            for cicle in serie:
                                if cicle.tag == '{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}Periodo':
                                    data = {}
                                    hour = 0
                                    for intervalo in cicle:
                                        production = ''
                                        for value in intervalo:
                                            if value.tag =='{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}Ctd':
                                                production = value.attrib['v'].replace('.', ',')
                                                hour += 1
                                                data[hour] = production
                            res[name_cicle] = data
        except FileNotFoundError:
            raise Exception("Error: Fichero no encontrado")
        except ET.ParseError:
            raise Exception("Error: Fallo al procesar el fichero. Asegurese que sea el tipo correcto.")
        return res

    def get_file_date(self, filepath):
        date = os.path.basename(filepath)
        date_list = date.split('_')
        date = date_list[1].split('.')[0]
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        return date