if __name__ == "__main__":  
    datos = [{'valor': 10}, {'valor': 20}, {'valor': 30}]  

    ds = ListDataSource(datos)  
    proc = SumProcessor(field='valor')  
    fmt = JSONFormatter()  
    delivery = NullDelivery()  

    runner = ReportRunner(ds, proc, fmt, delivery)  
    salida = runner.run()  
    print(salida)