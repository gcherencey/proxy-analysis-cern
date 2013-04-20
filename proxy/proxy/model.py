'''
Created on Jun 28, 2012

Module which create the object and map them for the database (Job,Site,Connection,Input)

@author: Gaylord Cherencey
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Column, Sequence
from sqlalchemy.types import Integer, String
import re

Base = declarative_base()

class Input(Base):
    '''Class which describe a input :
    - <<PK>> id_Input : Integer
    - <<FK>> id_Job : Integer
    - name : String
    '''

    __tablename__ = 'inputs'
    id_Input = Column(Integer, Sequence('input_id_seq'), primary_key=True)
    id_Job = Column(Integer, ForeignKey('jobs.id_Job'),index=True)
    name = Column(String)

    def __init__(self, name):

        self.name = name

class Connection(Base):
    '''Class which describe a connection :
    - <<PK>> id_Connection : Integer
    - <<FK>> id_Job : Integer
    - time : String
    - DB : String
    '''

    __tablename__ = 'connections'
    id_Connection = Column(Integer, Sequence('connection_id_seq'), primary_key=True)
    id_Job = Column(Integer, ForeignKey('jobs.id_Job'),index=True)
    time = Column(String)
    DB = Column(String)

    def __init__(self, time, DB):

        self.time = time
        self.DB = DB

    def __repr__(self):

        return "Site: id_Job({0}), time({1}))".format(
                self.id_Job, self.time)

class Job(Base):
    '''Class which describe a job :
    - id_Job <<PK>>
    - id_Site <<FK>>
    - name : String
    - relationship with Input table
    - relationship with Connection table
    '''

    __tablename__ = 'jobs'
    id_Job = Column(Integer, Sequence('job_id_seq'), primary_key=True)
    id_Site = Column(Integer, ForeignKey('sites.id_Site'),index=True)
    name = Column(String)

    inputs = relationship("Input", backref="jobs")
    connections = relationship("Connection", backref="jobs")

    def __init__(self, name):

        self.name = name

    def __repr__(self):

        return "Job: id_Job({0}), id_Site({1}))".format(
                self.id_Job, self.id_Site)

class Site(Base):
    '''Class which describe a site :
    - <<PK>> id_Site : Integer
    - name : String
    - relationship with Job table
    '''

    __tablename__ = 'sites'
    id_Site = Column(Integer, Sequence('site_id_seq'), primary_key=True)
    name = Column(String,index=True)

    jobs = relationship("Job", backref="sites")

    def __init__(self, name):
        self.name = name

class DataBase(object):
    '''Class which declare the database and contains few methods to add data into it'''

    def __init__(self, filename):
        """Initialization of the database"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        self.filename = filename
        self.engine = create_engine('sqlite:///%s' % self.filename, echo=False)
        Base.metadata.create_all(self.engine)
        self._sessionMaker = sessionmaker(bind=self.engine)
        self.session = self._sessionMaker()
        self.all_site = {}

    def site(self, name):
        """Creation of the site object and add it to the database"""

        site = self.session.query(Site).filter(Site.name==name).first()
        if site is None:
            site = Site(name)
            self.session.add(site)
        return site

        self.session.commit()

    def add_Data(self, k, v):
        """"Add of the data into the database

            k -> name of the job
            v dictionary with the data ( { 'connections':[], 'inputs': [], 'site': '' } )
        """

        if v['site'] not in self.all_site.values():
            self.all_site[self.all_site.__len__()] = v['site']

        current_site = self.site(v['site'])

        if self.session.query(Job).filter(Job.name==k).first() is None :
            current_job = Job(k)

            for input_Element in v["inputs"]:
                #Check if this input object is already in the database or not
                if self.session.query(Input).filter(Input.name==input_Element).first() is None :
                    #if not we add it
                    current_input = Input(input_Element)
                    current_job.inputs.append(current_input)

            for connection in v["connections"]:
                result = re.split(r'(\S*)$', connection)
                #Check if this connection object is already in the database or not
                if self.session.query(Connection).filter(Connection.time==result[0]).first() is None :
                    #if not we add it
                    current_connection = Connection(result[0],result[1])
                    current_job.connections.append(current_connection)

            current_site.jobs.append(current_job)

        self.session.add(current_site)

        self.session.commit()