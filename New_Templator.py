'''Templator.
Author: Kevin Dryden (2020), under supervision of Dr. Anya Tafliovich

Given a Template file and Aggregate Json, create A HTML output merging the two.

'''

import argparse
import json
import os
import shutil



if __name__ == '__main__':


    #Collect Arguments for Function Flexibility (Json Aggregate Path, Template Path, Output Path) or leave arguments blank for defaults

    PARSER = argparse.ArgumentParser(
        description=('Produces a HTML output of the aggegated results.'))
    PARSER.add_argument('Json_Aggregate_Path', nargs='?',
                        help='Location of the Json',
                        default='aggregated.json')
    PARSER.add_argument('Template_Path', nargs='?',
                        help=('Path to the HTML template'),
                        default='template.html')
    PARSER.add_argument('Output_Path', nargs='?',
                        help=('Path to the output'),
                        default='output.html')
    ARGS = PARSER.parse_args()

    #Part that does the templating

    #Open Json File

    jsonfile = open(ARGS.Json_Aggregate_Path)
    data = json.load(jsonfile)

    #Create new output file based on the template and opens it. If Output File already exists it will be overwritten

    shutil.copyfile(ARGS.Template_Path, ARGS.Output_Path)
    file = open(ARGS.Output_Path, 'r+')

    #Parse the output file and insert Json information into specified location (var aggregated)

    lines = file.readlines()
    count = 0
    for line in lines:
        if line.strip().startswith("var aggregated"):
            break
        count = count+1
    file.seek(0)
    lines.insert(count+1, " ; \n")
    lines.insert(count+1, json.dumps(data))
    file.writelines(lines)
