import grequests
import pandas
import json

def fetch_urls(srcode, freshman_year, senior_year):
    print("Generating urls...")
    BASE_URL = "http://dione.batstate-u.edu.ph/public/sites/apps/student/ajax.php?do=fetch_grades"
    SEMESTERS = ["FIRST","SECOND","SUMMER","SUMMER2"]
    urls = []
    for i in range(senior_year-freshman_year):
        SCHOOL_YEAR = ("{}-{}".format(freshman_year, freshman_year+1))
        for j in range(len(SEMESTERS)):
            urls.append("{}&srcode={}&schoolyear={}&semester={}".format(BASE_URL,srcode,SCHOOL_YEAR,SEMESTERS[j]))
        freshman_year += 1
    return urls

def fetch_grades(urls):
    grades = []
    rs = (grequests.get(url) for url in urls)
    res = grequests.map(rs)
    print("Fetching grades. Please wait...")
    for grade in res:
        if(len(grade.json()) >= 0):
            [grades.append(subject) for subject in grade.json()]
    return grades

'''
compute for gwa
'''
def determine_gwa(grades_object):
    gwa = 0
    total_units = 0
    for subject in grades_object:
        gwa += float(subject['grade2'])*float(subject['subject_credits'])
        total_units += float(subject['subject_credits'])
    gwa /= total_units
    print("GWA: {}. Total Units: {}".format(gwa, total_units))



def main():
    srcode = input("Enter your SR Code: ")
    freshman_year = int(input("Enter your freshman year: "))
    senior_year = int(input("Enter your senior year: "))
    grades_url = fetch_urls(srcode, freshman_year, senior_year)
    grades = fetch_grades(grades_url)
    determine_gwa(grades)

if __name__ == '__main__':
    main()