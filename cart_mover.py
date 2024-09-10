"""
        v2
"""

import subprocess
import json, re
import pandas as pd
from docopt import docopt
from prettytable import PrettyTable

def get_args():
	"""Function to get command line arguments.

	Defines arguments needed to run this program.

	:return: Dictionary with arguments
	:rtype: dict
	"""
	
	usage = """
	Usage:
        move_cart.py -L <LIB> --cartridges
        move_cart.py -L <LIB> -C <CARTRIDGE> --moveToSlot

        
		move_cart.py --version
		move_cart.py -h | --help

	Options:
		-h --help            Show this message and exit


	"""

	args = docopt(usage)
	return args	

def get_devices():
    """Function that will get all the devices"""
    output = subprocess.check_output(['device_scan', '-t', 'changer']).decode('utf-8')

    return output

def mapping(output):
    """This map the device and vendor info into lib"""

    # Split the file contents by each device
    devices = output.split('\n\n')
    # print(output)
    e = 1

    # Create an empty list to store the extracted information
    data = []
    # Create an empty list of device mapped to lib
    mapped =[]
    # # Loop through each device and extract the device and vendor info
    for device in devices:
        """ search for the pattern "Device=\[(.*?)\]", where (.*?) is anycharacter inside 
                 the square brackets [], from the string DEVICE.
                 
                 The program will get the characters inside the brackets and have it as 
                 a value for 'MATCH1'
                 
                 Similarly, we can find Vendor using regex with pattern
                 """ 
        match1 = re.search(r"Device=\[(.*?)\]", device)
        if match1:
            device_ = match1.group(1)

        match2 = re.search(r"Vendor info =	\[(.*?)\]", device)
        if match2:
            vendor = match2.group(1)
            """The match1 will be the device and the match2 will be the vendor info.
                Each time RE will find the match device and vendor will be appended to the 
                list named DATA
            """
            data.append([device_,vendor])


    for i in range(len(data)):

        if data[i][1] == '1803130000078AA3410':
            lib = '1'
        elif data[i][1] == '1803130000078AA3390':
            lib = '2'
        elif data[i][1] == '1901130000078AA4040':
            lib = '3'

        if i == 0:
            mapped.append([data[i][0],data[i][1],lib])
            
        else:
            if data[i][1] == data[i-1][1]:
                mapped.append([data[i][0],data[i][1],lib])
            else:
                e = e+1
                mapped.append([data[i][0],data[i][1],lib])

    # Create dataframe for mapping
    df = pd.DataFrame(mapped, columns=['devices', 'vendor', 'lib'])
    df = df.drop_duplicates(subset='lib', keep='first').reset_index(drop=True)

    return df

def get_mapped(df):
    """Create dictionary for the mapped data"""
       
    out = {row['lib']:[row['devices'], row['vendor']] for idx, row in df.iterrows()}
    return out

def cart_display(data):
    table = PrettyTable()
    table.field_names = ["volser", "state", "accessible", "location", "mediaType", "encrypted", "mostRecentVerification", "mostRecentUsage", 
                         "logicalLibrary", "elementAddress", "internalAddress"]

    # Add rows to table
    for item in data:
        volser = item["volser"]
        state = item["state"]
        accessible = item['accessible']
        location = item["location"]
        mediaType = item["mediaType"]
        encrypted = item["encrypted"]
        mostRecentVerification = item["mostRecentVerification"]
        mostRecentUsage = item["mostRecentUsage"]
        logicalLibrary = item["logicalLibrary"]
        elementAddress = item["elementAddress"]
        internalAddress = item["internalAddress"]
      
        
        table.add_row([volser, state, accessible, location, mediaType, encrypted, mostRecentVerification, mostRecentUsage, logicalLibrary,
                        elementAddress, internalAddress])

    print(table)

def cart_info(command):

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print(f"Error: {error.decode('utf-8')}")
            exit(1)
        
        # Load the contents as JSON
        cmd_out = output.decode('utf-8')
        try:
            out_json = json.loads(cmd_out)
            cart_display(out_json) 
        except:
            print(output.decode('utf-8'))
        

    except subprocess.CalledProcessError:
        return "Error running command."
    except FileNotFoundError:
        return "command not found."

def move_cartridge(command):

    try:

        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print(f"Error: {error.decode('utf-8')}")
            exit(1)
        
        
        return output

    except subprocess.CalledProcessError:
        return "Error running command."
    except FileNotFoundError:
        return "command not found."



def main(args):
    lib = args['<LIB>']
    cart = args['<CARTRIDGE>']
    output = get_devices()

    data = mapping(output)
    map_lib = get_mapped(data)

    if lib in map_lib:
        driver = map_lib[lib][0]
        if args['--cartridges']:
            command = ['/opt/ITDT/itdt', '-f', driver, 'ros', 'POST', '/v1/dataCartridges']
            cart_info(command)

        elif args['--moveToSlot']:
            typ = 'moveToSlot'
            url = f"/v1/workItems '[{{\"type\":\"{typ}\",\"cartridge\":\"{cart}\"}}]'"
            command = ['/opt/ITDT/itdt', '-f', driver, 'ros', 'POST', url]
            cmd_out = move_cartridge(command)
            print(cmd_out.decode('utf-8'))
    else:
        print('The Lib you entered is not on the devices!')
   


if __name__ == '__main__':
    ARGS = get_args()
    main(ARGS)


