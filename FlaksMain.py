from flask import Flask, render_template, request, jsonify

from characterCreation import character1, character2

from Mob_Generation_fix import *

import json

app = Flask(__name__, template_folder="templates")

@app.route('/character1')
def c1():
    jsoncharacter1 = json.dumps(character1.__dict__)
    response = jsonify(jsoncharacter1)
    response.headers['Content-Type'] = 'application/json'
    return response.json

@app.route('/character2')
def c2():
    jsoncharacter2 = json.dumps(character2.__dict__)
    response = jsonify(jsoncharacter2)
    response.headers['Content-Type'] = 'application/json'
    return response.json

@app.route('/mob')
def m():
    jsonmob = json.dumps(mob1.__dict__)
    response = jsonify(jsonmob)
    response.headers['Content-Type'] = 'application/json'
    return response.json

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('start.html')

@app.route('/fight_mob', methods=['GET', 'POST'])
def fight_mob():
    if mob1.health <= 0:
        character1.xp += mob1.xp
        character1.balance += 25
        mob1.__init__()
    mob1.take_damage(character1.critical_attack)
    character1.take_damage(mob1.critical_attack)
    character1.reset_attack()
    character1.reset_luck()

    if character1.xp >= 100:
        character1.level += 1
        character1.xp -= 100

    if character1.health <= 0:
        return render_template('game_over.html')

    return render_template('fight_mob.html', character=character1, mob=mob1)


@app.route('/fight_character', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'c1damage' in request.form:
            if request.form['c1damage'] == 'damage':
                character1.take_damage(character2.critical_attack)
                character2.take_damage(character1.critical_attack)
                character1.reset_attack()
                character2.reset_attack()
                character1.reset_luck()
                character2.reset_luck()

        if character1.health <= 0:
            character1.alive = False
            return render_template('winner.html', character=character2)
        if character2.health <= 0:
            character1.alive = False
            return render_template('winner.html', character=character1)

    return render_template('fight_character.html', character1=character1, character2=character2,)


if __name__ == "__main__":
    app.run(debug=True)
