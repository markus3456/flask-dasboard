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
    

app = create_app()

class Form(FlaskForm):
    year = SelectField('year', choices=[(2021),(2022)])
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


@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def index():
    form = Form()
    
    #fig2 pie-chart to vizualize allocation of tasks of each category
    labels = total['acc'].tolist()
    values = total['balance'].tolist()
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
                        text="{}€".format(tot)))

    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)



    if request.method == 'POST':
        month = form.month.data
        month = int(month)
        print(type(month))
        #return '<h1>Month: {}</h1>'.format(form.month.data)
        
        df_m = mon(giro,month,2022)

        fig = px.bar(df_m, x='date', y='value',
                   hover_data=['value', 'authority'], 
                labels={'value':'value'})

        graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index.html', graphJSON=graphJSON,  graphJSON2=graphJSON2,  form=form)
   
    

    

    #Bar Plot Month
    df_i = pd.DataFrame(columns=['date','value'])

    fig = px.bar(df_i, x='date', y='value',
                    
                labels={'value':'value'})

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    
    month = [{'month': 'Select Month'},
            {'month': 'January'},
            {'month': 'Febuary'},
            {'month':'March'},
            {'month': 'April'},
            {'month': 'May'},
            {'month': 'June'},
            {'month': 'July'},
            {'month': 'August'},
            {'month': 'September'},
            {'month': 'October'},
            {'month': 'November'},
            {'month': 'December'},] 
    
    
    

    return render_template('index.html',  graphJSON=graphJSON, graphJSON2=graphJSON2, month=month, form=form) 


@app.route('/month', methods=["POST"])
def month():
    month12 = request.form.get("month")
    print(month12)
    return redirect(url_for("index"))

#     category=[{'category': 'Select Month'},{'category': 'January'},{'category': 'Febuary'},{'category':'March'}] 
#     return render_template('base.html' , category=category)

if __name__ == "__main__":
    app.run(debug=True)