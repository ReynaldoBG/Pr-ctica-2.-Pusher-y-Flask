from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

app = Flask(__name__)

def db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='as_practica2'
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contacto')
def contacto():
    return render_template("formulario.html")

@app.route('/alumnos/guardar', methods=['POST'])
def guardar_alumno():
    email = request.form['email']
    nombre = request.form['nombre']
    asunto = request.form['asunto']

    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)", 
                   (email, nombre, asunto))
    conn.commit()
    
    cursor.close()
    conn.close()

    pusher_client = pusher.Pusher(
        app_id="1767326",
        key="42b9b4800a5a14fc436c",
        secret="569fb5bfe16d510b6ce7",
        cluster="us2",
        ssl=True
    )


    pusher_client.trigger('my-channel', 'my-event', {
        'message': 'Nuevo registro agregado'
    })
    print("Evento emitido a Pusher")  

    return render_template("formulario.html")

@app.route('/alumnos/obtener', methods=['GET'])
def obtener_alumnos():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM tst0_contacto")
    registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(registros)

if __name__ == '__main__':
    app.run(debug=True)
