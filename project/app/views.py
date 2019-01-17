from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access
from app import appbuilder, db
from flask_appbuilder.models.group import aggregate_count
from flask_babel import lazy_gettext as _
from .models import ContactGroup, Gender, Contact, EmployeeTable
from .forms import MyForm
import json
import logging
import requests
import tabulate
import ast
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import (Blueprint, request, make_response, jsonify)


engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()




def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()





class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group': 'Contacts Group'}
    list_columns = ['name','designation', 'personal_celphone', 'birthday', 'contact_group.name']
 
    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name','gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]




class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]



class MyView(BaseView):

    route_base = "/api/v1"
    
    @expose('/empdata', methods=['GET','POST'])
    def employee_data(self):
        emp_data = session.query(Contact).filter().all()
        surveylist = []
        for i in emp_data:   
           surveylist.append({'name' : i.name})
        return json.dumps(surveylist)


class GetApi(BaseView):
    route_base = "/api/v1"
    @expose('/getdata', methods=['GET'])
    def get_data(self):
        url = "http://localhost:8080/api/v1/empdata"
        response = requests.request("GET", url)
        data = json.loads(response.text)
        ult_list = ast.literal_eval(json.dumps(data))
        header = ult_list[0].keys()
        rows =  [x.values() for x in ult_list]
        return tabulate.tabulate(rows, header, tablefmt='rst')


db.create_all()
fill_gender()
appbuilder.add_view_no_menu(MyView())
appbuilder.add_view_no_menu(GetApi())
appbuilder.add_view(GroupModelView, "Departments",icon='fa-envelope')
appbuilder.add_view(ContactModelView,"About Me", icon="fa-phone")
appbuilder.add_link("List Bangalore Employee", href='/api/v1/getdata',icon="fa-envelope ", category='Menu')
#appbuilder.add_link("Google", href="https://www.google.com/", icon = "fa-google-plus")


##############################################













