from tempfile import template
from MySQLdb.cursors import Cursor
from xml.sax.handler import feature_external_ges
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask.wrappers import Request
from flask import request
from flask_paginate import Pagination, get_page_parameter
from flask_mysqldb import MySQL
from datetime import date, datetime, timedelta
from flask import make_response
import http.cookiejar

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rolex.b1'
app.config['MYSQL_DB'] = 'consultas_iub'


mysql = MySQL(app)
app.secret_key = 'ghjklñ'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')  # login Psicologo
def index():
    return render_template('admin/login.html')


@app.route('/index_user')
def index_user():
    return render_template('index.html')


@app.route('/base')
def base():
    return render_template('admin/home.html')


# Index Admin
@app.route('/index_admin')
def index_admin():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM profesor')
    profesor = cursor.fetchall()
    print(profesor)
    cursor.close()
    curs = mysql.connection.cursor()
    curs.execute(
        'SELECT id_profesor, COUNT(*) AS repeticiones FROM consulta GROUP BY id_profesor')
    cons = curs.fetchone()
    print(cons)
    return render_template('admin/index.html', profesor=profesor, cons=cons)


@app.route('/login_profe')  # Login_Profe_URL
def login_profe():
    return render_template('profesor/login.html')


@app.route('/contacto')  # contactanos_URL
def contacto():
    return render_template('contactanos/index.html')


# registro_URL_Estudiante
@app.route('/registro')
def registro():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM programas')
        programa = cursor.fetchall()
        cursor.close()
        program = []
        for rows in programa:
            data = {"id": rows[0], "nombre": rows[1]}
            program.append(data)
            # print(program)

        curs = mysql.connection.cursor()
        curs.execute('SELECT * FROM tipo')
        tipo = curs.fetchall()
        curs.close()
        docs = []
        for row in tipo:
            date = {"id": row[0], "tipo": row[1]}
            docs.append(date)
            # print(docs)

        return render_template('estudiante/registro.html', program=program, docs=docs)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})


# Login_Est_URL
@app.route('/login_est')
def login_est():
    return render_template('estudiante/login.html')


# Index Profesor
@app.route('/index_profe', methods=['GET', 'POST'])
def index_profe():
    id_profe = session['id']
    if request.method == 'GET':
        search = request.args.get('search')
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT c.id_consulta, est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, p.apellido, 
                       c.descripcion FROM consulta c INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p ON 
                       c.id_profesor = p.id WHERE c.descripcion LIKE %s AND c.id_profesor=%s''', (f"%{search}%", id_profe))

        datos = cursor.fetchall()
        cursor.close()
        payload_search = []
        for rows in datos:
            result = {
                'id': rows[0],
                'nombre_estudiante': rows[1],
                'apellido_estudiante': rows[2],
                'tipo_documento': rows[3],
                'numero_estudiante': rows[4],
                'programa': rows[5],
                'correo': rows[6],
                'fecha': rows[7],
                'descripcion': rows[8]
            }
            payload_search.append(result)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT c.id_consulta, est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, CONVERT(c.fecha, DATETIME) AS fecha, p.nombre, 
                       p.apellido, c.descripcion FROM consulta c INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p 
                       ON c.id_profesor = p.id WHERE id_profesor=%s''', (id_profe,))
        dato = cursor.fetchall()
        cursor.close()
        payload = []
        for row in dato:
            result = {
                'id': row[0],
                'nombre_estudiante': row[1],
                'apellido_estudiante': row[2],
                'tipo_documento': row[3],
                'numero_estudiante': row[4],
                'programa': row[5],
                'correo': row[6],
                'fecha': row[7],
                'descripcion': row[10]
            }
            payload.append(result)

        page = int(request.args.get(get_page_parameter(), 1))
        per_page = 10  # Cantidad de resultados por página
        offset = (page - 1) * per_page
        pagination = Pagination(page=page, per_page=per_page, total=len(
            payload), css_framework='bootstrap5')

        return render_template('profesor/index.html', payload=payload[offset:offset + per_page], id_profe=id_profe, pagination=pagination, payload_search=payload_search)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})


@app.route('/res_profesor')
def res_profesor():
    return render_template('admin/register.html')


# Registrar profesor
@app.route('/register')  
def register():
    datos = ['', '', '', '']
    return render_template('admin/register.html', datos=datos)




@app.route('/register')
# Registrar caso Estudiante
@app.route('/register_caso')  # Redireccionar Caso
def register_caso():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM modulo")
        modulos = cursor.fetchall()
        cursor.close()

        payload = []
        for row in modulos:
            moduls = {'id': row[0], 'nombre_modulo': row[2]}
            payload.append(moduls)

        curs = mysql.connection.cursor()
        curs.execute("SELECT * FROM profesor")
        profesor = curs.fetchall()
        curs.close()
        profe = []
        for rows in profesor:
            data = {"id": rows[0], "nombre": rows[1], "apellido": rows[2]}
            profe.append(data)

        return render_template('estudiante/register.html', payload=payload, profe=profe)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})


# Registrar Estudiante
@app.route('/register_student', methods=['POST'])
def register_student():
    msg= ''
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo = request.form['tipo']
        documento = request.form['documento']
        programa = request.form['programa']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO estudiante(nombre, apellido, tipo_documento, programa, correo, contraseña, numero_estudiante) VALUES (%s, %s, %s, %s, %s, %s, %s)',(str(nombre), str(apellido), str(tipo), str(programa), str(correo), str(contraseña), str(documento)))
        
        mysql.connection.commit()
        new_student_id = cursor.lastrowid

        # Agrega el ID a la sesión
        session['id'] = new_student_id
        cursor.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_est', msg=msg))


# Registrar Profesor
@app.route('/register_profesor', methods=['POST'])
def register_profesor():
    msg = ''
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        # tipo = request.form['tipo']
        # documento = request.form['documento']
        # programa = request.form['programa']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO profesor(nombre, apellido, correo, password) VALUES (%s, %s, %s, %s)', (str(
            nombre), str(apellido), str(correo), str(contraseña)))

        mysql.connection.commit()
        cursor.close()
        msg = 'Se ha registrado correctamente!'
    return redirect(url_for('index_admin', msg=msg))


# Index Estudiante
@app.route('/index_est', methods=['GET', 'POST'])
def index_est():
    id_est = session['id']
    print(id_est)
    print(session.keys())
    if 'id' not in session:
        return redirect(url_for('login_est'))
    else:
        if request.method == 'GET':
            search = request.args.get('search')
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, p.apellido, 
                    c.descripcion FROM consulta c INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p ON 
                    c.id_profesor = p.id WHERE c.descripcion LIKE %s AND c.id_estudiante=%s''', (f"%{search}%", id_est))

            datos = cursor.fetchall()
            cursor.close()
            payload_search = []
            for rows in datos:
                result = {
                    'nombre_estudiante': rows[0],
                    'apellido_estudiante': rows[1],
                    'programa': rows[4],
                    'fecha': rows[6],
                    'profesor': rows[7],
                    'apellido_profesor': rows[8],
                    'descripcion': rows[9]
                }
                payload_search.append(result)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, p.apellido, c.descripcion FROM consulta c 
                           INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p ON c.id_profesor = p.id WHERE c.id_estudiante=%s''', (id_est,))

            modulo = cursor.fetchall()

            cursor.close()
            payload = []
            for row in modulo:
                data = {
                    'nombre_estudiante': row[0],
                    'apellido_estudiante': row[1],
                    'programa': row[4],
                    'fecha': row[6],
                    'profesor': row[7],
                    'apellido_profesor': row[8],
                    'descripcion': row[9]
                }
                payload.append(data)

            # Paginación
            page = int(request.args.get(get_page_parameter(), 1))
            per_page = 10  # Cantidad de resultados por página
            offset = (page - 1) * per_page
            pagination = Pagination(page=page, per_page=per_page, total=len(
                payload), css_framework='bootstrap5')

            return render_template('estudiante/index.html', payload=payload[offset:offset + per_page], id_est=id_est, pagination=pagination, payload_search=payload_search)
        except Exception as e:
            print(e)
            return jsonify({"informacion": str(e)})


# Actulizar Perfil Estudiante (Pendiente)
@app.route('/update_profile')
def update_profile():
    return render_template('estudiante/update_profile.html')


# Login Admin
@app.route('/login', methods=['POST'])
def login():
    msg = ''
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM administrador WHERE correo = %s AND contraseña = %s', (correo, contraseña))
        user = cursor.fetchone()
        print(user)
        if user:

            return redirect(url_for('index_admin'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('admin/login.html', msg=msg)


@app.route('/login_p', methods=['POST'])  # Login_Profesor
def login_p():
    msg = ''
    if request.method == 'POST':
        documentop = request.form['documento']
        contraseñap = request.form['contraseña']
        Cursor = mysql.connection.cursor()
        Cursor.execute(
            'SELECT * FROM profesor WHERE correo = %s AND password = %s', (documentop, contraseñap))
        user = Cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['nombre'] = user[1]
            session['apellido'] = user[2]
            session['correo'] = user[3]
            return redirect(url_for('index_profe'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('profesor/login.html', msg=msg)


@app.route('/login_estu', methods=['POST'])
def login_estu():
    if request.cookies.get('loggedin') == 'true':
        id = int(request.cookies.get('id'))
        nombre = request.cookies.get('nombre')
        apellido = request.cookies.get('apellido')
        correo = request.cookies.get('correo')

    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM estudiante WHERE correo = %s AND contraseña = %s', (correo, contraseña))
        user = cursor.fetchone()
        # print(user)
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['nombre'] = user[1]
            session['apellido'] = user[2]
            session['correo'] = user[5]
            id = session['id']
            print(id)
            response = make_response(redirect(url_for('index_est')))
            response.set_cookie('loggedin', 'true')
            response.set_cookie('id', str(session['id']))
            response.set_cookie('nombre', session['nombre'])
            response.set_cookie('apellido', session['apellido'])
            response.set_cookie('correo', session['correo'])
            return response

        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('estudiante/login.html', msg=msg)


@app.route('/mis_consultas')
def mis_consultas():
    id_est = session['id']
    print(id_est)
    print(session.keys())
    if 'id' not in session:
        return redirect(url_for('login_est'))
    else:
        if request.method == 'GET':
            search = request.args.get('search')
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT e.nombre, e.apellido, r.fecha as FECHA, c.descripcion AS DESCRIPCION, r.modalidad, p.nombre AS PROFESOR, p.apellido FROM res_consulta r INNER JOIN estudiante e ON
                           r.id_estudiante = e.id INNER JOIN consulta c ON r.id_consulta = c.id_consulta INNER JOIN profesor p ON r.id_profesor = p.id WHERE c.descripcion LIKE %s AND c.id_estudiante=%s''', (f"%{search}%", id_est))

            datos = cursor.fetchall()
            cursor.close()
            payload_search = []
            for rows in datos:
                result = {
                    'nombre_estudiante': rows[0],
                    'apellido_estudiante': rows[1],
                    'fecha': rows[2],
                    'descripcion': rows[3],
                    'modalidad': rows[4],
                    'nombre_profesor': rows[5],
                    'apellido_profesor': rows[6]
                }
                payload_search.append(result)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                           SELECT e.nombre, e.apellido, r.fecha as FECHA, c.descripcion AS DESCRIPCION, r.modalidad, p.nombre AS PROFESOR, p.apellido, r.estado FROM res_consulta r INNER JOIN estudiante e ON
                           r.id_estudiante = e.id INNER JOIN consulta c ON r.id_consulta = c.id_consulta INNER JOIN profesor p ON r.id_profesor = p.id WHERE r.id_estudiante=%s''', (id_est,))

            modulo = cursor.fetchall()
            print(modulo)

            cursor.close()
            payload = []
            for row in modulo:
                data = {
                    'nombre_estudiante': row[0],
                    'apellido_estudiante': row[1],
                    'fecha': row[2],
                    'descripcion': row[3],
                    'modalidad': row[4],
                    'nombre_profesor': row[5],
                    'apellido_profesor': row[6],
                    'estado': row[7]
                }
                payload.append(data)

            # Paginación
            page = int(request.args.get(get_page_parameter(), 1))
            per_page = 10  # Cantidad de resultados por página
            offset = (page - 1) * per_page
            pagination = Pagination(page=page, per_page=per_page, total=len(
                payload), css_framework='bootstrap5')

            return render_template('estudiante/res_consulta.html', payload=payload[offset:offset + per_page], id_est=id_est, pagination=pagination, payload_search=payload_search)
        except Exception as e:
            print(e)
            return jsonify({"informacion": str(e)})


@app.route('/res_cons', methods=['POST'])  # Registrar Consulta estudiante
def res_cons():
    user = session['id']
    print(user)
    if request.method == 'POST':
        profesor = request.form['profesor']
        modulo = request.form['modulo']
        consulta = request.form['consulta']
        fecha = request.form['fecha']
        cons = mysql.connection.cursor()
        cons.execute('SELECT * FROM profesor WHERE nombre = %s',
                     [str(profesor)])
        result = cons.fetchone()
        if result:
            id_profesor = result[0]
            print(id_profesor)
        cons.close()
        con = mysql.connection.cursor()
        con.execute(
            'SELECT * FROM modulo WHERE nombre_modulo = %s', [str(modulo)])
        res = con.fetchone()
        if res:
            global id_modulo
            id_modulo = res[0]
            print(id_modulo)
        con.close()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO consulta (id_estudiante, id_profesor, fecha, descripcion, id_modulo) VALUES (%s, %s, %s, %s, %s)',
                    (user, id_profesor, fecha, consulta, id_modulo))
        mysql.connection.commit()
        cur.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_est', msg=msg))


# Actualizar consulta profesor
@app.route('/update/<int:id>', methods=['GET'])
def update(id):
    global id_consulta
    id_consulta = 0
    id_consulta = id
    print(id)
    ''''No es obligación utilizar el session del profesor, solo estoy trayendo la info 
        de la página principal, que si lo tiene, en está caso solo utilizo la sentencia
        para que me muestre el dato correspondido'''
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, p.apellido, c.descripcion FROM consulta c 
                           INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p ON c.id_profesor = p.id WHERE c.id_consulta=%s''', (id_consulta,))

        consulta = cursor.fetchall()
        cursor.close()
        payload_search = []
        for rows in consulta:
            result = {
                'nombre_estudiante': rows[0],
                'apellido_estudiante': rows[1],
                'programa': rows[4],
                'fecha': rows[6],
                'profesor': rows[7],
                'apellido_profesor': rows[8],
                'descripcion': rows[9]
            }
            payload_search.append(result)
        cursor.close()

        return render_template('profesor/editar_consulta.html', payload_search=payload_search)
    except Exception as e:
        return render_template('error.html', error_message=str(e))


@app.route('/aceptar/<int:id>', methods=['POST'])  # Aceptar consulta
def aceptar(id):
    id_consulta = id
    print(id_consulta)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * from consulta WHERE id_consulta=%s''', (id,))
    cons = cursor.fetchone()
    cursor.close()
    print(cons)
    if cons:
        id_const = cons[0]
        id_est = cons[1]
        id_profe = cons[2]
        fecha = cons[3]
        descripcion = cons[4]
        curs = mysql.connection.cursor()
        curs.execute('''INSERT INTO res_consulta (id_consulta, id_estudiante, id_profesor, fecha, asunto, modalidad, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                     (id_consulta, id_est, id_profe, fecha, descripcion, 'Presencial', 'Aceptado'))
        msg = 'Se actualizo la consuta correctamente    '
        mysql.connection.commit()
        curs.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_profe', msg=msg))


@app.route('/declinar/<int:id>', methods=['POST'])  # Declinar consulta
def declinar(id):
    id_consulta = id
    print(id_consulta)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * from consulta WHERE id_consulta=%s''', (id,))
    cons = cursor.fetchone()
    cursor.close()
    print(cons)
    if cons:
        id_const = cons[0]
        id_est = cons[1]
        id_profe = cons[2]
        fecha = cons[3]
        descripcion = cons[4]
        curs = mysql.connection.cursor()
        curs.execute('''INSERT INTO res_consulta (id_consulta, id_estudiante, id_profesor, fecha, asunto, estado) VALUES (%s, %s, %s, %s, %s, %s)''',
                     (id_consulta, id_est, id_profe, fecha, descripcion, 'Declinado'))
        msg = 'Se actualizo la consuta correctamente    '
        mysql.connection.commit()
        curs.close()
        msg = 'La consulta se ha actualizado correctamente!'
    return redirect(url_for('index_profe', msg=msg))


# Actualiza i/u guardar Consulta estudiante by profesor
@app.route('/update_res_cons', methods=['POST'])
def update_res_cons():

    if request.method == 'POST':

        nombre_est = request.form['nombre_estudiante']
        profesor = request.form['profesor']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        modalidad = request.form['modalidad']
        estado = request.form['estado']
        cons = mysql.connection.cursor()
        cons.execute('SELECT * FROM profesor WHERE nombre = %s',
                     [str(profesor)])
        result = cons.fetchone()
        if result:
            id_profesor = result[0]
            print(id_profesor)
        cons.close()
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM estudiante WHERE nombre = %s',
                    [str(nombre_est)])
        res = con.fetchone()
        if res:
            global id_est  # Id_estudiante
            id_est = res[0]
            print(id_est)
        con.close()
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO res_consulta (id_consulta, id_estudiante, id_profesor, fecha, asunto, modalidad, estado) VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)''', (str(id_consulta), str(id_est), str(id_profesor), str(fecha), str(descripcion), str(modalidad), str(estado)))
        msg = 'Se actualizo la consuta correctamente    '
        mysql.connection.commit()
        cur.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_profe', msg=msg))


# Registrar Profesor (Pendiente)

 # Cerrar sesion
@app.route('/logout')
def logout():
    # removemos los datos de la sesión para cerrar sesión
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('correo', None)
    session.pop('contraseña', None)
    session.clear()

    # session.cookies.clear()
    return redirect(url_for('index'))


def status_401(error):
    return render_template('login')


def status_404(error):
    return '<h1>Página no encontrada</h1>', 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    # login_manager.init_app(app)
    app.run(port=5000, debug=True)
