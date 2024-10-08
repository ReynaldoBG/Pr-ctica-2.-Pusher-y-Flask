from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

app = Flask(__name__)

def db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contacto')
def contacto():
    return render_template("formulario.html")

@app.route('/alumnos/guardar', methods=['POST'])
def guardar_alumno():
    id_registro = request.form.get('id')  
    email = request.form['email']
    nombre = request.form['nombre']
    asunto = request.form['asunto']

    conn = db_connection()
    cursor = conn.cursor()
    
    if id_registro:  
        cursor.execute(
            "UPDATE tst0_contacto SET Correo_Electronico = %s, Nombre = %s, Asunto = %s WHERE Id_Contacto = %s",
            (email, nombre, asunto, id_registro)
        )
    else:  
        cursor.execute(
            "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)",
            (email, nombre, asunto)
        )
    
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
        'message': 'Registro guardado'
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

@app.route('/alumnos/eliminar/<int:id>', methods=['DELETE'])
def eliminar_alumno(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tst0_contacto WHERE Id_Contacto = %s", (id,))
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

    pusher_client.trigger('my-channel', 'eliminar-event', {
        'id': id
    })
    
    return jsonify({'status': 'Registro eliminado exitosamente'}), 200

@app.route('/alumnos/editar/<int:id>', methods=['GET'])
def editar_alumno(id):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tst0_contacto WHERE Id_Contacto = %s", (id,))
    registro = cursor.fetchone()

    cursor.close()
    conn.close()

    if registro:
        return render_template("formulario.html", registro=registro)
    else:
        return "Registro no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
