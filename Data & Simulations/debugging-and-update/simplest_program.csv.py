import csv
import os
import shutil

outputFile = open('log.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)

outputWriter.writerow(['spam', 'eggs', 'bacon', 'ban'])

