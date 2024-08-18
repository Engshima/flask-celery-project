from flask import Flask, render_template,request, jsonify
from celery import Celery
from project import create_app, ext_celery
from project.users.tasks import generate_summary
from project.users.models import User



app = Flask(__name__)
app = create_app()

celery = ext_celery.celery
celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)



celery.conf.broker_connection_retry_on_startup = True



     
app = Flask(__name__)
@app.route('/templates', methods =['POST'])
def original_text_form():
		text = request.form['input_text']
		number_of_sent = request.form['num_sentences']
# 		print("TEXT:\n",text)
		summary = generate_summary(text,int(number_of_sent))
# 		print("*"*30)
# 		print(summary)
		return render_template('index1.html', title = "Summarizer", original_text = text, output_summary = summary, num_sentences = 5)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username , password)

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401


@app.route('/')
def homepage():
	title = "TEXT summarizer"
	return render_template('index1.html', title = title)


if __name__ == "__main__":
	app.debug = True
	app.run()

