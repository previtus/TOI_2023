import numpy
import os
import sys
import pylab
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import norm


# Function to load the wifi RSS data
def load_wifi_data(data_folder, n_samples, n_ap):
    """
    :param data_folder: Location of WiFi RSS data
    :param n_samples: Number of RSS samples collected for each location
    :param n_ap: Number of access points
    :return: train and test wifi databases
    """

    #sys.stdout.write("-> Loading files...")
    train_path = os.path.join(data_folder,"wifiData")
    test_path = os.path.join(data_folder,"testWifiData")

    # We are going to examine two cases with 3 and 5 Access Points (APs)
    if n_ap == 3:
        ap_index = [1, 2, 3]
    else:
        ap_index = [1, 2, 3, 4, 5]

    # We read the wifi RSS collected in the training phase to built the Wifi database
    file_list = os.listdir(train_path)
    train_files = [f for f in file_list if os.path.splitext(f)[1] == '.txt']

    n_locations = len(train_files)
    wifi_database = numpy.zeros((n_locations, (n_ap * n_samples) + 3))
    ap_name = "AP_"

    file_count = -1
    for f in train_files:
        file_count += 1

        if n_ap == 3:
            ap_counter = [0, 0, 0]
        else:
            ap_counter = [0, 0, 0, 0, 0]

        fid = open(os.path.join(train_path,f), 'r')
        wifi_database[file_count, 0] = file_count
        first_line = 0
        for line in fid:
            data = line.split()
            if first_line == 0:
                first_line += 1
                wifi_database[file_count, 1] = int(data[0])
                wifi_database[file_count, 2] = int(data[1])
            else:
                for idx in range(1, n_ap + 1):
                    if data[1] == (ap_name + str(idx)):
                        ap_counter[idx - 1] += 1
                        db_index = int((n_samples * (ap_index[idx - 1] - 1)) + 2 + ap_counter[idx - 1])
                        wifi_database[file_count, db_index] = float(data[2])

    # Now we load the test points. Wifi data collected at unknown locations.
    file_list = os.listdir(test_path)
    test_files = [f for f in file_list if os.path.splitext(f)[1] == '.txt']
    test_files.sort()
    n_locations = len(test_files)
    test_db = numpy.zeros((n_locations, (n_ap * (n_samples - 10)) + 3))

    file_count = -1
    for f in test_files:
        file_count += 1

        if n_ap == 3:
            ap_counter = [0, 0, 0]
        else:
            ap_counter = [0, 0, 0, 0, 0]

        fid = open(os.path.join(test_path,f), 'r')
        test_db[file_count, 0] = file_count
        first_line = 0
        for line in fid:
            data = line.split()
            if first_line == 0:
                first_line += 1
                test_db[file_count, 1] = int(data[0])
                test_db[file_count, 2] = int(data[1])
            else:
                for idx in range(1, n_ap + 1):
                    if data[1] == (ap_name + str(idx)):
                        ap_counter[idx - 1] += 1
                        db_index = int(((n_samples - 10) * (ap_index[idx - 1] - 1)) + 2 + ap_counter[idx - 1])
                        test_db[file_count, db_index] = float(data[2])

    #sys.stdout.write("done\n")
    return wifi_database, test_db

# Fit a normal distribution to the RSS data
def fit_data(train_db, n_samples, n_ap):
    """
    :param train_db: RSS points collected at known locations
    :param n_samples: Number of RSS samples per location
    :param n_ap: Number of access points
    :return: Wifi fingerprint database; We approximate the RSS at each location with a Gaussian
    """

    sys.stdout.write("-> Modeling RSS with Gaussian dist...")

    n_loc = len(train_db)

    # Initialize Wifi database
    wifi_db = numpy.zeros((n_loc, 3 + (n_ap * 2)))

    for i in range(0, n_loc):
        wifi_db[i, 0] = i
        wifi_db[i, 1] = train_db[i, 1]
        wifi_db[i, 2] = train_db[i, 2]
        for j in range(0, n_ap):
            ind_start = int((n_samples * j) + 3)
            ind_end = int((j + 1) * n_samples + 3)
            dat = train_db[i, ind_start:ind_end]
            [mu, sigma] = norm.fit(dat)
            wifi_db[i, (j * 2) + 3] = mu
            wifi_db[i, (j * 2) + 4] = sigma

    sys.stdout.write("done\n")
    return wifi_db

# Visualize fingerprint locations and locations of APs
def show_fingerprints(train_db, n_ap):
    """
    :param train_db: RSS points collected at known locations
    :param n_ap: Number of APs
    :return: null
    """
    #sys.stdout.write("-> Displaying fingerprints...")

    if n_ap == 3:
        ap_loc = np.array([[6, 6], [8, 16], [18, 14]])
    else:
        ap_loc = np.array([[6, 6], [8, 16], [18, 14], [16, 4], [12, 10]])

    pylab.figure()
    pylab.plot(train_db[:, 1], train_db[:, 2], 'co', markersize=17)
    pylab.plot(ap_loc[:, 0], ap_loc[:, 1], 'b*', markersize=10)
    major_ticks = numpy.arange(-2, 22, 2)
    axes = pylab.gca()
    axes.set_xlim([-2, 22])
    axes.set_ylim([-2, 22])
    axes.set_xticks(major_ticks)
    axes.set_yticks(major_ticks)
    pylab.grid(True)
    pylab.xlabel("X [m]")
    pylab.ylabel("Y [m]")
    pylab.title("Cyan points: fingerprint locations, Blue points: Access Points")
    pylab.show(block=False)
    #sys.stdout.write("done\n")

    return


