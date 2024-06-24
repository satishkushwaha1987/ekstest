from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import db, User, S3Bucket
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@admin_bp.route('/add-user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        aws_access_key_id = request.form.get('aws_access_key_id')
        aws_secret_access_key = request.form.get('aws_secret_access_key')
        is_admin = request.form.get('is_admin') == 'on'
        
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin.add_user'))

        new_user = User(
            username=username, 
            email=email, 
            password=password,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            is_admin=is_admin
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_user.html')

@admin_bp.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('admin.html', users=users)

@admin_bp.route('/admin/add_bucket', methods=['POST'])
def add_bucket():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return redirect(url_for('index'))

    user_id = request.form.get('user_id')
    aws_access_key_id = request.form.get('aws_access_key_id')
    aws_secret_access_key = request.form.get('aws_secret_access_key')
    bucket_name = request.form.get('bucket_name')

    new_bucket = S3Bucket(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        bucket_name=bucket_name,
        user_id=user_id
    )
    db.session.add(new_bucket)
    db.session.commit()
    flash('Bucket added successfully!', 'success')
    return redirect(url_for('admin.admin'))

