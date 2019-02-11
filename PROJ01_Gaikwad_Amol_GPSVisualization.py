"""
10/27/2018
Author: Amol Gaikwad

GPS data visualization

"""

import csv
import math
from haversine import haversine

__author__ = 'Amol Gaikwad'

def main():
    """
        Main Program
        Handle command line arguments.

        :param : None

        :return: None
    """
    max_cost = math.inf
    # List of input txt files
    inp_files = ["ZIAC_CO0_2018_10_12_1250.txt", "ZIAB_CIU_2018_10_11_1218.txt", "ZIAA_CTU_2018_10_10_1255.txt",
                 "ZI8N_DG8_2018_08_23_1316.txt", "ZI8K_EV7_2018_08_20_1500.txt", "ZI8J_GKX_2018_08_19_1646.txt",
                 "ZI8H_HJC_2018_08_17_1745.txt", "ZI8G_ERF_2018_08_16_1428.txt"]
    # Loop over all files
    for file in inp_files:
        # Get valid records
        orig_data = preprocess(file)
        # Calculate cost of data
        cost = get_cost(orig_data)

        # Update max cost if cost < max_cost
        if cost < max_cost:
            max_cost = cost
            cost_data = orig_data
            min_file = file

    print("Optimum path file " + min_file)
    print("Optimum cost " + str(max_cost))

    # Get latitude and longitude information from data
    data = process_directions(cost_data)
    # Get latitude and longitude of turns
    turn_list = check_left_turn(0, cost_data)
    # Emit kml file header
    file = write_kmlfile_header(min_file)
    # Emit kml file body
    file = write_kmlfile_body(file, data)
    # Emit kml file body for turns
    file = write_kmlfile_body_turn(file, turn_list)
    # Get latitude and longitude of stops
    stop_list = check_stop(cost_data, data)
    # Emit kml file body for stops
    file = write_kmlfile_body_stop(file, stop_list)
    # Emit kml file trailer
    file = write_kmlfile_trailer(file)



def get_cost(data):
    """
       Get cost according to cost function

       :param :
        data: data for which cost is to be calculated

       :return:
        cost: cost for the data

    """
    # Get initial time in mins
    initial_time = get_time_mins(data[0][0])
    # Get last time in mins
    last_time = get_time_mins(data[len(data)-1][0])
    # Get time in mins
    diff_time = last_time - initial_time

    # Get max velocity
    max_velocity = max([float(row[5]) for row in data])

    # Calculate cost function
    cost = (diff_time/30) + (max_velocity)/(120*0.868976)

    return cost

def get_time_mins(time):
    """
       Get time in minutes from UTC time

       :param :
        time: UTC time

       :return:
        total_min: total time in minutes

    """
    timearr = time.split(".")
    # Convert hours to mins
    hours_to_min = float(float(timearr[0][0:2]) * 60)
    min = float(timearr[0][2:4])
    # Get seconds information
    sec = timearr[0][4:6]+"." + timearr[1]
    # Convert secs to mins
    sec_to_min = float(sec)/60

    total_min = hours_to_min + min + sec_to_min

    return total_min

def check_left_turn(idx, data):
    """
       Check for left turn

       :param :
        idx: starting index of data
        data: input_data

       :return:
        turn_list: latitude and longitude containing turns

    """
    point_data = []
    # Set window size
    window_size = 30
    # While index doesnt reach end of data
    while idx < len(data) and idx+window_size < len(data):
        # Get current angle
        curr_angle = float(data[idx][6])
        # Get next angle
        next_angle = float(data[idx+window_size][6])
        # Get current speed
        curr_speed = float(data[idx][5])
        # Get next speed
        next_speed = float(data[idx + window_size][5])
        diff_angle = 0
        if(curr_angle > next_angle):
            if (curr_speed > 1 and next_speed > 1):
                # Calculate angle difference
                diff_angle = abs(curr_angle - next_angle)
        else:
            if (curr_speed > 1 and next_speed > 1):
                # Calculate angle difference for wrap around case
                diff_angle = abs(curr_angle+360 - next_angle)

        # Check for left turn
        if(diff_angle > 55) and (diff_angle < 115):
            new_idx = (idx+idx+window_size)/2
            # Get mid point data for turn
            point = data[math.ceil(new_idx)]
            point_data.append(point)
            # If turn found increment index by window size
            idx += window_size+1
        else:
            # Increment index for next data point
            idx += 1

    turn_list = process_directions(point_data)

    return turn_list

def check_stop(data, direction_data):
    """
       Check for stop data

       :param :
        data: input_data
        direction_data: latitude and longitude data

       :return:
        stop_list: latitude and longitude containing stops

    """
    idx = 0
    point_data = []
    # Loop while you don't reach end of data
    while idx < len(direction_data)and idx+1 < len(direction_data):
        # Get current point
        curr_point = (float(direction_data[idx][0]),float(direction_data[idx][1]))
        # Get next point
        next_point = (float(direction_data[idx+1][0]),float(direction_data[idx+1][1]))
        # Calculate haversine distance
        dist = haversine(curr_point, next_point)
        # Initialize thresholds
        threshold_speed = 0.01
        threshold_distance = 0.002
        threshold_time = 0.4
        # Get current time
        curr_time = float(data[idx][0])
        # Get next time
        next_time = float(data[idx+1][0])
        # Get time difference
        time_diff = next_time - curr_time
        # Get current speed
        curr_speed = float(data[idx][5])
        # Append stop data if speed is less than threshold speed and time greater tha threshold time
        if curr_speed < threshold_speed and time_diff > threshold_time:
            # Append data if distance less than threshold distance
            if dist < threshold_distance:
                point_data.append(data[idx])

        idx += 1

    # Get latitude and longitude for stop data
    stop_list = process_directions(point_data)

    return stop_list

def write_kmlfile_header(file_name):
    """
       Emit kml file header

       :param :
        file_name: file name of kml file to be written

       :return:
        data: written file

    """
    file_arr = file_name.split(".")
    file = open(file_arr[0]+".kml", "w+")
    str = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns = "http://www.opengis.net/kml/2.2">\n\
        <Document>\n\
        <Style id="yellowPoly">\n\
            <LineStyle>\n\
                <color>Af00ffff</color>\n\
                <width>6</width>\n\
            </LineStyle>\n\
            <PolyStyle>\n\
                <color>7f00ff00</color>\n\
            </PolyStyle>\n\
        </Style>\n\
        <Placemark><styleUrl>#yellowPoly</styleUrl>\n\
        <LineString>\n\
        <Description>Speed in MPH, not altitude.</Description>\n\
        <extrude> 1 </extrude>\n\
        <tesselate> 1 </tesselate>\n\
        <altitudeMode> clamp to ground </altitudeMode>\n\
        <coordinates>'

    file.write(str)

    return file


def write_kmlfile_body(file, data):
    """
       Emit kml file body containing data points

       :param :
        file: file to be written
        data: turn data

       :return:
        data: written file

    """

    for val in data:
        file.write(str(val[1])+",")
        file.write(str(val[0])+"\n")

    return file

def write_kmlfile_body_turn(file, data):
    """
       Emit kml file body for turns

       :param :
        file: file to be written
        data: turn data

       :return:
        data: written file

    """
    string = """
                            </coordinates>   
                        </LineString>  
                    </Placemark> 
           """
    file.write(string)
    string = ""
    for val in data:
        string += """<Placemark>
                <description>Default Pin is Yellow</description>
                <Point><coordinates>"""
        string += (str(val[1])+",")
        string += (str(val[0])+"\n")
        string += """</coordinates></Point>
                </Placemark>"""

        file.write(string)

    return file


def write_kmlfile_body_stop(file, data):
    """
       Emit kml file body for stop

       :param :
        file: file to be written
        data: stop data

       :return:
        data: written file

    """

    string = ""
    for val in data:
        string += """<Placemark>
        <description>Red PINfor A Stop</description>
        <Style id="normalPlacemark">
        <IconStyle>
        <color>ff0000ff</color>
        <Icon>
        <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>
        </Icon>
        </IconStyle>
        </Style>
        <Point><coordinates>"""
        string += (str(val[1])+",")
        string += (str(val[0])+"\n")
        string += """</coordinates></Point>
                </Placemark>"""

        file.write(string)

    return file

def write_kmlfile_trailer(file):
    """
       Emit kml file trailer

       :param :
        file: file to be written

       :return:
        file: written file

    """

    str = """      
            </Document>
        </kml>
        """

    file.write(str)

    return file

def process_directions(data):
    """
       Extracts the latitude and longitude information from the given data

       :param :
        data: extracted data

       :return:
        directions: latitude and longitude
    """
    directions = []

    for val in data:
        temp= []
        # Get latitude
        lat = val[1]
        # Get longitude
        long = val[3]
        # Get north/south
        north_south = val[2]
        # Get east/west
        east_west = val[4]

        lat_minsarr = lat.split(".")
        # Get latitude mins
        lat_mins = lat_minsarr[0][-2:]
        # Get latitude degrees
        lat_degrees = float(lat_minsarr[0][0:len(lat_minsarr[0])-2])
        lat_mins += "."+lat_minsarr[1]
        # Get latitude hours
        lat_hours = float(lat_mins)/60
        lat_degrees+= lat_hours
        if(north_south == 'S'):
            # If direction is South multiply by -1
            lat_degrees = -1 * lat_degrees;

        # Append latitude
        temp.append(lat_degrees)

        long_minsarr = long.split(".")
        # Get longitude mins
        long_mins = long_minsarr[0][-2:]
        # Get longitude degrees
        long_degrees = float(long_minsarr[0][0:len(long_minsarr[0])-2])
        long_mins += "." + long_minsarr[1]
        # Get longitude hours
        long_hours = float(long_mins) / 60
        long_degrees += long_hours
        if (east_west == 'W'):
            # If direction is West multiply by -1
            long_degrees = -1 * long_degrees;

        # Append longitude
        temp.append(long_degrees)
        # Add latitude and longitude to directions
        directions.append(temp)

    return directions

def preprocess(file):
    """
       Preprocess input file data

       :param :
        file: Input csv file

       :return:
        data: extracted data

    """
    extracted_data = []

    # open file
    with open(file, encoding="utf-8") as f:
        # Skip first five header line
        next(f)
        next(f)
        next(f)
        next(f)
        next(f)
        # read csv data file
        csv_readfile = csv.reader(f, delimiter=',')
        for row in csv_readfile:
            # Choose only records having $GPRMC and which are active
            if row[0]=='$GPRMC' and row[2]=='A':
                data = []
                # Append time
                data.append(row[1])
                # Append latitude
                data.append(row[3])
                # Append N/S
                data.append(row[4])
                # Append longitude
                data.append(row[5])
                # Append E/W
                data.append(row[6])
                # Append speed
                data.append(row[7])
                # Append angle
                data.append(row[8])

                extracted_data.append(data)

    return extracted_data

if __name__ == '__main__':
    main()