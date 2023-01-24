from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    open_par = 0
    close_par = 0
    if request.method == "POST" and request.form.get('submit') == 'Submit':
        input = request.form['rule']
        rule_list = input.split("\n")
        new_list = []
        for x in rule_list:
            new_list.append(x.strip())
        rule_list = []
        for y in new_list:
            if y != "(and" and y != "(or" and y != "(if":
                for letter in y:
                    if letter == "(":
                        open_par += 1
                    elif letter == ")":
                        close_par +=1
                if close_par > open_par:
                    y = y[:-1]
                rule_list.append(y)

        output = '(let ['

        cond_number = 1

        for index, cond in enumerate(rule_list):
            if index == len(rule_list) - 1:
                output = output + f'condition{cond_number} (if {cond} "TRUE" "FALSE")'
            else:
                output = output + f'condition{cond_number} (if {cond} "TRUE" "FALSE") '
            cond_number += 1

        output = output + '] (str "'

        new_count = 1
        for index, cond in enumerate(rule_list):
            if '"' in cond:
                slash = "\ "[0]
                cond = cond.replace('"', f'{slash}"')
            if new_count < len(rule_list):
                output = output + f'{cond}: "condition{new_count}" '
            else:
                output = output + f'{cond}: "condition{new_count}""))'
            new_count += 1

        page = 2
        return render_template('rule.html', rule=output, page=page)
    
    elif request.method == "POST" and request.form.get('submit') == 'Compute':
        page = 3
        response = request.form['rule']
        list = response.split(" ")

        for index, item in enumerate(list):
            list[index] = item.strip()


        empty_list = []
        string = ""

        for letter in list[0]:
            empty_list.append(letter)
        empty_list.insert(0, '"')    
        list[0] = (string.join(empty_list))



        for index, x in enumerate(list):
            new_index = index
            if x.lower() == "true" or x.lower() == "false":
                if index != len(list) - 1:
                    index = index + 1
                    list[index] = f'"{list[index]}'
            if x.lower() == "true" or x.lower() == "false":
                new_index = new_index - 1
                a = []
                for letter in list[new_index]:
                    a.append(letter)
                a.insert(-1, '"')
                empty = ""
                list[new_index] = (empty.join(a))

        for index, x in enumerate(list):
            new_index = index
            if x.lower() == "true" or x.lower() == "false":
                list[index] = x + ','
                if index == len(list) - 1:
                    list[index] = x


        new_string = ' '.join(list)

        output = '{' + new_string + '}'
        return render_template('rule.html', page=page, output=output)
    
    else:
        page = 1
        return render_template('rule.html', page=page)
if __name__ == '__main__':
    app.run(debug=True)




    




