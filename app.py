from flask import Flask, request, render_template
from random import randint, choice, sample

# install debugtoolbar extension in ubuntu with pip then initialize it in the app
from flask_debugtoolbar import DebugToolbarExtension
# from flask import request
app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
debug = DebugToolbarExtension(app)

# add some docstrings
@app.route('/home')
def home_page():
    html = """
    <html>
        <body>
            <h1>Homepage!</h1>
            <p>Welcome to my simple app</p>
            <a href='/hello'>Go to hello page </a>
        </body>
    </html>
    """
    return render_template('home.html')

@app.route('/lucky')
def lucky_number():
    num = randint(1,10)
    return render_template('lucky.html', lucky_num=num, msg ="You are so lucky!")

@app.route('/form')
def show_form():
    return render_template("form.html")

@app.route('/form-2')
def show_form_2():
    return render_template("form_2.html")

COMPLIMENTS = ["cool", "clever", "tenacious", "awesome", "Pythonic"]


@app.route('/greet')
def get_greet():
    username = request.args["username"]
    nice_thing = choice(COMPLIMENTS)
    return render_template("greet.html", username=username, compliment = nice_thing)


# 
@app.route('/greet-2')
def get_greet_2():
    username = request.args["username"]
    # # below string doesn't work as it will return an error message. arg wants_compliments won't exist if unchecked. 
    # wants_compliments = request.args["wants_compliments"]
    # if its in there get it, if not don't throw error. Use get request for optional args
    wants = request.args.get("wants_compliments")
    nice_things = sample(COMPLIMENTS, 3)
    return render_template("greet_2.html", username = username, wants_compliments= wants, compliments=nice_things)

# @ is a decorator that demands a function declared right after
# funtion runs every time @app.route('something') is visited
@app.route('/hello/')
def say_hello():
    return render_template("hello.html")


@app.route('/goodbye')
def say_goodbye():
    return render_template("goodbye.html")

@app.route('/search')
def search():
    # print(request.args)
    # term and sort are contained within this route only
    term = request.args["term"]
    sort = request.args["sort"]
    # use term to find db data that matches term
    return f"<h1>Search Results for: {term} </h1> <p>Sorting by: {sort} </p>"


@app.route('/spell/<word>')
def spell_word(word):
    caps_word=word.upper()
    return render_template('spell_word.html', word=caps_word)



# @app.route("/post", methods=["POST"])
# def post_demo():
#     return "YOU MADE A POST REQUEST!"


# @app.route("/post", methods=["GET"])
# def get_demo():
#     return "YOU MADE A get REQUEST!"

# name attribute in html stores data when saved in server. name is key in kv pair
@app.route('/add-comment')
def add_comment_form():
    return """
        <h1>Add Comment </h1>
        <form method='POST'>
            <input type= 'text' placeholder='comment' name='comment'/>
            <input type= 'text' placeholder='username' name = 'username' />
            <button>Submit</button>
        </form>
    """

# can have 2 routes with same path if you want, but diff logic based off verb
@app.route('/add-comment', methods=["POST"])
def save_comment():
    comment = request.form["comment"]
    username = request.form["username"]
    print(request.form)
    return f"""
    <h1> saved your comment of {comment}</h1>
    <ul>
        <li> Username: {username} </li>
        <li> Comment: {comment} </li>
    </ul>

    """

# keyword arguement ('subreddit' below) inside braces is passed along to def show_subreddit
@app.route('/r/<subreddit>')
# above keyword arguement must match exactly keyword in function below
def show_subreddit(subreddit):
    return f"<h1>Browing the {subreddit} subreddit </h1>"



@app.route('/r/<subreddit>/comments/<int:post_id>')
def show_comments(subreddit, post_id):
    return f"<h1>viewing comments for post with id: {post_id} from the {subreddit} subreddit </h1>"



# mock data base
POSTS = {
    1:"I like chicken tenders",
    2:"I hate mayo!",
    3:"Double raindbow all the way",
    4:"YOLO OMG (kill me)"
}

# default data type is string, need to specify int (inlike js everything is a string)
# @app.route('/posts/<id>')
# will return not found if string passed in where expecting id
@app.route('/posts/<int:id>')
def find_post(id):    
    # post = POSTS[id]
    post = POSTS.get(id, "Post not found")
    return f"<p>{post}</p>"



# query param modifies the page, url param is subject of the page


# reddit badges - loop through each and show if applicable 
# if messages color orange
# if signed in show username else show sign up