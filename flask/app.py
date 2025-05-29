from flask import Flask, render_template, request, jsonify  
import sqlite3  

app = Flask(__name__)  

def get_db_connection():  
    conn = sqlite3.connect('database.db')  
    conn.row_factory = sqlite3.Row  
    return conn  

@app.route('/')  
def mostrar_datos():  
    conn = get_db_connection()  
    usuario = conn.execute('SELECT * FROM usuarios WHERE dni = ?', ('45624362',)).fetchone()  
    conn.close()  

    if usuario is None:  
        return "Usuario no encontrado", 404  

    return render_template('datos.html',  
                           apellido=usuario['apellido'],  
                           nombre=usuario['nombre'],  
                           direccion=usuario['direccion'],  
                           dni=usuario['dni'])  

@app.route('/buscar')  
def buscar_usuario():  
    dni = request.args.get('dni')  

    if not dni:  
        return jsonify({'error': 'Debes enviar el parámetro dni en la URL'}), 400  

    conn = get_db_connection()  
    usuario = conn.execute('SELECT apellido, nombre FROM usuarios WHERE dni = ?', (dni,)).fetchone()  
    conn.close()  

    if usuario:  
        return jsonify({'apellido': usuario['apellido'], 'nombre': usuario['nombre']}), 200  
    else:  
        return "EL Usuario no Existe!!!", 404  

if __name__ == '__main__':  
    app.run(debug=True)