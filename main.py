import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user

from forms.goods import GoodsForm
from forms.search import SearchForm
from forms.users import RegisterForm, LoginForm
from forms.favs_b import FavsForm
from forms.ords_b import OrdsForm
from forms.add import AddForm
from forms.pay import PayForm
from data.goods import Goods
from data.users import User
from data.association import Association
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

favs = []
ords = []
res = []


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
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)


@app.route("/", methods=['GET', 'POST'])
def index():
    global favs, ords, res
    res.clear()
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    a = db_sess.query(Association)
    if current_user.is_authenticated:
        for i in goods:
            for j in a:
                if current_user.id == j.user_id:
                    if i.id == j.favs_id:
                        favs.append(i.id)
                    if i.id == j.orders_id:
                        ords.append(i.id)
    return render_template("main.html", title='Главная страница', goods=goods,
                           favs=favs, ords=ords,
                           form2=form)


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    global ords, res

    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    summ = 0
    for i in goods:
        if i.id in ords:
            summ += i.cost

    return render_template("basket.html", title='Корзина', goods=goods,
                           ords=ords, summ=summ, form2=form)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    global ords, res
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    summ = 0
    for i in goods:
        if i.id in ords:
            summ += i.cost

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form3 = PayForm()
    if form3.validate_on_submit():
        return redirect('/')

    return render_template("pay.html", title='Оплата', goods=goods,
                           ords=ords, summ=summ, form2=form2, form3=form3)


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    global favs, res

    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    return render_template("favorites.html", title='Избранное', goods=goods,
                           favs=favs, form2=form)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    global favs, ords, res
    form = SearchForm()
    if form.validate_on_submit():
        res.clear()
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    # form.button.data true - false
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)

    return render_template('search_results.html', title='Результаты поиска',
                           res=res, form2=form,
                           goods=goods,
                           favs=favs, ords=ords)


@app.route("/categories/<int:r>", methods=['GET', 'POST'])
def cat(r):
    global favs, ords, res
    sl = {1: 'Телевизоры', 2: 'Смартфоны', 3: 'Одежда', 4: 'Обувь',
          5: 'Игрушки'}
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    col = 0
    for i in goods:
        if i.category == sl[r]:
            col += 1
    return render_template("categories.html", title='Поиск по категориям',
                           goods=goods, favs=favs,
                           ords=ords,
                           form2=form, cat=sl[r], col=col)


@app.route("/product/<int:r>", methods=['GET', 'POST'])
def product(r):
    global favs, ords, res
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    for i in goods:
        if i.id == r:
            tl = i.title
    return render_template("product.html", title=f'{tl}', goods=goods,
                           favs=favs,
                           ords=ords,
                           form2=form, i_id=r)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global favs, res

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", form2=form2)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   form2=form2)
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           form2=form2)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global favs, res

    form2 = SearchForm()
    if form2.validate_on_submit():
        db_sess = db_session.create_session()
        goods = db_sess.query(Goods)
        for i in goods:
            if str(form2.ttle.data).lower() in str(i.title).lower():
                res.append(i.id)
        return redirect('/search_results')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               form2=form2)
    return render_template('login.html', title='Авторизация', form=form,
                           form2=form2)


if __name__ == '__main__':
    main()
