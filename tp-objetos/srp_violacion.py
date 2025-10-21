import json  
import csv  
import smtplib  

class Reporte:  
    def __init__(self, source_type, source_path):  
        self.source_type = source_type  # 'csv', 'list', 'db' (simulado)  
        self.source_path = source_path  

    def obtener_datos(self):  
        if self.source_type == 'csv':  
            datos = []  
            with open(self.source_path, newline='') as f:  
                reader = csv.DictReader(f)  
                for row in reader:  
                    datos.append({k: float(v) if v.replace('.','',1).isdigit() else v for k,v in row.items()})  
            return datos  
        elif self.source_type == 'list':  
            return self.source_path  # aquí source_path es una lista ya  
        elif self.source_type == 'db':  
            return [{'valor': 10}, {'valor': 20}]  
        else:  
            return []  

    def procesar(self, datos, operacion='suma', campo='valor'):  
        if operacion == 'suma':  
            return sum(item.get(campo, 0) for item in datos)  
        elif operacion == 'promedio':  
            vals = [item.get(campo, 0) for item in datos]  
            return sum(vals)/len(vals) if vals else 0  
        elif operacion == 'filtrar':  
            return [d for d in datos if d.get(campo, 0) > 0]  
        else:  
            return datos  

    def generar_salida(self, resultado, formato='texto'):  
        if formato == 'texto':  
            return f"Resultado: {resultado}"  
        elif formato == 'json':  
            return json.dumps({'resultado': resultado})  
        elif formato == 'html':  
            return f"<html><body><h1>Resultado</h1><p>{resultado}</p></body></html>"  
        else:  
            return str(resultado)  

    def guardar(self, contenido, destino='archivo', path='salida.txt', send_email_conf=None):  
        if destino == 'archivo':  
            with open(path, 'w') as f:  
                f.write(contenido)  
            return True  
        elif destino == 'email':  
            if not send_email_conf:  
                raise ValueError("Falta configuración de email")  
            smtp = smtplib.SMTP(send_email_conf['host'])  
            smtp.sendmail(send_email_conf['from'], send_email_conf['to'], contenido)  
            smtp.quit()  
            return True  
        else:  
            return False  

    def ejecutar(self, operacion='suma', campo='valor', formato='texto', destino='archivo', path='salida.txt'):  
        datos = self.obtener_datos()  
        resultado = self.procesar(datos, operacion=operacion, campo=campo)  
        salida = self.generar_salida(resultado, formato=formato)  
        self.guardar(salida, destino=destino, path=path)  
        return salida