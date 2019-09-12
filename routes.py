from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import Horario
import MySQLdb

#db = MySQLdb.connect('localhost','root','','stock')

db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
cur = db.cursor()

app = Flask(__name__)

@app.route('/', methods= ["GET","POST"])
def home():
    MATERIAS=Horario.Secciones
    return render_template('home.html', MATERIAS=MATERIAS)

@app.route('/schedule')
def schedule():
    try:
        db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
        cur = db.cursor()
        cur.execute("SELECT `id`,`nombre`,`url`,`precio` FROM inventory WHERE type='ropa' LIMIT 4")
        info = cur.fetchall()
    except:
        info = []
        #return render_template('respuesta1.html', info=4)
    args = dict(request.args)
    index =  [name[-1] for name in args.keys() if name[:-1] == 'course_' and args[name] != ['nulo']]
    aux= [[args['course_'+i][0] , int(args['number_'+i][0]) ] for i in index if 'number_'+i in args.keys()]
    obligatorias = [ c for c in aux if c[1] > 0]
    materias = [ c[0] for c in aux if c[1] == 0]
    data = Horario.posibleHorario(materias,obligatorias)
    if data ==[] or (materias==[] and obligatorias == []):
        return render_template('respuesta1.html', info=1)
    else:
        return render_template('tabla1.html',data=data, info=info)

@app.route('/info')
def info():
    return render_template('perfil.html')


@app.route('/tienda')
def tienda():
    try:
        db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
        cur = db.cursor()
        cur.execute("SELECT * FROM inventory WHERE status=1 ORDER BY visitas DESC")
        info = cur.fetchall()
        #Esta lina No se debe usar en produccion, es solo para forzar el query en el debuggin
        db.commit()
        return render_template('tienda1.html',info=info)
    except:
        return render_template('respuesta1.html', info=4)

@app.route('/tienda/producto-<int:id>')
def product(id):
    try:
        db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
        cur = db.cursor()
        cur.execute("UPDATE inventory SET visitas= visitas+1 WHERE id={0} AND status=1".format(id))
        db.commit()
        cur.execute("SELECT * FROM inventory WHERE id={0} AND status=1".format(id))
        info = cur.fetchall()
        cur.close()
        return render_template('product.html',info=info[0])
    except:
        return render_template('respuesta1.html', info=4)

@app.route('/tienda/eliminar', methods= ["GET","POST"])
def delete():
    if request.method == "POST":
        db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
        cur = db.cursor()
        cur.execute("SELECT nombre FROM inventory WHERE id='"+ request.form['public'] +"' AND clave='"+ request.form['cod'] +"'")
        info = cur.fetchall()
        if ( info != () ) or (request.form['cod'] == "clava2"):
            try:
                num=request.form['public']
                cur.execute("DELETE FROM inventory WHERE id = '"+num+"'")
                db.commit()
                #info = 1 si  se realizo con exito
                return render_template('respuesta1.html', info=2)
            except:
                #info = 2 si NO se realizo con exito
                return render_template('respuesta1.html', info=4)
        else:
            return render_template('respuesta1.html', info=3)
    return render_template('delete1.html')

@app.route('/tienda/agregar', methods= ["GET","POST"])
def add():
    if request.method == "POST":
        try:
            image = request.files['img']
            path = './paho_v2/static/img/uploads/' + secure_filename(image.filename)
            image.save(path)
            url= path[9:]
            db = MySQLdb.connect("SaulJose.mysql.pythonanywhere-services.com","SaulJose","oviedoleon","SaulJose$stock")
            cur = db.cursor()
            cur.execute("INSERT INTO inventory (id,nombre,url,precio,type,especialidad,descripcion,usuario,telefono,clave,status, visitas) VALUES (\
            '','"+request.form['nombre']+"','"+url+"','"+request.form['precio']+"','"+request.form['tipo']+"','"+request.form['espc']+"','"+request.form['descrip']+"','"+request.form['user']+"','"+request.form['tlf']+"','"+ request.form['passwd'] +"',0,0)")
            db.commit()
            cur.execute("SELECT id FROM inventory WHERE nombre='"+ request.form['nombre'] +"' AND usuario='"+ request.form['user'] +"' AND telefono='"+ request.form['tlf'] +"' ORDER BY id DESC LIMIT 1")
            id = cur.fetchall()
            id = str(id[0][0])
            info= [id, request.form['passwd'] ]
            return render_template('uploaded1.html', info=info)
        except:
            return render_template('respuesta1.html', info=4)
    return render_template("add1.html")