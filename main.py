from os import abort

from flask import Flask, render_template, request, make_response, session
# noinspection PyUnresolvedReferences
from data import db_session
# noinspection PyUnresolvedReferences
from data.users import User
# noinspection PyUnresolvedReferences
from data.news import News
# noinspection PyUnresolvedReferences
from data.jobs import Jobs
# noinspection PyUnresolvedReferences
from forms.user import RegisterForm, LoginForm
# noinspection PyUnresolvedReferences
from forms.news import NewsForm
# noinspection PyUnresolvedReferences
from forms.jobs import JobsForm
from werkzeug.utils import redirect
import flask_login
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask import make_response, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    news = News()
    news.title = 'привет'
    news.content = 'пока'

    @app.route("/")
    def index():
        db_sess = db_session.create_session()
        if current_user.is_authenticated:
            news = db_sess.query(News).filter(
                (News.user == current_user) | (News.is_private != True))
        else:
            news = db_sess.query(News).all()  # db_sess.query(News).filter(News.is_private != True)
        return render_template("index_news.html", news=news)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
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
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/jobs')
    @login_required
    def add_jobs():
        form = JobsForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            jobs = Jobs()
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.is_finished = form.is_finished.data
            jobs.collaborations = form.collaborations.data
            jobs.duration = form.duration.data
            current_user.jobs.append(jobs)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('jobs.html', title='Добавление работы',
                               form=form)

    @app.route('/news', methods=['GET', 'POST'])
    @login_required
    def add_news():
        form = NewsForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = News()
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            current_user.news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('news.html', title='Добавление новости',
                               form=form)

    @app.route('/news/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_news(id):
        form = NewsForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id,
                                              News.user == current_user
                                              ).first()
            if news:
                form.title.data = news.title
                form.content.data = news.content
                form.is_private.data = news.is_private
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id,
                                              News.user == current_user
                                              ).first()
            if news:
                news.title = form.title.data
                news.content = form.content.data
                news.is_private = form.is_private.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('news.html',
                               title='Редактирование новости',
                               form=form
                               )

    @app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def news_delete(id):
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            db_sess.delete(news)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')

    db_session.global_init("db/blogs.db")

    app.run()


if __name__ == '__main__':
    main()
