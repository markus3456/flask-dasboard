#!/usr/bin/env python

from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    request, 
    session
)
from flask_wtf import FlaskForm
from wtforms import SelectField

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from app import create_app
from extract import extract
from calc import mon
import calc as calc

ptsbm, extra, giro ,ptsbc= extract()
    


a = ptsbm['balance'].tail(1)
b = extra['balance'].tail(1)
c = giro['balance'].tail(1)
d = ptsbc['balance'].tail(1)

tot = pd.concat([a,b,c,d], ignore_index=True)
owner = {'ptsb_marki' : a,'extra_marki':b,'giro_marki':c,'ptsb_cristinika':d}
total = pd.DataFrame(owner)
total = total.transpose()
total = total.reset_index()
total = total.set_axis(['acc','balance'], axis=1, inplace=False)
tot = total['balance'].sum()
tot = str(tot)

print(tot)
print(total)

a = calc.net()
print(a)

app = create_app()

class Form(FlaskForm):
    month = SelectField('month',choices=[   (1, 'January'),
                                            (2, 'Febuary'),
                                            (3, 'March'),
                                            (4, 'April'),
                                            (5, 'May'),
                                            (6, 'June'),
                                            (7, 'July'),
                                            (8, 'August'),
                                            (9, 'September'),
                                            (10, 'October'),
                                            (11, 'November'),
                                            (12, 'December'),])
                                    
class Form2(FlaskForm):
    acc = SelectField('acc', choices=[('ptsbm', 'ptsbm'),
                                        ('ptsbc', 'ptsbc'),
                                        ('giro', 'giro'),
                                        ('extra', 'extra'),])

class Form3(FlaskForm):
    year = SelectField('year', choices=[(2021),
                                        (2022),
                                        (2023)])


@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def index():

    #import forms for dropdown content
    form = Form()
    form2 = Form2()
    form3 = Form3()
    
    #fig2 pie-chart to vizualize allocation of tasks of each category
    labels = a['acc'].head(5).tolist()
    values = a['balance'].head(5).tolist()
    tot = a.iloc[-1]['balance']
    tot = tot.round(2)

    #print(labels)
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig2.update_layout(
        autosize=False,
        showlegend=False,
        width=300,
        height=150,
        margin=dict(l=5, r=5, t=1, b=1),
    )
    fig2.update_traces(hovertemplate=None, textposition='outside')
    fig2.add_annotation(dict(x=0.5, y=0.5,  align='center',
                        xref = "paper", yref = "paper",
                        showarrow = False,
                        text="{}???".format(tot)))

    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)



    if request.method == 'POST' and form2.acc.data is not None:

        #get data for monthly dropdowns
        acc = form2.acc.data                #will return string
        month = form.month.data             
        month = int(month)                  #convert to int
        
        #query account and month, create new dataframe 
        df_m = mon(acc,month,2022)
        
        #calculate sum of expenditures and amount of transactions
        a1 = round(sum(x for x in df_m["value"] if x < 0),2)
        a2 = len(df_m)
        print(a1)
        print(a2)

        #plot expenditure in bar-chart
        fig = px.bar(df_m, x='date', y='value',
                   hover_data=['value', 'authority'], 
                labels={'value':'value'})

        graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print('POST form2')
        return render_template('index.html', graphJSON=graphJSON,  graphJSON2=graphJSON2,   form=form ,form2=form2, form3=form3)

    if request.method == 'POST' and form3.year.data is not None:
        
        #get data anaual dropdowns
        year = form3.year.data
        year = int(year)
        print(year)


        #plot line chart for annual asset-growth
        start = 2021
        end = 2022
        df_y = calc.annual(giro,ptsbm,ptsbc,extra,start,end)
        fig3 = px.line(df_y, x="date", y="total")
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        print('POST form3')
        return render_template('index.html', graphJSON=graphJSON,  graphJSON3=graphJSON3, form=form ,form2=form2, form3=form3)
   
    

    

    #Bar Plot Month empty
    df_i = pd.DataFrame(columns=['date','value'])

    fig = px.bar(df_i, x='date', y='value',
                    
                labels={'value':'value'})

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    df_ii = pd.DataFrame(columns=['date','total'])
    fig3 = px.line(df_ii, x="date", y="total")
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    #ptsbm, extra, giro ,ptsbc
    acc = [{'acc': 'select acc'},
            {'acc': 'ptsbm'},
            {'acc': 'ptsbc'},
            {'acc': 'giro'},
            {'acc': 'extra'},]
    
    month = [{'month': 'Select Month'},
            {'month': 'January'},
            {'month': 'Febuary'},
            {'month': 'March'},
            {'month': 'April'},
            {'month': 'May'},
            {'month': 'June'},
            {'month': 'July'},
            {'month': 'August'},
            {'month': 'September'},
            {'month': 'October'},
            {'month': 'November'},
            {'month': 'December'},] 
    
    
    
    print('POST default')
    return render_template('index.html',  graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3, 
                            acc=acc, month=month, form=form, form2=form2, form3=form3) 


@app.route('/month', methods=["POST"])
def month():
    month12 = request.form.get("month")
    print(month12)
    return redirect(url_for("index"))

#     category=[{'category': 'Select Month'},{'category': 'January'},{'category': 'Febuary'},{'category':'March'}] 
#     return render_template('base.html' , category=category)

if __name__ == "__main__":
    app.run(debug=True)