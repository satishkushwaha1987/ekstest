from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    aws_access_key_id = db.Column(db.String(100))
    aws_secret_access_key = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_suspended = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class S3Bucket(db.Model):
    __tablename__ = 's3bucket'
    id = db.Column(db.Integer, primary_key=True)
    aws_access_key_id = db.Column(db.String(100), nullable=False)
    aws_secret_access_key = db.Column(db.String(100), nullable=False)
    bucket_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('s3_buckets', lazy=True))

class S3BucketForm(FlaskForm):
    aws_access_key_id = StringField('AWS Access Key ID', validators=[DataRequired()])
    aws_secret_access_key = StringField('AWS Secret Access Key', validators=[DataRequired()])
    bucket_name = StringField('Bucket Name', validators=[DataRequired()])
    user_id = HiddenField('User ID', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    aws_access_key_id = StringField('AWS Access Key ID', validators=[DataRequired()])
    aws_secret_access_key = StringField('AWS Secret Access Key', validators=[DataRequired()])
    submit = SubmitField('Add User')

