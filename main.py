import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user

from forms.search import SearchForm
from forms.users import RegisterForm, LoginForm
# from forms.add import AddForm for /add
from forms.pay import PayForm
from data.goods import Goods
from data.users import User
from data.association import Association
from data import db_session

# from forms.check import ChecksForm  # new

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secreret123123'

res = []
categories = ['Телевизоры', 'Смартфоны', 'Одежда', 'Обувь', 'Игрушки']


def get_favs():
    favs = []
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    a = db_sess.query(Association)
    if current_user.is_authenticated:
        for i in goods:
            for j in a:
                if current_user.id == j.user_id:
                    if i.id == j.favs_id:
                        favs.append(i.id)
    return favs


def get_ords():
    ords = []
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods)
    a = db_sess.query(Association)
    if current_user.is_authenticated:
        for i in goods:
            for j in a:
                if current_user.id == j.user_id:
                    if i.id == j.orders_id:
                        ords.append(i.id)
    return ords


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
    app.run(host='0.0.0.0', port=port)


# new
@app.route('/func_run')
def func_run():
    x = request.args.get('par_1')
    y = request.args.get('par_2')
    z = request.args.get('par_3')
    if z == '2':
        if y == 'true':
            db_sess = db_session.create_session()
            product = Association(
                user_id=int(str(current_user).split()[1]),
                favs_id=None,
                orders_id=int(x) - 100,
                o_count=1
            )
            db_sess.add(product)
            db_sess.commit()
        else:
            db_sess = db_session.create_session()
            a = db_sess.query(Association).filter(Association.user_id == int(str(current_user).split()[1]),
                                                  Association.orders_id == int(x) - 100).first()
            db_sess.delete(a)
            db_sess.commit()
    else:
        if y == 'true':
            db_sess = db_session.create_session()
            product = Association(
                user_id=int(str(current_user).split()[1]),
                favs_id=int(x),
                orders_id=None,
                o_count=None
            )
            db_sess.add(product)
            db_sess.commit()
        else:
            db_sess = db_session.create_session()
            a = db_sess.query(Association).filter(Association.user_id == int(str(current_user).split()[1]),
                                                  Association.favs_id == int(x)).first()
            db_sess.delete(a)
            db_sess.commit()
    return '', 204


@app.route("/", methods=['GET', 'POST'])
def index():
    global res, categories
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
    # form4 = FavsForm()
    # form4 = ChecksForm()  # new
    # if form4.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     assoc = Association(
    #         user_id=current_user.id,
    #         favs_id=form4.favs_id.data,
    #         orders_id=0,
    #         o_count=0
    #     )
    #     db_sess.add(assoc)
    #     db_sess.commit()
    return render_template("main.html", title='Главная страница', goods=goods,
                           favs=get_favs(), ords=get_ords(),
                           form2=form, cats=categories)


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    global res
    ords = get_ords()
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


#
# @app.route('/add', methods=['GET', 'POST'])
# def add():
#     form2 = SearchForm()
#     if form2.validate_on_submit():
#         db_sess = db_session.create_session()
#         goods = db_sess.query(Goods)
#         for i in goods:
#             if str(form2.ttle.data).lower() in str(i.title).lower():
#                 res.append(i.id)
#         return redirect('/search_results')
#
#     form3 = AddForm()
#     if form3.validate_on_submit():
#         db_sess = db_session.create_session()
#         product = Goods(
#             title=form3.title.data,
#             cost=form3.cost.data,
#             description=form3.description.data,
#             category=form3.category.data,
#             rate=form3.rate.data,
#             image=form3.image.data,
#         )
#         db_sess.add(product)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('add.html', title='Добавление товара', form2=form2,
#                            form3=form3)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    global res
    ords = get_ords()
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
    global res
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
                           favs=get_favs(), form2=form)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    global res, categories
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
                           favs=get_favs(), ords=get_ords(), cats=categories)


@app.route("/categories/<int:r>", methods=['GET', 'POST'])
def cat(r):
    global res, categories
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
        if i.category == categories[r - 1]:
            col += 1
    return render_template("categories.html", title='Поиск по категориям',
                           goods=goods, favs=get_favs(),
                           ords=get_ords(),
                           form2=form, cat=categories[r - 1], col=col, cats=categories)


@app.route("/product/<int:r>", methods=['GET', 'POST'])
def product(r):
    global res
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
                           favs=get_favs(),
                           ords=get_ords(),
                           form2=form, i_id=r)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global res

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
    global res

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


