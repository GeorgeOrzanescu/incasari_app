from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, StringField
from wtforms.validators import DataRequired, ValidationError
import datetime
from flask_weasyprint import HTML, render_pdf

from BNR_scrape import  curs_zi, curs_ieri

# Configs
app=Flask(__name__)


app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Function for validation
def integer_validator(IncasareForm,suma):
    
    if isinstance(suma.data,float) is False :
        raise ValidationError('Numar invalid')

# Database
class Incasare(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    departament_incasare = db.Column(db.String)
    tip_abonament = db.Column(db.String(40),default='')
    mod_plata = db.Column(db.String)
    nume = db.Column(db.String)
    suma = db.Column(db.Integer)
    date = db.Column(db.String)
    profesor = db.Column(db.String,default='')
    tip_client = db.Column(db.String,default='')

class Cheltuieli(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    suma = db.Column(db.Integer)
    nume = db.Column(db.String)
    date = db.Column(db.String)
    serviciu = db.Column(db.String)

class Raport(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    numerar = db.Column(db.Integer)
    card = db.Column(db.Integer)
    date = db.Column(db.String)

# Forms
class TipIncasare(FlaskForm):
    tip = SelectField('Tip incasare',choices=[(0,'Piscina'),(1,'Balet'),(2,'Dans'),(3,'Party'),(4,'Cheltuieli')])
    submit = SubmitField('Submit')

class AlteIncasari(FlaskForm):
    modplata = SelectField('Modalitate plata',choices=[(0,'Numerar'),(1,'Card'),(2,'Op')])
    suma = FloatField('Suma',[integer_validator])
    nume = StringField('Nume client',[DataRequired()])
    serviciu = StringField('Serviciu')
    submit = SubmitField('Inregistreaza Incasare')

class IncasarePiscinaForm(FlaskForm):
    modplata = SelectField('Modalitate plata',choices=[(0,'Numerar'),(1,'Card'),(2,'Op')])
    suma = FloatField('Suma',[integer_validator])
    nume = StringField('Nume client',[DataRequired()])
    profesor = SelectField('Profesor',choices=[(0,'Name 1'),(1,'Name 2'),(2,'Name 3'),(3,'Name 4'),(4,'Name 5'),(5,'Name 6'),(6,'Name 7'),(7,'Name 8'),(8,'Name 9'),(9,'Name 10'),(10,'Name 11'),(11,'Name 12'),(12,'Name 13'),(13,'Name 14'),(14,'Name 15'),])
    tip_abonament=SelectField('Tip abonament',choices=[(0,'Afternoon 1 luna/4 sedinte'),(1,'Afternoon 1 luna/8 sedinte'),(2,'Happy Hour 1 luna /4 sedinte'),(3,'Happy Hour 1 luna/8 sedinte'),(4,'Baby Express 1 luna/4 sedinte'),(5,'Baby Express 1 luna/8 sedinte'),(6,'Initiere si perfectionare 1 luna/4 sedinte'),(7,'Initiere si perfectionare 1 luna/8 sedinte')])
    tip_client = SelectField('Tip client',choices=[(0,'Prelungire'),(1,'Client nou')])
    submit = SubmitField('Inregistreaza Incasare')

class RaportZ(FlaskForm):
    raportz_numerar = FloatField('Raport Z Restaurant numerar',[integer_validator])
    raportz_card = FloatField('Raport Z Restaurant card',[integer_validator])
    submit = SubmitField('Inregistreaza RaportZ')

class ReplaceIncasare(FlaskForm):
    select_id = FloatField('Id',[integer_validator])
    submit = SubmitField('Sterge incasare!')
    
# Routes

@app.route('/',methods=["GET","POST"])
def main():
    form = TipIncasare()
    form1 = RaportZ()

    if form1.validate_on_submit():
        raport = Raport(numerar=form1.raportz_numerar.data,card=form1.raportz_card.data,date=datetime.datetime.today().strftime("%d/%m/%Y"))
        db.session.add(raport)
        db.session.commit()
        print("succes")
        flash('Raport Z inregistrat cu success!','success')
        return redirect(url_for('main'))
    elif form.tip.data == '0':
        flash('Completeaza campurile !','warning')
        return redirect(url_for('piscina'))
    elif form.tip.data == '1':
        flash('Completeaza campurile !','warning')
        return redirect(url_for('balet'))
    elif form.tip.data == '2':
        flash('Completeaza campurile !','warning')
        return redirect(url_for('dans'))
    elif form.tip.data == '3':
        flash('Completeaza campurile !','warning')
        return redirect(url_for('party'))
    elif form.tip.data == '4':
        flash('Completeaza campurile !','warning')
        return redirect(url_for('cheltuieli'))
    

    total = sum(y.suma for y in Incasare.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_numerar= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Numerar",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_card= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Card",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_op= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Op",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    cheltuieli = sum(y.suma for y in Cheltuieli.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")))
    raport = Raport.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")).first()
    

    return render_template('main.html',form=form,form1=form1,date=datetime.datetime.today().strftime("%d/%m/%Y"),total=total,total_numerar = total_numerar,total_card = total_card,total_op=total_op ,cheltuieli=cheltuieli,raport=raport,curs_zi=curs_zi,curs_ieri=curs_ieri)



@app.route('/piscina',methods=["GET","POST"])
def piscina():
    form = IncasarePiscinaForm()

    if form.validate_on_submit():
        incasare = Incasare(departament_incasare='piscina',tip_abonament=form.tip_abonament.choices[int(form.tip_abonament.data)][1],mod_plata=form.modplata.choices[int(form.modplata.data)][1],nume=form.nume.data,suma=form.suma.data,date=datetime.datetime.today().strftime("%d/%m/%Y"),profesor=form.profesor.choices[int(form.profesor.data)][1],tip_client=form.tip_client.choices[int(form.tip_client.data)][1])
        
        db.session.add(incasare)
        db.session.commit()

        flash('Incasare inregistrata!','success')
        return redirect(url_for('main'))

    return render_template('piscina.html',form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))

@app.route('/balet',methods=["GET","POST"])
def balet():
    form = AlteIncasari()

    if form.validate_on_submit():
        incasare = Incasare(departament_incasare='Balet',mod_plata=form.modplata.choices[int(form.modplata.data)][1],suma=form.suma.data,nume=form.nume.data,tip_abonament=form.serviciu.data,date=datetime.datetime.today().strftime("%d/%m/%Y"))

        db.session.add(incasare)
        db.session.commit()

        flash('Incasare inregistrata!','success')
        return redirect(url_for('main'))

    return render_template('balet.html',form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))

@app.route('/dans',methods=["GET","POST"])
def dans():
    form = AlteIncasari()

    if form.validate_on_submit():
        incasare = Incasare(departament_incasare='Dans',mod_plata=form.modplata.choices[int(form.modplata.data)][1],suma=form.suma.data,nume=form.nume.data,tip_abonament=form.serviciu.data,date=datetime.datetime.today().strftime("%d/%m/%Y"))

        db.session.add(incasare)
        db.session.commit()

        flash('Incasare inregistrata!','success')
        return redirect(url_for('main'))

    return render_template('dans.html',form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))

@app.route('/party',methods=["GET","POST"])
def party():
    form = AlteIncasari()

    if form.validate_on_submit():
        incasare = Incasare(departament_incasare='Party',mod_plata=form.modplata.choices[int(form.modplata.data)][1],suma=form.suma.data,nume=form.nume.data,tip_abonament=form.serviciu.data,date=datetime.datetime.today().strftime("%d/%m/%Y"))

        db.session.add(incasare)
        db.session.commit()

        flash('Incasare inregistrata!','success')
        return redirect(url_for('main'))

    return render_template('party.html',form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))


@app.route('/cheltuieli',methods=["GET","POST"])
def cheltuieli():
    form = AlteIncasari()

    if form.validate_on_submit():
        cheltuiala = Cheltuieli(suma=form.suma.data,nume=form.nume.data,serviciu=form.serviciu.data,date=datetime.datetime.today().strftime("%d/%m/%Y"))
        db.session.add(cheltuiala)
        db.session.commit()

        flash('Cheltuiala inregistrata!','success')
        return redirect(url_for('main'))

    return render_template('cheltuieli.html',form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))


@app.route('/incasari_detaliat',methods=["GET","POST"])
def incasari_detaliat():
    form = ReplaceIncasare()
    incasari = (y for y in Incasare.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")))

    if form.validate_on_submit():
        to_delete = Incasare.query.filter_by(id=form.select_id.data).first()
        db.session.delete(to_delete)
        db.session.commit()

        flash('Incasare stearsa!--> reintrodu incasarea din pagina principala','warning')
        return redirect(url_for('incasari_detaliat'))
    
    return render_template('incasari_detaliat.html',incasari=incasari,form=form,date=datetime.datetime.today().strftime("%d/%m/%Y"))

@app.route('/raport_detaliat',methods=["GET","POST"])
def raport_detaliat():
    incasari_piscina = (y for y in Incasare.query.filter_by(departament_incasare ='piscina',date=datetime.datetime.today().strftime("%d/%m/%Y")))
    incasari_balet = (y for y in Incasare.query.filter_by(departament_incasare ='Balet',date=datetime.datetime.today().strftime("%d/%m/%Y")))
    incasari_dans= (y for y in Incasare.query.filter_by(departament_incasare ='Dans',date=datetime.datetime.today().strftime("%d/%m/%Y")))
    incasari_party= (y for y in Incasare.query.filter_by(departament_incasare ='Party',date=datetime.datetime.today().strftime("%d/%m/%Y")))
    incasari_cheltuieli= (y for y in Incasare.query.filter_by(departament_incasare ='Cheltuieli',date=datetime.datetime.today().strftime("%d/%m/%Y")))

    html = render_template('raport_detaliat.html',incasari_piscina=incasari_piscina,incasari_balet=incasari_balet,incasari_dans=incasari_dans,incasari_party=incasari_party,incasari_cheltuieli=incasari_cheltuieli,date=datetime.datetime.today().strftime("%d/%m/%Y"))

    return render_pdf(HTML(string=html),download_filename='report_detaliat.pdf', automatic_download=False)


@app.route('/print')
def printeaza():


    total = sum(y.suma for y in Incasare.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_numerar= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Numerar",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_card= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Card",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    total_op= sum(y.suma for y in Incasare.query.filter_by(mod_plata="Op",date=datetime.datetime.today().strftime("%d/%m/%Y")))
    cheltuieli = sum(y.suma for y in Cheltuieli.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")))
    raport = Raport.query.filter_by(date=datetime.datetime.today().strftime("%d/%m/%Y")).first()

    html = render_template('print.html',total=total,total_numerar = total_numerar,total_card = total_card,total_op=total_op ,cheltuieli=cheltuieli,raport=raport,date=datetime.datetime.today().strftime("%d/%m/%Y"))

    return render_pdf(HTML(string=html),download_filename='report.pdf', automatic_download=False)

    



if __name__ == "__main__":
    app.run(debug=True)
    
