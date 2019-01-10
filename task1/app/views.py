from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access
from app import appbuilder, db
from flask_appbuilder.models.group import aggregate_count
from flask_babel import lazy_gettext as _
from .models import ContactGroup, Gender, Contact, EmployeeTable
from .forms import MyForm
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access



################################################

# engine = create_engine("postgresql://scott:tiger@localhost/test")
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()

class MyView(BaseView):
    # datamodel = SQLAInterface(EmployeeTable)
    route_base = "/api/v1"
    #list_columns = ['name', 'designation', 'job_location']

    # @expose('/method3/', methods=['GET', 'POST'])
    # @has_access
    # def method3(self):
    #     #form = MyForm()
    #      return self.render_template('form.html')

    @expose('/empdata', methods=['GET'])
    def employee_data(self):
	    # emp_data = EmployeeTable.query.filter().all()
        #emp_data = db.EmployeeTable.filter_by(name=designation).first()
        #emp_data = db.query(EmployeeTable).filter_by(name=designation).first()
        #emp_data = db.session.query(EmployeeTable).all()
        emp_data = session.query(EmployeeTable).filter().all()
        print('emp_data',emp_data)
        return json.dumps(emp_data)
                  


# appbuilder.add_view(MyView(), "Form", href='/myview/method3', category='My View')
# appbuilder.add_view(MyView(), href='/empdata') 
appbuilder.add_view_no_menu(MyView())


#################################################

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
    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group.name']
 
    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]



class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]



db.create_all()
fill_gender()
appbuilder.add_view(GroupModelView, "Departments",icon='fa-envelope')
appbuilder.add_view(ContactModelView,"About Me", icon="fa-phone")
appbuilder.add_link("Google", href="https://www.google.com/", icon = "fa-google-plus")


##############################################


'''
class EmployeeModelView(ModelView):
    datamodel = SQLAInterface(Employee)

   # label_columns = {'contact_group': 'Contacts Group'}
    list_columns = ['name', 'designation', 'job_location']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'designation', 'job_location']}),
               ]


#@expose('/method5/<string:param1>')
#@has_access
appbuilder.add_view(EmployeeModelView(), "Employee List", icon="fa-envelope", category="My View")
#appbuilder.add_view(EmployeeModelView(), "Employee List",icon="fa-envelope", href='/myview/method5/anjali', category='My View')
'''


##############################################



class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'Form successfully submitted'


    def form_get(self, form):
        form.field1.data = 'This was prefilled'


    def form_post(self, form):
        flash(self.message, 'info')



appbuilder.add_view(MyFormView, "Form", icon="fa-envelope")



################################################








