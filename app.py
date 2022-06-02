
from flask import Flask,  render_template, request, redirect, url_for, session # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from os import path #pip install notify-py
from notifypy import Notify



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'app_medicenter'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("contenido.html")  


@app.route('/forgot_pass', methods = ["GET", "POST"])
def forgot_pass():

    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        
        if email == user["email"]:
            session['password'] = user['password']
                
            return render_template("paciente/pass.html")

        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="Correo no valido"
            notificacion.send()
            return render_template("forgot_pass.html")
        
    else:
        
        return render_template("forgot_pass.html")



@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")

@app.route('/nosotros', methods = ["GET", "POST"])
def nosotros():
    session.clear()
    return render_template("contenido.html")    

@app.route('/layout_session', methods = ["GET", "POST"])
def layout_session():
    session.clear()
    return render_template("contenido_session.html")




STATIC_URL = 'static/'
@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        rut = request.form['rut']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE rut=%s",(rut,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if password == user["password"]:
                session['name'] = user['name']
                session['rut'] = user['rut']
                session['password'] = user['password']
                
                if user["type"] == "secretaria":
                    session['type'] = user['type']
                    return render_template("secretaria/home_secretaria.html")
                
                elif user["type"] == "doctor":
                    session['type'] = user['type']
                    return render_template("doctor/home_doctor.html")

                else:
                    return render_template("paciente/home.html")

            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        
        return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()   
    cur.close()

    notificacion = Notify()
       
    if request.method == 'GET':
        return render_template("registro.html", users=users) 
    
    else:
        rut = request.form['rut']
        name = request.form['name']
        last_name = request.form['last_name']
        cellphone_num = request.form['cellphone_num']
        email = request.form['email']
        password = request.form['password']
        pass_confirmation = request.form['pass_confirmation']
        address = request.form['address']
        phone_num = request.form['phone_num']
        


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (rut,name,last_name,cellphone_num,email,password,pass_confirmation,address,phone_num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (rut,name,last_name,cellphone_num, email,password,pass_confirmation,address, phone_num)) 
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="ya te encuentras registrado en Dos Alamos, por favor inicia sesión para poder agendar una hora."
        notificacion.send()
        return redirect(url_for('login'))



@app.route('/horadoc', methods = ["GET", "POST"])
def horadoc():
    notificacion = Notify()

    if request.method == 'POST':
        specialty = request.form['specialty']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE specialty=%s",(specialty,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if specialty == user["specialty"]:
                session['name'] = user['name']
                session['last_name'] = user['last_name']
                
                if user["specialty"] == "general":
                    session['specialty'] = user['specialty']
                    return redirect(url_for('medico_g'))

            
                if user["specialty"] == "kinesiologo":
                    session['specialty'] = user['specialty']
                    return redirect(url_for('medico_k'))
            
                if user["specialty"] == "oftalmologo":
                    session['specialty'] = user['specialty']
                    return redirect(url_for('medico_of'))
                
                if user["specialty"] == "otorrino":
                    session['specialty'] = user['specialty']
                    return redirect(url_for('medico_ot'))

                else:
                    return render_template("secretaria/home_secretaria.html")

            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Especialidad no valida"
                notificacion.send()
                return render_template("secretaria/home_secretaria.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("secretaria/home_secretaria.html")
    else:
        
        return render_template("secretaria/horadoc.html") 






@app.route('/medico_g', methods = ["GET", "POST"])
def medico_g():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reserva")
    reserva = cur.fetchall()   
    cur.close()

    notificacion = Notify()
       
    if request.method == 'GET':
        return render_template("secretaria/medico_g.html", reserva=reserva) 
    
    else:
        specialty = request.form['specialty']
        doctor = request.form['doctor']
        medical_date = request.form['medical_date']
        medical_hour = request.form['medical_hour']
        


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reserva (specialty,doctor,medical_date,medical_hour) VALUES (%s,%s,%s,%s)", (specialty,doctor,medical_date,medical_hour)) 
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Las horas ya se encuentran registradas en Dos Alamos."
        notificacion.send()
        return redirect(url_for('horadoc'))



@app.route('/medico_k', methods = ["GET", "POST"])
def medico_k():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reserva")
    reserva = cur.fetchall()   
    cur.close()

    notificacion = Notify()
       
    if request.method == 'GET':
        return render_template("secretaria/medico_k.html", reserva=reserva) 
    
    else:
        specialty = request.form['specialty']
        doctor = request.form['doctor']
        medical_date = request.form['medical_date']
        medical_hour = request.form['medical_hour']
        


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reserva (specialty,doctor,medical_date,medical_hour) VALUES (%s,%s,%s,%s)", (specialty,doctor,medical_date,medical_hour)) 
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Las horas ya se encuentran registradas en Dos Alamos."
        notificacion.send()
        return redirect(url_for('horadoc'))



@app.route('/medico_of', methods = ["GET", "POST"])
def medico_of():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reserva")
    reserva = cur.fetchall()   
    cur.close()

    notificacion = Notify()
       
    if request.method == 'GET':
        return render_template("secretaria/medico_of.html", reserva=reserva) 
    
    else:
        specialty = request.form['specialty']
        doctor = request.form['doctor']
        medical_date = request.form['medical_date']
        medical_hour = request.form['medical_hour']
        


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reserva (specialty,doctor,medical_date,medical_hour) VALUES (%s,%s,%s,%s)", (specialty,doctor,medical_date,medical_hour)) 
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Las horas ya se encuentran registradas en Dos Alamos."
        notificacion.send()
        return redirect(url_for('horadoc'))



@app.route('/medico_ot', methods = ["GET", "POST"])
def medico_ot():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reserva")
    reserva = cur.fetchall()   
    cur.close()

    notificacion = Notify()
       
    if request.method == 'GET':
        return render_template("secretaria/medico_ot.html", reserva=reserva) 
    
    else:
        specialty = request.form['specialty']
        doctor = request.form['doctor']
        medical_date = request.form['medical_date']
        medical_hour = request.form['medical_hour']
        


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reserva (specialty,doctor,medical_date,medical_hour) VALUES (%s,%s,%s,%s)", (specialty,doctor,medical_date,medical_hour)) 
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Las horas ya se encuentran registradas en Dos Alamos."
        notificacion.send()
        return redirect(url_for('horadoc'))



if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True)