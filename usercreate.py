from app import app, db
from models import User

with app.app_context():
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin_password'

    if User.query.filter_by(email=email).first():
        print('Admin user already exists.')
    else:
        admin_user = User(username=username, email=email, is_admin=True)
        admin_user.password = password  # This will hash the password
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created.')

