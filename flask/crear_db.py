import sqlite3  

def crear_db():  
    conn = sqlite3.connect('database.db')  
    c = conn.cursor()  

    # tabla usuarios  
    c.execute('''  
        CREATE TABLE IF NOT EXISTS usuarios (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            apellido TEXT NOT NULL,  
            nombre TEXT NOT NULL,  
            direccion TEXT NOT NULL,  
            dni TEXT NOT NULL UNIQUE  
        )  
    ''')  

    # datos 
    usuarios = [  
        ('Iglesias', 'Jeremías', 'Gral Paz 1234', '45624362'),  
        ('Gómez', 'María', 'Av Italia 4321', '12345678')  
    ]  

    for u in usuarios:  
        c.execute('INSERT OR IGNORE INTO usuarios (apellido, nombre, direccion, dni) VALUES (?, ?, ?, ?)', u)  

    conn.commit()  
    conn.close()  
    print("Base de datos creada y datos insertados.")  

if __name__ == '__main__':  
    crear_db()