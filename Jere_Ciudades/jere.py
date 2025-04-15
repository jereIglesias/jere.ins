import sqlite3  

# Conectar a la base de datos  
conn = sqlite3.connect('ciudades_provincias.db')  
cursor = conn.cursor()  

# Leer y ejecutar el script 
def ejecutar_sql_script(archivo_sql):  
    with open(archivo_sql, 'r') as file:  
        sql_script = file.read()  
    
    cursor.executescript(sql_script)  
    conn.commit()  

# Consultar provincias  
def consultar_provincias():  
    cursor.execute('SELECT * FROM provincias')  
    return cursor.fetchall()  

# Consultar ciudades  
def consultar_ciudades():  
    cursor.execute('SELECT * FROM ciudades')  
    return cursor.fetchall()  

# Función principal  
def main():  
    # Ejecutar el script SQL para crear tablas y cargar datos  
    ejecutar_sql_script('ciudades.sql')  

    # Consultar y mostrar provincias  
    print("Provincias:")  
    provincias = consultar_provincias()  
    for provincia in provincias:  
        print(provincia)  

    # Consultar y mostrar ciudades  
    print("\nCiudades:")  
    ciudades = consultar_ciudades()  
    for ciudad in ciudades:  
        print(ciudad)  

# Ejecutar el programa  
if __name__ == '__main__':  
    main()  

# Cerrar la conexión  
conn.close()