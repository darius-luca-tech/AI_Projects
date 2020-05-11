from model import InputForm
from flask import Flask, render_template, request
from compute import compute

app = Flask(__name__)


@app.route('/')
def index():
    # form = InputForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     result = compute(form.a.data, form.b.data,form.c.data, form.d.data,form.e.data,form.z.data,form.g.data,form.h.data,form.i.data)
    # else:
    #     result = None
    return render_template('header.html')


@app.route('/Acasa/')
def home():
    # form = InputForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     result = compute(form.a.data, form.b.data,form.c.data, form.d.data,form.e.data,form.z.data,form.g.data,form.h.data,form.i.data)
    # else:
    #     result = None
    return render_template('Acasa.html')

@app.route('/Sdc/', methods=['GET', 'POST'])
def usingdata():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = compute(form.a.data, form.b.data,form.c.data, form.d.data,form.e.data,form.z.data,form.g.data,form.h.data,form.i.data)
    else:
        result = None
    return render_template('Sdc.html', form=form, result=result)

@app.route('/Mai_multe_informatii/')
def moreinfo():
    # form = InputForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     result = compute(form.a.data, form.b.data,form.c.data, form.d.data,form.e.data,form.z.data,form.g.data,form.h.data,form.i.data)
    # else:
    #     result = None
    return render_template('Mai_multe_informatii.html')

@app.route('/Masuri_de_precautie/')
def preventivemeasures():
    # form = InputForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     result = compute(form.a.data, form.b.data,form.c.data, form.d.data,form.e.data,form.z.data,form.g.data,form.h.data,form.i.data)
    # else:
    #     result = None
    return render_template('Masuri_de_precautie.html')

if __name__ == '__main__':
    app.run(debug = True)
