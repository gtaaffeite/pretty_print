import pandas as pd
import re

#import pdfkit 



certificate_list = {}
timetable = pd.DataFrame()


class certificate:  
    
    def __init__(self,units_queue,certificate): 
        
        self.local_semesters = pd.DataFrame() 
        self.certificate = certificate 
        self.units_queue = units_queue.sort_values(by=['exam_date'])
        
        for index, row in self.units_queue.iterrows():
            self.year = row['year']
            self.semester = row['semester']
            self.local_semesters = self.local_semesters.append({'year': self.year,'semester': self.semester}, ignore_index=True)
        self.local_semesters = self.local_semesters.drop_duplicates().sort_values(by=['year','semester'])
    
    
def create_certs(timetable, certificate_list):
    local_units_queue = pd.DataFrame()
    for index, row in timetable.iterrows():
        cert_key = row['certificate']
        if not certificate_list.get(cert_key):
            certificate_list.update({cert_key : None})
    for cert in certificate_list:
        local_units_queue = timetable.query('certificate == @cert')
        certificate_list[cert] = certificate(local_units_queue,cert)
    return

def pretty_print(certificate_list):
    to_html = ''
    for item in certificate_list: 
        to_html = f'<!DOCTYPE html> <html><head><title>{item}</title>'
        to_html = to_html + '<style> @media print {table, img, svg {break-inside: avoid;}} p.b {white-space: normal;}table {width:100%;} table, th, td { border: 1px solid black; border-collapse: collapse; }th, td { padding: 15px; text-align: left;}tr:nth-child(even) {background-color: #eee; }tr:nth-child(odd) {background-color: #fff;} p.lec {font-size: 0.67em;line-height: 0.1;}</style>   '
        to_html = to_html + f' </head><body> <h1>{item}</h1>'

                    
        cert = certificate_list[item]
        years = cert.local_semesters['year'].tolist()
        semesters = cert.local_semesters['semester'].tolist()
        myindex = len(years)
        for i in range(myindex):
            mysemester = semesters[i]
            myyear = years[i]
            sem_units = cert.units_queue.query('year == @myyear and semester == @mysemester')
            to_html = to_html + f'<table style="width:100%"><tr><th colspan="4">{item} | Year: {myyear} | Semester: {mysemester}</th></tr><tr><th>Unit Code</th><th>Unit Name</th> <th>Date</th> <th>Time</th><th>Facilitator</th></tr>'
            for index,row in sem_units.iterrows():
                exam_date = row['exam_date']
                day_week = row['day_week']
                exam_time = row['exam_time']
                certificate = row['certificate']
                year = row['year']
                semester = row['semester']
                unit_code = row['unit_code']
                unit_name = row['unit_name']
                lecturer = row['lecturer']
                to_html = to_html + f'<tr><td>{unit_code}</td><td>{unit_name}</td><td>{day_week}-{exam_date}</td><td>{exam_time}</td><td>{lecturer}</td></tr>' 



            to_html = to_html + '</table>'
            to_html = to_html + '<p class="b">...</p>'
           
        to_html = to_html + '</body></html>'
        af = open(f"{item}.html", "w")
        af.write(to_html)
        af.close()
        #pdfkit.from_file(f'{item}.html', f'{item}.pdf') 
                         
               
               

    return

def my_init(timetable,certificate_list):
    timetable = pd.read_csv ('master.csv')
    create_certs(timetable, certificate_list)  
    pretty_print(certificate_list)
    
    return
    
my_init(timetable,certificate_list)



    

