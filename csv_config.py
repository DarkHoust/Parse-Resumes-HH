from parser import *
import pandas as pandas
import csv

def parseResume(job):
    links = getLink(job)

    with open(job + '.csv', 'w+', newline='', encoding='utf-8') as f:
        resume = dict(parseLink(links[0]))
        csvControl = csv.writer(f)
        csvControl.writerow(resume.keys())
        csvControl.writerow(resume.values())

        for _ in range(1, len(links)):
            resume = dict(parseLink(links[_]))
            with open(job + '.csv', 'a+', newline='', encoding='utf-8' ) as f:
                csvControl = csv.writer(f)
                csvControl.writerow(resume.values())

