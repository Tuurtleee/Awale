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
        gen_popsize = int(request.form['genetic_popsize'])
        gen_mutprob = float(request.form['genetic_mutation'])
        taboo_iterations = int(request.form['taboo_iter'])
        taboo_taille = int(request.form['taboo_size'])
        config_genetique, gen_val = gen.run(gen_popsize, gen_iterations, gen_mutprob)
        config_recuit, rec_val = recuit.run(recuit_iterations, recuit_temperature)
        config_tabou, tab_val = tabou.run(taboo_iterations, taboo_taille)
        new_gen_config = []
        new_rec_config = []
        new_tab_config = []
        for i in range(0, 4):
            temp_gen = []
            temp_rec = []
            temp_tab = []
            for j in range(10):
                if i*10+j < len(config_genetique):
                    temp_gen.append(config_genetique[i*10+j])
                else:
                    temp_gen.append('\0')
                if i*10+j < len(config_recuit):
                    temp_rec.append(config_recuit[i*10+j])
                else:
                    temp_rec.append('\0')
                if i*10+j < len(config_tabou):
                    temp_tab.append(config_tabou[i*10+j])
                else:
                    temp_tab.append('\0')
            new_gen_config.append(temp_gen)
            new_rec_config.append(temp_rec)
            new_tab_config.append(temp_tab)
        return render_template('index.html', range_4=range(4), range_10=range(10), config_genetique=new_gen_config, config_recuit=new_rec_config, config_tabou=new_tab_config, gen_val=gen_val, rec_val=rec_val, tab_val=tab_val, recuit_iterations=recuit_iterations, recuit_temperature=recuit_temperature, gen_iterations=gen_iterations, gen_popsize=gen_popsize, gen_mutprob=gen_mutprob, taboo_iterations=taboo_iterations, taboo_taille=taboo_taille)
    config_genetique, gen_val = gen.run(100, 10, 0.1)
    config_recuit, rec_val = recuit.run(10, 100)
    config_tabou, tab_val = tabou.run(10, 100)
    return render_template('index.html', range_4=range(4), range_10=range(10), config_genetique=config_genetique, config_recuit=config_recuit, config_tabou=config_tabou, gen_val=gen_val, rec_val=rec_val, tab_val=tab_val, recuit_iterations=10, recuit_temperature=100, gen_iterations=10, gen_popsize=100, gen_mutprob=0.1, taboo_iterations=10, taboo_taille=100)

if __name__ == '__main__':
    app.run(debug=True)