from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.goods import GoodsForm
from forms.users import RegisterForm, LoginForm
from data.goods import Goods
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

favs = []
ords = []


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/db.db")
    app.run()


@app.route("/")
def index():
    global favs, ords
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    if current_user.is_authenticated:
        for i in current_user.favs_id.split(' '):
            favs.append(int(i))
        for j in current_user.orders_id.split(' '):
            ords.append(int(j))
    # if current_user.is_authenticated:
    #     user = db_sess.query(User)
    #     print(user)
    # else:
    #     return redirect('/login')
    return render_template("main.html", title='Главная страница', goods=goods, favs=favs, ords=ords)


@app.route('/basket')
def basket():
    global ords
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    summ = 0
    for i in goods:
        if i.id in ords:
            summ += i.cost
    return render_template("basket.html", title='Корзина', goods=goods, ords=ords, summ=summ)


@app.route('/favorites')
def favorites():
    global favs
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)

    # if current_user.is_authenticated:
    #     user = db_sess.query(User)

    return render_template("favorites.html", title='Избранное', goods=goods, favs=favs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
