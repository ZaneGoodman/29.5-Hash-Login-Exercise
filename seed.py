from models import db,  connect_db, User, Feedback
from app import app



db.drop_all()
db.create_all()


User.query.delete()


user1 = User(username="zane", password="$2b$12$sKYAE05nDhjYPc1Yx4qsE.t9gtx5BjGtgpIOisVWMiBaTckt1qmjW", email="123@icloud.com", first_name="zane", last_name="evens")
user2 = User(username="bob", password="$2b$12$cWYN1luwvwHf.iEwkTzjsuHrAVG8Mq/hlCOSdqST5wYnKFXjJWC9W", email="bob@gmail.com", first_name="bob", last_name="hale")
user3 = User(username="ashley", password="$2b$12$23Yeu3wPLQOjQOsbVE0PzuqTvpEhR64iql/rYkd8EyZqk8fLk1ohe", email="ash123@aol.com", first_name="ashley", last_name="loot")



fb1 = Feedback(title="Chucky Cheese", content="Disappointed with my last experience at Chucky Cheese", username="zane")
fb2 = Feedback(title="Walmart", content="Walmarts new flooring system is very effecient", username="bob")
fb3 = Feedback(title="Target", content="Target is on its way down in stock price", username="ashley")

db.session.add_all([user1,user2,user3])
db.session.commit()

db.session.add_all([fb1,fb2,fb3])
db.session.commit()