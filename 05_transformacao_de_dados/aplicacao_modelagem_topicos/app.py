from flask import Flask, request, render_template
import noticias, json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    busca = request.args.get('busca')
    if busca:
        lista_noticias = noticias.obter_noticias_similares(busca)
        return render_template('index.html', noticias= lista_noticias)

    return render_template('index.html', noticias=noticias.obter_lista_noticias_dict())
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)

