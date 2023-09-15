from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoflask'

# Almacenamiento de la conexión en una variable
mysql = MySQL(app)

try:
    mysql.connection.ping(reconnect=True)
except AttributeError as e:
    print(f"Error al conectar a MySQL: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informacion/')
def informacion():
    return render_template('informacion.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/insertar_coche', methods=['GET', 'POST'])
def insertar_coche():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches (marca, modelo, precio, ciudad) VALUES (%s, %s, %s, %s)",
                       (marca, modelo, precio, ciudad))
        mysql.connection.commit()

        return redirect(url_for('index'))
    return render_template('insertar_coche.html')

@app.route('/coches')
def coches():
    # Carga de cursor SQL
    cursor = mysql.connection.cursor()
    # Instrucción SQL
    cursor.execute("SELECT * FROM coches")
    # Recorrido de la información almacenada en coches
    coches = cursor.fetchall()
    # Cierre de cursor
    cursor.close()

    return render_template('coches.html', coches=coches)

@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    cursor = mysql.connection.cursor()
    # Instrucción SQL con cláusula WHERE
    cursor.execute(f"DELETE FROM coches WHERE id={coche_id}")
    mysql.connection.commit()
    # El commit finaliza la transacción actual
    return redirect(url_for('coches'))

@app.route('/editar-coche/<coche_id>', methods=['GET', 'POST'])
def editar_coche(coche_id):
    if request.method == 'POST':
        # Acceso a los campos del formulario
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        # Carga de cursor SQL
        cursor = mysql.connection.cursor()
        # Instrucción SQL
        cursor.execute("""
        UPDATE coches
        SET marca=%s, modelo=%s, precio=%s, ciudad=%s WHERE id = %s
        """, (marca, modelo, precio, ciudad, coche_id))
        # El commit finaliza la transacción actual
        mysql.connection.commit()
        return redirect(url_for('coches'))

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM coches WHERE id={coche_id}")
    # Recorrido de la información almacenada en coches
    coche = cursor.fetchall()
    # Cierre de cursor
    cursor.close()

    return render_template('insertar_coche.html', coche=coche[0])

if __name__ == '__main__':
    app.run()
