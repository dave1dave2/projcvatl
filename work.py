from flask import Flask, render_template, url_for, flash, request, redirect

from flask_mysqldb import MySQL
import os
from pathlib import Path
#pour importer les fichiers
from werkzeug import secure_filename


app = Flask(__name__)
app.secret_key = 'hello'
"""
#variable pour télecharger nos fichiers
uploads_dir = os.path.join(work.instance_path, 'uploads')
os.makedirs(uploads_dir, exists_ok=True)"""
#deuxième methodes  uploa contient le chemin et allowed les exentions
UPLOAD_FOLDER = '/dos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'xlsx', 'jpg', 'jpeg', 'docx'}

#variable de connexion à mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'd@ve1234'
app.config['MYSQL_DB'] = 'dave'



mysql = MySQL(app)
#mysql.init_app(app)

#focntion de verifcation de l'extension du fichier
def allowed_file(filename):

    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/acceuil')
def acceuil():
   
    return render_template('formpage.html')
"""
# être connecter à une session
@app.route('/session')
def session():
    if 'login' in session :
        use = session ['login']

        return render_template('projet.html')

    return "Session out" """

#se connecter à un comp^te utilisateur
@app.route('/connexion', methods=['GET','POST'])
def connexion():
    if request.method == "POST":
        user = request.form['login']
        passw = request.form['passwor']
        # avoir le curseur dans BD
        #cur = mysql.get_db().cursor()
        
        cur = mysql.connection.cursor()
        cur.execute("select * from user where username =%s and password = %s",(user,passw))
        result = cur.fetchone()
        if result :

            return render_template('projet.html',use=user)
        
        else :
            return 'BAD PASSWORD'


        cur.close()
        
    return render_template('connexion.html')




#route pour deposer les dossiers de validation
@app.route('/projet',methods=['GET','POST'])
def projet():
    cur = mysql.connection.cursor()
    if request.method == "POST" :
        namechefprojet = request.form['namechefprojet']
        descrip = request.form['descproj']
        date = request.form['date']
        fichier = UPLOAD_FOLDER 
        fich = request.files["files"]
        fich1 = request.files["files1"]
        
        
        # Si aucun fichier n'est selectionné
        if fich.filename == '' and fich.filename == '':
            flash('No selected file')
            return "aucun fifichier selectionner"
        
        
        
        #enregistrer le fichier
        if fich and fich1 and allowed_file(fich.filename):
            #pour le premier fichier
            filename = secure_filename(fich.filename)
            save_proj = namechefprojet+'_'+descrip+'_'+filename
            fich.save(os.path.join('dos', save_proj))

            #pour le deuxième fichier
            filename = secure_filename(fich1.filename)
            save_proj = namechefprojet+'_'+descrip+'_'+filename
            fich1.save(os.path.join('dos', save_proj))

            
            cur.execute("INSERT INTO projet(chefprojet,description ,publication ,repertoire) VALUES (%s, %s, %s, %s)", (namechefprojet, descrip,date,fichier))
            mysql.connection.commit()
            cur.close()
            return "fichier download"
        
        #si l'extension du fichier n'est pas pris en compte 
        if fich.filename != ALLOWED_EXTENSIONS and fich1.filename != ALLOWED_EXTENSIONS:
            flash('No selected file')
            return "l'éxtension n'est pas prise en compte"
        #filename = secure_filename(fich)
        """
        fich.save(os.path.join(app.config[UPLOAD_FOLDER],filename))
        cur.execute("INSERT INTO user(chefprojet,description ,publication ,repertoire) VALUES (%s, %s, %s, %s)", (chefp, descrip,date,fichier))
        mysql.connection.commit()
        cur.close()
            
        return "enregistrement non effectuer" """
 
    return render_template('projet.html')

# créer un compte utilisateur
@app.route('/compte', methods=['GET','POST'])
def compte():
    cur = mysql.connection.cursor()
    if request.method == "POST" :
        username = request.form['newuser']
        passw = request.form['passw']
        passw1 = request.form['password1']
        
        cur.execute("select * from user where username =%s ",[username])
        #cur.execute("select * from user where username= %s ",(username))
        verif = cur.fetchone()
        if not verif :
            #verification de la correspondance du mot de passe
            if passw1 == passw :
                cur.execute("INSERT INTO user(username, password) VALUES (%s, %s)", (username, passw))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('connexion'))
            
            else :
                return "le mot de passe n'est pas correcte"

        else :
            return "cet utilisateur existe déja"   
    
    return render_template('compte.html')

@app.route('/test')
def test():
    return render_template('helo.html')

   

    




if __name__=="__main__" :
    app.run(debug=True)