# EarthQuake Project
This is a scientific project for ITMO University related to estimating the resources needed in case of extreme situations

# Algorithms description
## Earthquake way of working
1. Initiation
1. Call to МЧС
1. Sending forces to help
1. Sort patients
1. Do the operations on place
1. Transport the severly injured to specialized clinics in Moscow and SPB
1. Transport the injured to the clinics in the nearest big city (столица области)
1. CLose the whole rescue operation

## Formulas

## The number of brigades
x = n * t1 / t2
n - the number of injured (all)
t1 - average time of one operation
t2 - the brigade working time per day

# File description
1. index.py - tarting point of the model
1. transport.py - data about planes and other transport machines
1. medical_help_onland.py - data about operations and medical personnel
1. earthquake_data.py - data about the earthquake that took place
