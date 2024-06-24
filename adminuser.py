from app import db
from models import User

admin_user = User(username='admin', email='admin@example.com')
admin_user.password = 'Skush@1987'  # This will hash the password
admin_user.is_admin = True
db.session.add(admin_user)
db.session.commit()

