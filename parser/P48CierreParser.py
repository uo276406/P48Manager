import os
import xml.etree.ElementTree as ET


class P48CierreParser:

    def __init__(self, cycles):
        self.cycles = cycles

    def parse(self, filepath):
        try:
            root = ET.parse(filepath).getroot()
            res = {"date": self.get_file_date(filepath)}
            for serie in root:
                for cycle in serie:
                    if cycle.tag == '{urn:sios.ree.es:p48cierre:1:0}UPEntrada':
                        if cycle.attrib['v'] in self.cycles:
                            name_cycle = cycle.attrib['v']
                            data = {}
                            for cycle in serie:
                                if cycle.tag == '{urn:sios.ree.es:p48cierre:1:0}Periodo':
                                    sum_quarter = 0.
                                    is_quarter = 0
                                    hour = 0
                                    for interval in cycle:
                                        for value in interval:
                                            if value.tag == '{urn:sios.ree.es:p48cierre:1:0}Ctd':
                                                sum_quarter += float(value.attrib['v'])
                                                is_quarter += 1
                                        if is_quarter % 4 == 0 and is_quarter != 0:
                                            hour += 1
                                            sum_quarter = str(sum_quarter).replace('.', ',')
                                            data[hour] = sum_quarter
                                            sum_quarter = 0
                            res[name_cycle] = data
                    elif cycle.tag == '{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}UPEntrada':
                        if cycle.attrib['v'] in self.cycles:
                            name_cycle = cycle.attrib['v']
                            data = {}
                            for cycle in serie:
                                if cycle.tag == '{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}Periodo':
                                    hour = 0
                                    for interval in cycle:
                                        production = ''
                                        for value in interval:
                                            if value.tag == '{http://sujetos.esios.ree.es/schemas/2007/03/07/P48Cierre-esios-MP/}Ctd':
                                                production = value.attrib['v'].replace('.', ',')
                                                hour += 1
                                                data[hour] = production
                            res[name_cycle] = data
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
