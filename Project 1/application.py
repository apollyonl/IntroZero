import os
from flask import Flask, render_template, request, session, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "whatever"
app.permanent_session_lifetime=timedelta(minutes=60)
engine = create_engine("postgres://fedglbab:1RTzmSrJiG9GzKOjYJPJtUSiXs1EWgN2@drona.db.elephantsql.com:5432/fedglbab")
#engine = create_engine('postgresql://postgres:1234@localhost:5432/project1')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        books = db.execute("SELECT * FROM books WHERE isbn like :search OR year like :search OR title like :search OR author like :search",{"search": "%"+search.strip()+"%"}).fetchall()
        if(not books):
            books = db.execute("SELECT * FROM books WHERE isbn like :search OR year like :search OR title like :search OR author like :search",{"search": "%"+search.capitalize().strip()+"%"}).fetchall()
            if(not books):
                books = db.execute("SELECT * FROM books WHERE isbn like :search OR year like :search OR title like :search OR author like :search",{"search": "%"+search.upper().strip()+"%"}).fetchall()
                if(not books):
                    books = db.execute("SELECT * FROM books WHERE isbn like :search OR year like :search OR title like :search OR author like :search",{"search": "%"+search.lower().strip()+"%"}).fetchall()
            
        return render_template("index.html",books=books)
    else:
        books = db.execute("SELECT * FROM books").fetchall()
        return render_template("index.html", books=books)
        
    
    
@app.route("/log_in", methods=["GET","POST"])
def log_in():
    #Obtenemos el nombre del usuario
    if request.method == 'POST':
        user = request.form.get("user")
        password = request.form.get("password")
        try:
            if(user and password):
                userdb = db.execute("SELECT user_id,password FROM users WHERE user_id = :user_id",{"user_id": user}).fetchall()
                if(user == userdb[0][0] and password == userdb[0][1]):
                    session.permanent=True
                    session['user'] = user
                    return redirect('/')
                else:
                    return render_template("log_in.html",message="Contraseña Incorrecta")
            else:
                return render_template("log_in.html",message="Porfavor llene todos los campos")
        except:
           return render_template("log_in.html",message="Usuario no encontrado")
    else: 
        return render_template("log_in.html")
    
    
@app.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == 'POST':
        user = request.form.get("user")
        lname = request.form.get("lname").strip().capitalize()
        fname = request.form.get("name").strip().capitalize()
        name = fname + ' ' + lname
        password = request.form.get("password")
        email = request.form.get("email")
       
        if(len(user) != 0 and len(name) != 0 and len(lname) != 0 and len(password) != 0 and len(email) != 0): 
            try:
                db.execute("INSERT INTO users (user_id, name, email, password) VALUES (:userdb, :namedb, :emaildb, :passworddb)", {"userdb": user, "namedb": name,"emaildb": email,"passworddb": password})               
                db.commit()
                return redirect('/log_in')
            except:
                db.close()
                return render_template("sign_up.html",message="Nombre de usuario en uso, Eljia otro porfavor")
        else:           
            return render_template("sign_up.html",message="PorFavor llene los campos",email=email,user=user,fname=fname,lname=lname,password=password)
    
        #return render_template("sign_up.html",message=f"hola {name} su contraseña es {password}")
    return render_template("sign_up.html")
@app.route("/book/<book_isbn>", methods=["GET","POST"])
def book(book_isbn):
    info = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": book_isbn}).fetchall()
    session.permanent=True
    session['isbn'] = info[0][0]
    session['title'] = info[0][1]
    session['author'] = info[0][2]
    session['year'] = info[0][3]
    isbn = session['isbn']
    title = session['title']
    author = session['author']
    year = session['year']
    reviews = db.execute("SELECT e.review, m.name, e.rating FROM reviews e INNER JOIN users m on e.user_id = m.user_id WHERE e.isbn = :isbndb;", {"isbndb": info[0][0],}).fetchall()
        #aqui me quede
    rating="";
    if(request.method == 'POST'):
        review = request.form.get('review')
        if(request.form.get('rating1')):
            rating = request.form.get('rating1')
        if(request.form.get('rating2')):
            rating = request.form.get('rating2')
        if(request.form.get('rating3')):
            rating = request.form.get('rating3')
        if(request.form.get('rating4')):
            rating = request.form.get('rating4')
        if(request.form.get('rating5')):
            rating = request.form.get('rating5')
        try:
            if(rating):
                db.execute("INSERT INTO reviews (review, rating, user_id, isbn) VALUES (:reviewdb, :ratingdb, :user_iddb, :isbndb)", {"reviewdb": review, "ratingdb": rating,"user_iddb": session['user'],"isbndb": info[0][0]})
                db.commit()
                reviews = db.execute("SELECT e.review, m.name,e.rating FROM reviews e INNER JOIN users m on e.user_id = m.user_id WHERE e.isbn = :isbndb;", {"isbndb": info[0][0],}).fetchall()
                return render_template("book.html",reviews=reviews,isbn=isbn,title=title,author=author,year=year)
            else:
                message="Favor de llenar todos los campos"
                reviews = db.execute("SELECT e.review, m.name,e.rating FROM reviews e INNER JOIN users m on e.user_id = m.user_id WHERE e.isbn = :isbndb;", {"isbndb": info[0][0],}).fetchall()
                return render_template("book.html",message = message,reviews=reviews,isbn=isbn,title=title,author=author,year=year)
            
        except:
            return render_template("book.html",message = "Favor de iniciar sesion para dejar su reseña",reviews=reviews,isbn=isbn,title=title,author=author,year=year)
        
    else:
        return render_template("book.html",reviews=reviews,isbn=isbn,title=title,author=author,year=year)
@app.route('/log_out')
def log_out():
    session.pop('user')
    return redirect('/')

"""
def main():
    user = "apol13"#request.form.get("user")
    password = 1234#request.form.get("password")
    #userdb = db.execute("SELECT user_id,password FROM users WHERE user_id = :user",{"user_id": user}).fetchone()
    users = db.execute("SELECT user_id,password FROM users WHERE user_id = :user_id",{"user_id": user}).fetchall()
   # for x in users:
    #    userdb = x.user_id
     #   passworddb = x.password
    #print(userdb,passworddb, user,password)
    if user == users[0][0]:
        print("hola")
    
if __name__ == "__main__":
    main()
    """
    
    
    