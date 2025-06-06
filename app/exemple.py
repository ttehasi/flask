import json
from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    session
)
# from app.db.utils import (
#     add_user, 
#     get_user_by_id, 
#     get_all_users, 
#     update_user, 
#     detele_user
# )

# сначала данные хранились в файлах, потом способом хранения стали сессии

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SECRET_KEY'] = 'ecdeew'

# users = json.load(open("app/users.json", 'r'))


@app.route('/')
def index():
    return '<div style="width: 100vh; margin: 0 auto"><a style="font-size: 10vh;" href="/users">Пользователи</a></div>'


@app.route('/users')
def users_get():
    messages = get_flashed_messages(with_categories=True)
    # with open("app/users.json", "r") as f:
    #     users = json.load(f)
    users = session.get('users', [])
    if users == []:
        users = [{'id':1, 'name':'egor gr', 'email': 'sosAL@da.com'}, {'id':2, 'name':'egor sin', 'email': 'ikari_sinkin@net.re'}]
    # users = get_all_users() база данных
    leng = len(users)
    term = request.args.get('term', '')
    filtered_users = [user for user in users if term in user['name']]
    return render_template(
        'index.html',
        users=filtered_users,
        search=term,
        messages=messages,
        leng=leng
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'new.html',
            user=user_data,
            errors=errors,
        ), 422
    if session.get('users') is None:
        session['users'] = [{'id':1, 'name':'egor gr', 'email': 'sosAL@da.com'}, {'id':2, 'name':'egor sin', 'email': 'ikari_sinkin@net.re'}]
    # else:
    #     if not session['users']:
    #         users = session['users']
    users = session['users']
    if not users:
        session['users'] = [{'id':1, 'name':'egor gr', 'email': 'sosAL@da.com'}, {'id': 2, 'name': 'egor sin', 'email': 'ikari_sinkin@net.re'}]
        user = {
            'id': 3,
            'name': str(user_data['name']),
            'email': user_data['email']
        }
    else:
        user = {
            'id': session['users'][-1]['id'] + 1,
            'name': str(user_data['name']),
            'email': user_data['email']
        }
    session['users'].append(user)
    # add_user(user_data['name'], user_data['email']) база данных
    flash('Пользователь успешно добавлен', 'success')
    return redirect(url_for('users_get'), code=302)
    # with open('app/users.json') as file:
    #     users = json.load(file)
    # if users:
    #     id = users[-1]['id'] + 1
    # else:
    #     id = 1
    # user = {
    #     'id': id,
    #     'name': str(user_data['name']),
    #     'email': user_data['email']
    # }
    # users.append(user)
    # with open("app/users.json", "w") as f:
    #     json.dump(users, f)
    # flash('Пользователь успешно добавлен', 'success')
    # return redirect(url_for('users_get'), code=302)


@app.route('/users/<int:id>/edit')
def edit_user(id):
    # with open('app/users.json', 'r') as file:
    #     users = json.load(file)
    users = session.get('users', [])
    user = ser = next((user for user in users if user['id'] == id), 'User not found')
    if user == 'User not found':
        return user, 404
    # user = get_user_by_id(id) база данных
    if user:
        errors = {}
        return render_template(
            'edit.html',
            errors=errors,
            user=user
        )
    else:
        return 'User not found', 404
    

@app.route('/users/<int:id>/patch', methods=['POST'])
def patch_user(id):
    # with open('app/users.json', 'r') as file:
    #     users = json.load(file)
    users = session.get('users')
    user = next(user for user in users if user['id'] == id)
    # user = get_user_by_id(id) база данных
    data = request.form.to_dict()
    
    errors = validate(data)
    if errors:
        return render_template(
            'edit.html',
            errors=errors,
            user=user
        ), 422
    user['email'] = data['email']
    user['name'] = data['name']
    # for us in users:
    #     if us['id'] == user['id']:
    #         us = user
    # with open('app/users.json', 'w') as file:
    #     json.dump(users, file)
    # update_user(id, data['name'], data['email']) база данных 
    flash("Пользователь успешно обновлен", "success")
    return redirect(url_for('users_get'))


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'new.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<int:id>')
def users_show(id):
    # with open("app/users.json", "r") as f:
    #     users = json.load(f)
    users = session.get('users', [])
    user = next((user for user in users if id == user['id']), 'User not found')
    # user = get_user_by_id(id) база данных
    if user == 'User not found':
        return user, 404 
    if user:  
        return render_template(
            'show.html',
            user=user,
        )
    else:
        return 'User not found'


@app.route('/users/<int:id>/delete', methods=['POST'])
def user_delete(id):
    # with open('app/users.json', 'r') as file:
    #     users = json.load(file)
    users = session.get('users', []) 
    user = next((i for i in users if i['id'] == id), 'User not found')
    if user == 'User not found':
        return user
    users.pop(users.index(user))
    # with open('app/users.json', 'w') as file:
    #     json.dump(users, file)
    # detele_user(id) база данных
    flash('Пользователь удален', 'success')
    return redirect(url_for('users_get'))


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

@app.errorhandler(404)
def not_found(error):
    return 'Not found!', 404