from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from entities.account import Account
from entities.log import Log
from entities.transaction import Transaction
from entities.user import User
from persistence.db import get_connection
from dotenv import load_dotenv
import os

from enums.Valuepermission import ValuePermission
from enums.log_type import LogType
from enums.profile_type import ProfileType

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

# Para pasar los enums a los templates
@app.context_processor
def inject_enums():
    return dict(ValuePermission=ValuePermission)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    return render_template('index.html')

@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    return render_template('signup.html')

@app.route('/welcome')
@login_required
def welcome():
    account = Account.get_account_by_id(current_user.id)
    balance = account.get_saldo() if account else 0
    return render_template('welcome.html', account=account, balance=balance)

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin():
        return redirect(url_for('welcome'))
    logs = Log.get_all_logs()
    return render_template('admin.html', logs=logs)

# NUEVAS RUTAS PROTEGIDAS POR PERMISOS
@app.route('/customer/edit')
@login_required
def customer_edit_panel():
    if not current_user.has_permission(ValuePermission.CUSTOMER_EDIT):
        return redirect(url_for('welcome'))
    return render_template('customer_edit.html')

@app.route('/customer/delete')
@login_required
def customer_delete_panel():
    if not current_user.has_permission(ValuePermission.CUSTOMER_DELETE):
        return redirect(url_for('welcome'))
    return render_template('customer_delete.html')

@app.route('/account/manage')
@login_required
def account_manage_panel():
    if not current_user.has_permission(ValuePermission.ACCOUNT):
        return redirect(url_for('welcome'))
    return render_template('account_manage.html')

@app.route('/transactions/commit')
@login_required
def transaction_commit_panel():
    if not current_user.has_permission(ValuePermission.TRANSACTION_COMMIT):
        return redirect(url_for('welcome'))
    return render_template('transaction_commit.html')

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo ya está registrado."}), 409

    if User.save(name, email, password):
        return jsonify({"success": True, "message": "Cuenta creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Error al crear cuenta."}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)
    if user:
        if user.is_active:
            login_user(user)
            Log.save_log(user, f"Inicio de sesión exitoso desde IP: {request.remote_addr}", LogType.LOGIN)
            return jsonify({
                "success": True, 
                "message": "Inicio de sesión exitoso.",
                "redirect": url_for('welcome')
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Su cuenta ha sido desactivada. Comuníquese con el administrador del sistema"
            }), 403
    else:
        return jsonify({
            "success": False,
            "message": "Los datos de acceso no son correctos."
        }), 401

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()