from MAIN_APP import db, login_manager
from flask_login import UserMixin
from sqlalchemy import DateTime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)

    def check_password_correction(self, attempted_password):
        return User.query.filter_by(username=self.username, password=attempted_password).first()


class TodoList(db.Model):
    __tablename__ = 'TodoList'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=80), nullable=False)
    description = db.Column(db.String(length=500), nullable=False)
    owned_user = db.Column(db.Integer(), db.ForeignKey('User.id'))
    date_created = db.Column(db.DateTime(timezone=True), nullable=False)

    def delete_list_item(self):
        TodoList.query.filter_by(id=self.id).delete()
        db.session.commit()

    def update_activity(self, update_string):
        TodoList.query.filter_by(id=self.id).update({"description": update_string})
        db.session.commit()