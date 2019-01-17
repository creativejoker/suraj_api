import datetime
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date

from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access



mindate = datetime.date(datetime.MINYEAR, 1, 1)




class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name




class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name




class Contact(Model):

    __tablename__ = "Contact"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")


    def __init__(self, **kwargs):
        super(Contact, self).__init__(**kwargs)

    def __repr__(self):
        #return self.name
        return "<Contact(name='%s', address='%s', birthday='%s',personal_phone='%s',personal_celphone='%s', contact_group='%s', gender='%s')>" % (self.name, self.address, self.birthday, self.personal_phone, self.personal_celphone, self.contact_group, self.gender)

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)       



class EmployeeTable(Model):

    __tablename__ = "employee_table"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    designation = Column(String(564))
    job_location = Column(String(564))  

    def __init__(self, **kwargs):
        super(EmployeeTable, self).__init__(**kwargs)

    def __repr__(self):
	    #return self.name
        return "<EmployeeTable(name='%s', designation='%s', job_location='%s')>" % (self.name, self.designation, self.job_location)
        


  





