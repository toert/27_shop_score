from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta, date

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Orders(db.Model):
    __tablename__ = 'orders'


@app.route('/')
def score():
    undone_orders_query = Orders.query.filter(Orders.confirmed.is_(None)).order_by(Orders.created)
    done_today = len(Orders.query.filter(func.date(Orders.confirmed) == date.today()).all())
    score = datetime.today() - undone_orders_query.first().created
    score_in_string = '{}:{}:{}'.format(score.days * 24 + score.seconds // 3600,  # hours
                                        (score.seconds % 3600) // 60,  # minutes
                                        score.seconds % 60)  # seconds
    if score > timedelta(minutes=30):
        color = 'firebrick'
    elif score > timedelta(minutes=7):
        color = 'darkgoldenrod'
    else:
        color = 'darkgreen'
    return render_template('score.html',
                           now=datetime.today(),
                           seven_minutes=timedelta(minutes=7),
                           thirty_minutes=timedelta(minutes=30),
                           orders=undone_orders_query.all(),
                           done_today=done_today,
                           score=score_in_string,
                           color=color)


if __name__ == "__main__":
    app.run()
