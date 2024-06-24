import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, User, S3Bucket
from admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(admin_bp)

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


@app.route('/admin', methods=['GET'])
def admin_panel():
    query = request.args.get('query')
    if query:
        users = User.query.filter(User.username.contains(query)).all()
    else:
        users = User.query.all()    
    return render_template('admin.html', users=users)

@app.route('/admin/search', methods=['GET'])
def admin_search():
    query = request.args.get('query')
    if query:
        users = User.query.filter(User.username.contains(query)).all()
    else:
        users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def admin_add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            aws_access_key_id=form.aws_access_key_id.data,
            aws_secret_access_key=form.aws_secret_access_key.data
        )
        new_user.set_password(form.password.data)  # Assuming you have a method to hash passwords
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_user.html', form=form)


@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    s3bucket = S3Bucket.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = True if request.form['is_admin'] == 'True' else False
        user.password = request.form['password']

        if s3bucket:
            s3bucket.aws_access_key_id = request.form['aws_access_key_id']
            s3bucket.aws_secret_access_key = request.form['aws_secret_access_key']
            s3bucket.bucket_name = request.form['bucket_name']
        else:
            new_s3bucket = S3Bucket(
                aws_access_key_id=request.form['aws_access_key_id'],
                aws_secret_access_key=request.form['aws_secret_access_key'],
                bucket_name=request.form['bucket_name'],
                user_id=user.id
            )
            db.session.add(new_s3bucket)

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin_panel'))
        except:
            db.session.rollback()
            flash('Error updating user!', 'danger')
            return redirect(url_for('admin_edit_user', user_id=user.id))
    return render_template('edit_user.html', user=user, s3bucket=s3bucket)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.password = password  # Using the password property to hash the password
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.aws_access_key_id or not user.aws_secret_access_key:
        flash('Missing AWS credentials. Please update your profile.', 'danger')
        return redirect(url_for('index'))
    
    logs = []
    buckets = []
    for bucket in user.s3_buckets:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=bucket.aws_access_key_id,
            aws_secret_access_key=bucket.aws_secret_access_key
        )
        bucket_logs = get_s3_logs(bucket.aws_access_key_id, bucket.aws_secret_access_key, bucket.bucket_name)
        logs.extend(bucket_logs)
        buckets.append({'name': bucket.bucket_name, 'logs': bucket_logs})
    
    return render_template('dashboard.html', user=user, logs=logs, buckets=buckets)

@app.route('/download-log/<filename>')
def download_log(filename):
    file_path = os.path.join('logs', filename)
    return send_file(file_path, as_attachment=True)

def get_s3_logs(aws_access_key_id, aws_secret_access_key, bucket_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    logs = []
    for obj in response.get('Contents', []):
        log = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
        logs.append(log['Body'].read().decode('utf-8'))
    return logs

@app.route('/user/<int:user_id>/buckets')
def get_user_buckets(user_id):
    user = User.query.get(user_id)
    if user:
        buckets = S3Bucket.query.filter_by(user_id=user_id).all()
        return jsonify([bucket.bucket_name for bucket in buckets])
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/suspend_user/<int:user_id>', methods=['POST'])
def admin_suspend_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_suspended = not user.is_suspended
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_s3bucket/<int:s3bucket_id>', methods=['GET', 'POST'])
def edit_s3bucket(s3bucket_id):
    s3bucket = S3Bucket.query.get_or_404(s3bucket_id)
    form = S3BucketForm(obj=s3bucket)
    if form.validate_on_submit():
        s3bucket.aws_access_key_id = form.aws_access_key_id.data
        s3bucket.aws_secret_access_key = form.aws_secret_access_key.data
        s3bucket.bucket_name = form.bucket_name.data
        s3bucket.user_id = form.user_id.data
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_s3bucket.html', form=form)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

