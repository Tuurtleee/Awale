from flask import Flask, request, redirect, g, render_template, session, jsonify
import genetique as gen
import recuit_simule as recuit
import tabou as tabou
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recuit_iterations = int(request.form['recuit_iter'])
        recuit_temperature = float(request.form['recuit_temp'])
        gen_iterations = int(request.form['genetic_iter'])
        gen_popsize = float(request.form['genetic_popsize'])
        gen_mutprob = float(request.form['genetic_mutation'])
        taboo_iterations = int(request.form['taboo_iter'])
        taboo_taille = int(request.form['taboo_taille'])
        config_genetique, gen_val = gen.run(gen_popsize, gen_iterations, gen_mutprob)
        config_recuit, rec_val = recuit.run(recuit_iterations, recuit_temperature)
        config_tabou, tab_val = tabou.run(taboo_iterations, taboo_taille)
        return render_template('index.html', range_4=range(4), range_10=range(10), config_genetique=config_genetique, config_recuit=config_recuit, config_tabou=config_tabou, gen_val=gen_val, rec_val=rec_val, tab_val=tab_val)
    config_genetique, gen_val = gen.run(100, 10, 0.1)
    config_recuit, rec_val = recuit.run(10, 100)
    config_tabou, tab_val = tabou.run(10, 100)
    print(config_genetique)
    return render_template('index.html', range_4=range(4), range_10=range(10))

if __name__ == '__main__':
    app.run(debug=True)