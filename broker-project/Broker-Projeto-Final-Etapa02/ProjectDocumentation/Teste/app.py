from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
from plotly.offline import plot

app = Flask(__name__)

@app.route('/')
def index():
    # Crie dados de exemplo
    data = {'x': [1, 2, 3, 4], 'y': [10, 11, 12, 13]}
    
    # Crie um gráfico usando Plotly Express
    fig = px.line(data, x='x', y='y', title='Gráfico de Linha Simples')
    
    # Salve o gráfico como HTML
    plot_div = pio.to_html(fig, full_html=False)

    return render_template('dashboard.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)