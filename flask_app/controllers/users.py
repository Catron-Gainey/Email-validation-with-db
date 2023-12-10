from flask import render_template, request, redirect, session
from flask_app import app 
from flask_app.models.user import Users


@app.route('/')
def main_page():
    return render_template('create.html') 

@app.route('/create', methods=['POST'])
def create_user():
    # if there are errors:
    # We call the staticmethod on Burger model to validate
    if not Users.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    # else no errors:
    user_id= Users.save(request.form)
    return redirect(f'/read/one/{user_id}')

# @app.route('/', methods=['POST'])
# def register():
#     if not Users.validate_user(request.form):
#         # we redirect to the template with the form.
#         return redirect('/')
#     # ... do other things
#     return redirect('/dashboard')

# @app.route('/create', methods=['POST'])
# def create():
#     user_id= Users.save(request.form)
#     return redirect(f'/read/one/{user_id}')

@app.route('/read/all')
def read_all():
    my_users = Users.get_all()
    return render_template("read_all.html", my_users = my_users)

@app.route('/read/one/<int:id>')
def read_one(id):
    user = Users.get_one_user(id)
    return render_template("read_one.html", user = user)

@app.route('/edit/<int:id>')
def edit(id):
    return render_template('edit.html', user=Users.get_one_user(id))

@app.route('/update/<int:id>',methods=['POST'])
def update_user(id):
    user_dict = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email":request.form["email"],
        "id":id
        }
    Users.update(user_dict)
    return redirect(f'/read/one/{id}')

@app.route('/delete/<int:id>')
def delete(id):
    Users.delete(id)
    return redirect('/read/all')

