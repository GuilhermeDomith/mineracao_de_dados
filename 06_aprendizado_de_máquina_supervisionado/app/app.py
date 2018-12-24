from flask import Flask, request, render_template, jsonify
import noticia as n

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        noticia = request.form['noticia']

        if noticia:
            pred, proba = n.predict_notices(noticia)
            print('Probabilidade: ', proba[0])
            if(proba[0][1] > 0.950):
                print('-->', True)
                return render_template('index.html', esporte=True, porcentagem=int(proba[0][1]*100))
            else:
                print('-->', False)
                return render_template('index.html', esporte=False, porcentagem=int(proba[0][0]*100))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)