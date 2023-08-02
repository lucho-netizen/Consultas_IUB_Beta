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


@app.route('/index_admin')
def index_admin():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM profesor')
    profesor = cursor.fetchall()
    print(profesor)
    cursor.close()
    curs = mysql.connection.cursor()
    curs.execute('SELECT id_profesor, COUNT(*) AS repeticiones FROM consulta GROUP BY id_profesor')
    cons = curs.fetchone()
    print(cons)
    return render_template('admin/index.html', profesor = profesor, cons = cons)


@app.route('/login_profe') #Login_Profe_URL
def login_profe():
    return render_template('profesor/login.html')


@app.route('/contacto') #contactanos_URL
def contacto():
    return render_template('contactanos/index.html')


#registro_URL_Estudiante
@app.route('/registro') 
def registro():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM programas')
        programa=cursor.fetchall()
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
            date = {"id": row[0], "tipo":row[1]}
            docs.append(date)
            # print(docs)
        
        return render_template('estudiante/registro.html', program=program, docs=docs)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    

#Login_Est_URL
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
        cursor.execute('''SELECT est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, p.apellido, 
                       c.descripcion FROM consulta c INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p ON 
                       c.id_profesor = p.id WHERE c.descripcion LIKE %s AND c.id_profesor=%s''', (f"%{search}%", id_profe))

        datos = cursor.fetchall()
        cursor.close()
        payload_search = []
        for rows in datos:
            result = {
                'nombre_estudiante': rows[0],
                'apellido_estudiante': rows[1],
                'tipo_documento': rows[2],
                'numero_estudiante': rows[3],
                'programa': rows[4],
                'correo': rows[5],
                'fecha': rows[6],
                'descripcion': rows[9]
            }
            payload_search.append(result)

    try:    
        cursor = mysql.connection.cursor() 
        cursor.execute('''SELECT est.nombre, est.apellido, est.tipo_documento, est.numero_estudiante, est.programa, est.correo, c.fecha, p.nombre, 
                       p.apellido, c.descripcion FROM consulta c INNER JOIN estudiante est ON c.id_estudiante = est.id INNER JOIN profesor p 
                       ON c.id_profesor = p.id WHERE id_profesor=%s''', (id_profe,))
        dato = cursor.fetchall()
        cursor.close()
        payload = []
        for row in dato:
            result = {
                'nombre_estudiante': row[0],
                'apellido_estudiante': row[1],
                'tipo_documento': row[2],
                'numero_estudiante': row[3],
                'programa': row[4],
                'correo': row[5],
                'fecha': row[6],
                'descripcion':row[9]
            }
            payload.append(result)

        page = int(request.args.get(get_page_parameter(), 1))
        per_page = 10  # Cantidad de resultados por página
        offset = (page - 1) * per_page
        pagination = Pagination(page=page, per_page=per_page, total=len(payload), css_framework='bootstrap5')

        return render_template('profesor/index.html', payload=payload[offset:offset + per_page], id_profe=id_profe, pagination=pagination, payload_search=payload_search)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})



# Registrar profesor
@app.route('/register')  
def register():
    datos = ['', '', '', '']
    return render_template('admin/register.html', datos=datos)



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
            data = {"id" :rows [0],"nombre" :rows[1], "apellido":rows[2]}
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
        cursor.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_est', msg=msg))


# Index Estudiante
@app.route('/index_est', methods=['GET', 'POST'])
def index_est():
    id_est = session['id']
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
                    'tipo_documento': rows[2],
                    'numero_estudiante': rows[3],
                    'programa': rows[4],
                    'correo': rows[5],
                    'fecha': rows[6],
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
                'tipo_documento': row[2],
                'numero_estudiante': row[3],
                'programa': row[4],
                'correo': row[5],
                'fecha': row[6],
                'profesor': row[7],
                'apellido_profesor':row[8],
                'descripcion':row[9]
                }
                payload.append(data)
            
            #Paginación
            page = int(request.args.get(get_page_parameter(), 1))
            per_page = 10  # Cantidad de resultados por página
            offset = (page - 1) * per_page
            pagination = Pagination(page=page, per_page=per_page, total=len(payload), css_framework='bootstrap5')

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
        cursor.execute('SELECT * FROM administrador WHERE correo = %s AND contraseña = %s', (correo, contraseña))
        user = cursor.fetchone()
        print(user)
        if user:

            return redirect(url_for('index_admin'))
        else:
            msg = 'Los datos ingresados son incorrectos'
            return render_template('admin/login.html', msg=msg)


@app.route('/login_p', methods=['POST']) #Login_Profesor
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

        
@app.route('/ver_casos')
def ver_casos():
    # user = session['identificacion']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM profesor")
    v_casos = cursor.fetchall()
    return render_template('profesor/ver_casos.html', v_casos = v_casos)


@app.route('/res_cons', methods=['POST']) #Registrar Consulta estudiante
def res_cons():
    user = session['id']
    print(user)
    if request.method == 'POST':
        profesor = request.form['profesor']
        modulo = request.form['modulo']
        consulta = request.form['consulta']
        fecha = request.form['fecha']
        cons = mysql.connection.cursor()
        cons.execute('SELECT * FROM profesor WHERE nombre = %s', [str(profesor)])
        result = cons.fetchone()
        if result:
            id_profesor = result[0]
            print(id_profesor)
        cons.close()
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM modulo WHERE nombre_modulo = %s', [str(modulo)])
        res = con.fetchone()
        if res:
            global id_modulo
            id_modulo = res[0]
            print(id_modulo)
        con.close()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO consulta (id_estudiante, id_profesor, fecha, descripcion, id_modulo) VALUES (%s, %s, %s, %s, %s)',(user, id_profesor, fecha, consulta, id_modulo))
        mysql.connection.commit()
        cur.close()
        msg = 'La consulta se ha realizado correctamente!'
    return redirect(url_for('index_est', msg=msg))


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
