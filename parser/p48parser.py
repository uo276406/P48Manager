import xml.etree.ElementTree as ET
import os

from cicles.p48cicles import P48cicles

class P48parser():

    def parse(self, filename):
        try:
            root = ET.parse(filename).getroot()
            res = {}
            res["date"] = self.get_file_date(filename)
            for serie in root:
                for cicle in serie:
                    if cicle.tag == '{urn:sios.ree.es:p48cierre:1:0}UPEntrada':
                        if cicle.attrib['v'] in P48cicles().list:
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
                                            data[hour] = sum_cuarter
                                            sum_cuarter = 0
                            res[name_cicle] = data
        except FileNotFoundError:
            raise Exception("Error: Fichero no encontrado")
        except ET.ParseError:
            raise Exception("Error: Fallo al procesar el fichero. Asegurese que sea el tipo correcto.")
        return res

    def get_file_date(self, filename):
        date = os.path.basename(filename)
        date_list = date.split('_')
        date = date_list[1].split('.')[0]
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        return date