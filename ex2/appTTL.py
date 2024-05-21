import json
import csv

ttl1 = """
@prefix : <http://www.example.org/disease-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix swrl: <http://www.w3.org/2003/11/swrl#> .
@prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .
@base <http://www.example.org/disease-ontology#> .

<http://www.example.org/disease-ontology> rdf:type owl:Ontology .

#################################################################
#    Annotation properties
#################################################################

###  http://www.example.org/disease-ontology#name
:name rdf:type owl:AnnotationProperty .


#################################################################
#    Object Properties
#################################################################

###  http://www.example.org/disease-ontology#exhibitsSymptom
:exhibitsSymptom rdf:type owl:ObjectProperty ;
                 rdfs:domain :Patient ;
                 rdfs:range :Symptom .


###  http://www.example.org/disease-ontology#hasDisease
:hasDisease rdf:type owl:ObjectProperty ;
            rdfs:domain :Patient ;
            rdfs:range :Disease .


###  http://www.example.org/disease-ontology#hasSymptom
:hasSymptom rdf:type owl:ObjectProperty ;
            rdfs:domain :Disease ;
            rdfs:range :Symptom .


###  http://www.example.org/disease-ontology#hasTreatment
:hasTreatment rdf:type owl:ObjectProperty ;
              rdfs:domain :Disease ;
              rdfs:range :Treatment .


###  http://www.example.org/disease-ontology#receivesTreatment
:receivesTreatment rdf:type owl:ObjectProperty ;
                   rdfs:domain :Patient ;
                   rdfs:range :Treatment .


#################################################################
#    Data properties
#################################################################

###  http://www.example.org/disease-ontology#hasDescription
:hasDescription rdf:type owl:DatatypeProperty .


#################################################################
#    Classes
#################################################################

###  http://www.example.org/disease-ontology#Disease
:Disease rdf:type owl:Class .


###  http://www.example.org/disease-ontology#Patient
:Patient rdf:type owl:Class .


###  http://www.example.org/disease-ontology#Symptom
:Symptom rdf:type owl:Class .


###  http://www.example.org/disease-ontology#Treatment
:Treatment rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

"""

doencas = []
sintomas = []
desc = {}
dic_d = {}
treatments = []
dic_treatments = {}

deseases = open("med_tratamentos.ttl", "w",encoding='utf-8')

deseases.write(ttl1)

with open('Disease_Treatment.csv',newline='', encoding='utf-8') as f:
    spamreader = csv.reader(f, delimiter=',', quotechar='|')
    next(spamreader,None)
    for row in spamreader:
        d = row[0].replace(" ","_").replace("(","_").replace(")","_")
        if d[0] == "_":
            d = d[1:]
        if d not in treatments:
            treatments.append(d)
        
        for i in range(1,len(row)):
            r = row[i].replace(" ","_").replace("(","_").replace(")","_")
            if row[i] != "" and r not in dic_treatments:
                if r[0] == "_":
                    r = r[1:]
                dic_treatments[r] = []
                ttl = f"""

###  http://www.example.org/disease-ontology#{r}
:{r} rdf:type owl:NamedIndividual ,
                           :Treatment .

"""
                deseases.write(ttl)

with open('Disease_Syntoms.csv',newline='', encoding='utf-8') as f:
    spamreader = csv.reader(f, delimiter=',', quotechar='|')
    next(spamreader,None)
    for row in spamreader:
        r = row[0].replace(" ","_").replace("(","_").replace(")","_")
        if r[0] == "_":
            r = r[1:]
        if r not in doencas:
            dic_d[r] = []
            doencas.append(r)

        for i in range(1,len(row)):
            r2 = row[i].replace(" ","_").replace("(","_").replace(")","_")
            if row[i] != "" and r2 not in sintomas:
                if r2[0] == "_":
                    r2 = r2[1:]
                sintomas.append(r2)
                ttl = f"""

###  http://www.example.org/disease-ontology#{r2}
:{r2} rdf:type owl:NamedIndividual ,
                :Symptom .

"""
                deseases.write(ttl)
            if r2 not in dic_d[r]:
                dic_d[r].append(r2)

with open('Disease_Description.csv',newline='', encoding='utf-8') as f:
    spamreader = csv.reader(f, delimiter=',', quotechar='|')
    next(spamreader,None)
    for row in spamreader:
        des = row[0].replace(" ","_").replace("(","_").replace(")","_")
        r = row[1:]
        descr = ','.join(r)
        desc[des] = descr

    
for d in doencas:
    sentence = f""":hasSymptom"""
    for s in dic_d[d]:
        if s != "":
            sentence = sentence + f""" :{s} ,"""
    
    if d in desc:
        sentence = sentence[:-1] + " ;"
    else:
        sentence = sentence[:-1] + " ."
    ttl = f"""

###  http://www.example.org/disease-ontology#{d}
:{d} rdf:type owl:NamedIndividual ,
                   :Disease ;
"""
    ttl = ttl + sentence

    if d in desc:
        if d in treatments:
            ttl2 = f"""
        :hasDescription "{desc[d].replace('"',"'")}"^^xsd:string ;
"""
        else:
            ttl2 = f"""
        :hasDescription "{desc[d].replace('"',"'")}"^^xsd:string .
"""
        ttl = ttl + ttl2

    sentence2 = f""":hasTreatment"""
    if d in treatments:
        for t in dic_treatments[d]:
            sentence2 = sentence2 + f""" :{t} ,"""
        
        sentence2 = sentence2[:-1] + " ."
        
        ttl = ttl + sentence2
        
    ttl += "\n"

    deseases.write(ttl)
    
ttlf = """

###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi
"""
deseases.write(ttlf)
