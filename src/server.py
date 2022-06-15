from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "fakedooge"
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def form():
    return render_template('/form.html')

@app.route('/crawl',methods=['POST'])
def crawl():
    if request.method == 'POST':
        return crawl_for_post(request.form['URL'])
    else:
        return redirect('/')
    pass