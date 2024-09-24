from flask import Flask, request, redirect, url_for, render_template
# from flask_sqlalchemy import SQLAlchemy
from business_logic import UserService
from data_access import db, create_database_if_not_exists

app = Flask(__name__)

# MySQL's connection URI (you can store this in config.py for better structure)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@sqlserver/three_tier_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/three_tier_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection
create_database_if_not_exists()  # Creates database if it doesn't exist
db.init_app(app)
# Ensure tables are created
with app.app_context():
    db.create_all()


@app.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()  # Fetching all users
    return render_template('index.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return render_template('user_detail.html', user=user)  # Render userdetails.html with user data
    return render_template('error.html', message="User not found"), 404  # Show error page if user not found


@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.form
        UserService.create_user(data['name'], data['email'])
        return redirect(url_for('get_users'))
    return render_template('create_user.html')


@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return render_template('error.html', message="User not found"), 404

    if request.method == 'POST':
        data = request.form
        UserService.update_user(user_id, data['name'], data['email'])
        return redirect(url_for('get_users'))

    return render_template('edit_user.html', user=user)


@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return render_template('error.html', message="User not found"), 404

    UserService.delete_user(user_id)
    return redirect(url_for('get_users'))


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
