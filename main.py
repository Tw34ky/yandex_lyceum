from flask import Flask
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
import werkzeug
import datetime
from flask import render_template
from data.jobs import Jobs
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()
    '''
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()
    # здесь я заполнил ДБ

    job_names = ['Soil Sample Analysis', 'Solar Panel Calibration', 'Subsurface Ice Survey', 'Atmospheric Data Upload',
                 'Rover Maintenance – Unit R2']
    job_leaders = ['Dr. Lena Hoshino', 'Eng. Mark Duvall', 'Dr. Arun Thakkar', 'Lt. Rachel Kim', 'Tech. Omar Velasquez']
    job_collaborations = [f'{random.randint(0, 15)}, {random.randint(0, 15)}',
                          f'{random.randint(0, 15)}, {random.randint(0, 15)}',
                          f'{random.randint(0, 15)}, {random.randint(0, 15)}',
                          f'{random.randint(0, 15)}, {random.randint(0, 15)}',
                          f'{random.randint(0, 15)}, {random.randint(0, 15)}']
    jobs_done = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1),
                 random.randint(0, 1)]
    work_durations = ['3.5', '6', '2.25', '4.75', '5.5']
    for i in range(5):
        job = Jobs()
        job.team_leader = job_leaders[i]
        job.job = job_names[i]
        job.collaborations = job_collaborations[i]
        job.is_finished = jobs_done[i]
        job.duration = work_durations[i]
        db_sess.add(job)
    db_sess.commit()
    '''


@app.route("/index")
def index():
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", news=jobs)


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
        return werkzeug.redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
