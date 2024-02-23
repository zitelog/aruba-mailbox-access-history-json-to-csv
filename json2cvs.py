 
import os
import argparse
import json
import csv

def parse(json_file):
    data = json_file["data"]
    rows = list()

    for item in data:
        row = list()
        for key, value in item.items():
            if key == "ipDetails":
                row.append(value.get("ipAddress"))
                row.append(value.get("asn"))
                info = value.get("info")
                row.append(info.get("blacklist"))
                row.append(info.get("ip"))
                row.append(info.get("num_blacklist"))
                row.append(value.get("org"))
                row.append(value.get("proxyType"))
                row.append(value.get("anonymity"))
                row.append(value.get("city"))
                row.append(value.get("country"))
                row.append(value.get("country_code"))
            elif key == "device":
                row.append(value.get("osPlatform"))
                row.append(value.get("osFamily"))
                row.append(value.get("osVersion"))
                row.append(value.get("browserEngine"))
                row.append(value.get("browserEngineVersion"))
            else: 
                row.append(value)

        if len(row):
            rows.append(row)
    return rows

def write(filename, rows):
    header = [
            'id', 'username', 'clientId', 'clientDescription',
            'ipAddress','asn','blacklist','ip','num_blacklist','org','proxyType','anonymity','city','country','country_code',
            'newDevice','osPlatform','osFamily','osVersion','browserEngine','browserEngineVersion',
            'reportedAccessDate','reportedAccessStatus','timestamp','additionalClientDescriptions','suspiciousAccessEventCode','suspiciousAccessEventDate','sessionId'
         ]
    
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == '__main__':
    argparse = argparse.ArgumentParser(prog='json2csv', description="Parse files from a directory and save the result in csv file with same name of the first file")

    argparse.add_argument("--input-path", help="If no path is specified the files will be searched in the current directory")
    argparse.add_argument('--output-path', metavar='', help="output directory, must exist. If no path is specified the file will be saved in the current directory")

    args = argparse.parse_args()

    input_path= os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.dirname(os.path.realpath(__file__))

    if args.input_path is not None and not os.path.isdir(args.input_path):
        print (argparse.prog + f": error: argument input-path: file not exist: '{args.input_path}'")
        exit()

    if args.output_path is not None and not os.path.isdir(args.output_path):
        print (argparse.prog + f": error: argument output-path: path not exist: '{args.output_path}'")
        exit()

    if args.input_path is not None:
        input_path = args.input_path

    if args.output_path is not None:
        output_path = args.output_path

    
    invalid_json_files = list()
    read_json_files = list()
    rows = list()
    for file in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path,file)):
            with open(os.path.join(input_path,file)) as json_file:
                try:
                    rows += parse(json.load(json_file))
                    read_json_files.append(file)
                except ValueError as e:
                    # if the file is not valid, print the error 
                    #  and add the file to the list of invalid files
                    #print("JSON object issue: %s" % e)
                    invalid_json_files.append(file)
    
    if len(read_json_files):
        outputfile = os.path.splitext(os.path.basename(read_json_files[0]))[0]
        outputfile += '.csv'
        outputfile = os.path.join(output_path,outputfile) 
        write(outputfile, rows)

