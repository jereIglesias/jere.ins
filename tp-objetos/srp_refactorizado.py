import json  
import csv  
from abc import ABC, abstractmethod  

# Fuentes de datos  
class DataSource(ABC):  
    @abstractmethod  
    def get_data(self):  
        pass  

class CSVDataSource(DataSource):  
    def __init__(self, path):  
        self.path = path  

    def get_data(self):  
        datos = []  
        with open(self.path, newline='') as f:  
            reader = csv.DictReader(f)  
            for row in reader:  
                datos.append({k: float(v) if v.replace('.','',1).isdigit() else v for k,v in row.items()})  
        return datos  

class ListDataSource(DataSource):  
    def __init__(self, data_list):  
        self.data_list = data_list  

    def get_data(self):  
        return self.data_list  

class MockDBDataSource(DataSource):  
    def get_data(self):  
        return [{'valor': 1}, {'valor': 2}, {'valor': 3}]  


# Procesadores de datos  
class DataProcessor(ABC):  
    @abstractmethod  
    def process(self, data):  
        pass  

class SumProcessor(DataProcessor):  
    def __init__(self, field='valor'):  
        self.field = field  

    def process(self, data):  
        return sum(item.get(self.field, 0) for item in data)  

class AverageProcessor(DataProcessor):  
    def __init__(self, field='valor'):  
        self.field = field  

    def process(self, data):  
        vals = [item.get(self.field, 0) for item in data]  
        return sum(vals)/len(vals) if vals else 0  

class FilterProcessor(DataProcessor):  
    def __init__(self, predicate):  
        self.predicate = predicate  

    def process(self, data):  
        return [d for d in data if self.predicate(d)]  


# Formatters / Generadores de salida  
class ReportFormatter(ABC):  
    @abstractmethod  
    def format(self, result):  
        pass  

class TextFormatter(ReportFormatter):  
    def format(self, result):  
        return f"Resultado: {result}"  

class JSONFormatter(ReportFormatter):  
    def format(self, result):  
        return json.dumps({'resultado': result})  

class HTMLFormatter(ReportFormatter):  
    def format(self, result):  
        return f"<html><body><h1>Resultado</h1><p>{result}</p></body></html>"  


# Delivery / Almacenamiento  
class Delivery(ABC):  
    @abstractmethod  
    def deliver(self, content):  
        pass  

class FileDelivery(Delivery):  
    def __init__(self, path):  
        self.path = path  

    def deliver(self, content):  
        with open(self.path, 'w') as f:  
            f.write(content)  
        return True  

class NullDelivery(Delivery):  
    def deliver(self, content):  
        return True  


# Orquestador  
class ReportRunner:  
    def __init__(self, datasource: DataSource, processor: DataProcessor, formatter: ReportFormatter, delivery: Delivery):  
        self.datasource = datasource  
        self.processor = processor  
        self.formatter = formatter  
        self.delivery = delivery  

    def run(self):  
        datos = self.datasource.get_data()  
        resultado = self.processor.process(datos)  
        salida = self.formatter.format(resultado)  
        self.delivery.deliver(salida)  
        return salida