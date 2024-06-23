import csv
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter, defaultdict
import pandas as pd
from datetime import datetime

airport_codes = [
    "AAL", "ABE", "ABQ", "ABV", "ABZ", "ACC", "ACE", "ACK", "ADA", "ADB",
    "ADD", "ADL", "ADQ", "ADS", "AEP", "AER", "AFW", "AGP", "AHB", "AKL",
    "ALA", "ALB", "ALC", "ALG", "AMA", "AMD", "AMM", "AMS", "ANC", "ANF",
    "ANU", "APA", "AQP", "ARN", "ATH", "ATL", "AUA", "AUH", "AUS", "AVL",
    "AXT", "AYT", "BAH", "BAQ", "BAV", "BBU", "BCD", "BCN", "BDJ", "BDL",
    "BDO", "BEG", "BEL", "BEN", "BER", "BET", "BEY", "BFI", "BFS", "BGI",
    "BGO", "BGW", "BGY", "BHD", "BHM", "BHX", "BIL", "BIO", "BJX", "BJY",
    "BKI", "BKK", "BKL", "BLA", "BLL", "BLQ", "BLR", "BMA", "BNA", "BNE",
    "BOD", "BOG", "BOI", "BOM", "BOO", "BOS", "BPN", "BRE", "BRI", "BRS",
    "BRU", "BSB", "BSL", "BTH", "BTR", "BTV", "BUD", "BUF", "BUR", "BVA",
    "BWI", "BWN", "BZE", "CAE", "CAG", "CAI", "CAK", "CAN", "CBB", "CBR",
    "CCJ", "CCS", "CCU", "CDG", "CEB", "CGB", "CGH", "CGK", "CGN", "CGO",
    "CGP", "CGQ", "CGR", "CHA", "CHC", "CHO", "CHS", "CIA", "CID", "CJU",
    "CKG", "CLE", "CLO", "CLT", "CMB", "CMH", "CMN", "CNF", "CNS", "CNX",
    "COK", "COR", "COS", "CPH", "CPT", "CRL", "CRP", "CRW", "CSX", "CTA",
    "CTG", "CTS", "CTU", "CUK", "CUL", "CUN", "CUR", "CUU", "CUZ", "CVG",
    "CWB", "CXH", "CYC", "CZX", "DAC", "DAD", "DAL", "DAR", "DAY", "DCA",
    "DEL", "DEN", "DFW", "DGA", "DJJ", "DKR", "DLA", "DLC", "DME", "DMK",
    "DMM", "DOH", "DPA", "DPS", "DRS", "DRW", "DSM", "DSN", "DTW", "DUB",
    "DUR", "DUS", "DVO", "DXB", "EBB", "EBH", "EBL", "ECP", "EDI", "EIN",
    "EIS", "ELP", "EMA", "ENA", "EOH", "ESB", "EUG", "EVN", "EWR", "EYW",
    "EZE", "FAI", "FAO", "FAR", "FAT", "FCO", "FLL", "FLN", "FLR", "FOC",
    "FOR", "FRA", "FRU", "FSD", "FTY", "FUE", "FUK", "FWA", "GAU", "GCI",
    "GDL", "GDN", "GEG", "GFK", "GIG", "GJT", "GLA", "GMP", "GOI", "GOT",
    "GRB", "GRO", "GRR", "GRU", "GRZ", "GSO", "GSP", "GUA", "GUM", "GVA",
    "GYD", "GYE", "GYN", "HAJ", "HAK", "HAM", "HAN", "HAV", "HBA", "HDY",
    "HEH", "HEL", "HET", "HFE", "HGH", "HHN", "HIJ", "HKG", "HKT", "HMO",
    "HND", "HNL", "HOU", "HPN", "HRB", "HSV", "HYA", "HYD", "IAD", "IAH",
    "IBZ", "ICN", "ICT", "IEV", "IKA", "IKT", "ILM", "ILO", "INC", "IND",
    "IOM", "ISB", "ISG", "ISL", "ISP", "IST", "ITM", "ITO", "IVG", "JAI",
    "JAN", "JAX", "JBQ", "JED", "JER", "JFK", "JHB", "JHG", "JJN", "JNB",
    "JNU", "JOG", "JRO", "KBL", "KBP", "KBR", "KCH", "KEF", "KGL", "KHH",
    "KHI", "KHN", "KIJ", "KIX", "KJA", "KKJ", "KLO", "KMG", "KMI", "KMJ",
    "KMQ", "KNO", "KOA", "KOJ", "KRK", "KRR", "KRS", "KRT", "KTM", "KTN",
    "KTW", "KUF", "KUL", "KWE", "KWI", "KWL", "KZN", "LAD", "LAN", "LAS",
    "LAX", "LBA", "LBB", "LCA", "LCK", "LCY", "LED", "LEJ", "LEX", "LGA",
    "LGB", "LGK", "LGW", "LHE", "LHR", "LHW", "LIH", "LIL", "LIM", "LIN",
    "LIRI", "LIS", "LIT", "LJG", "LJU", "LKO", "LLA", "LOP", "LOS", "LPA",
    "LPB", "LPL", "LST", "LTN", "LUN", "LUX", "LWM", "LYS", "LYVR", "MAA",
    "MAD", "MAF", "MAH", "MAN", "MAO", "MAR", "MBA", "MBJ", "MCI", "MCO",
    "MCT", "MCZ", "MDC", "MDE", "MDL", "MDT", "MDW", "MDZ", "MED", "MEL",
    "MEM", "MEX", "MFM", "MFR", "MHD", "MHT", "MIA", "MID", "MKC", "MKE",
    "MKK", "MLA", "MLE", "MLI", "MMX", "MNL", "MOB", "MPH", "MPL", "MPM",
    "MRS", "MRU", "MRV", "MRY", "MSN", "MSP", "MSQ", "MSY", "MTY", "MUC",
    "MVD", "MVY", "MXP", "MYJ", "MYR", "MYY", "NAN", "NAP", "NAS", "NAT",
    "NAY", "NBO", "NCE", "NCL", "NGB", "NGO", "NGQ", "NGS", "NKG", "NNG",
    "NRN", "NRT", "NSN", "NTE", "NTL", "NUE", "NYO", "OAK", "OGG", "OIT",
    "OKA", "OKC", "OMA", "OME", "ONT", "OOL", "OPO", "ORD", "ORF", "ORL",
    "ORY", "OSL", "OTP", "OTZ", "OVB", "PBI", "PDG", "PDK", "PDX", "PEK",
    "PEN", "PER", "PFO", "PHC", "PHL", "PHX", "PIA", "PIT", "PKU", "PLJ",
    "PLM", "PLS", "PLU", "PLZ", "PMI", "PMO", "PMV", "PNH", "PNK", "PNQ",
    "PNS", "POA", "POM", "POS", "PRG", "PSA", "PSP", "PTP", "PTY", "PUJ",
    "PUS", "PVD", "PVG", "PWM", "RAK", "RAO", "RDM", "RDU", "REC", "REP",
    "RGN", "RIC", "RIX", "RNO", "ROA", "ROC", "ROV", "RST", "RSW", "RTM",
    "RUH", "RYG", "SAH", "SAL", "SAN", "SAP", "SAT", "SAV", "SAW", "SBA",
    "SBH", "SBN", "SBW", "SCL", "SDF", "SDJ", "SDQ", "SDU", "SEA", "SFO",
    "SGF", "SGN", "SHA", "SHE", "SHJ", "SHV", "SIN", "SJC", "SJD", "SJO",
    "SJU", "SJW", "SKG", "SLC", "SLZ", "SMF", "SNA", "SOF", "SOU", "SPN",
    "SPR", "SRG", "SSA", "SSH", "STL", "STN", "STP", "STR", "STT", "STX",
    "SUB", "SUS", "SVG", "SVO", "SVQ", "SVX", "SWA", "SXB", "SXM", "SXR",
    "SYD", "SYR", "SYX", "SYZ", "SZB", "SZG", "SZX", "TAO", "TAS", "TEB",
    "TFN", "TFS", "THQ", "THR", "TIA", "TIJ", "TIP", "TJM", "TLH", "TLL",
    "TLS", "TLV", "TNA", "TOS", "TPA", "TPE", "TRD", "TRF", "TRN", "TRV",
    "TSA", "TSE", "TSN", "TSV", "TUL", "TUN", "TUS", "TYN", "TYS", "TZA",
    "TZX", "UBN", "UFA", "UIO", "UKB", "UME", "UPG", "URC", "USM", "UYN",
    "UZC", "VCE", "VCP", "VDO", "VER", "VIE", "VIX", "VKO", "VLC", "VNO",
    "VQS", "VRN", "VSA", "VTE", "VVI", "WAW", "WLG", "WMX", "WNZ", "WRO",
    "WUH", "WUX", "XIY", "XMN", "XNA", "XNN", "XQC", "YDF", "YEG", "YHM",
    "YHZ", "YIP", "YKS", "YLW", "YMM", "YNT", "YOW", "YPA", "YQB", "YQM",
    "YQR", "YQT", "YSB", "YTH", "YTS", "YTZ", "YUL", "YUM", "YVR", "YWG",
    "YWK", "YXE", "YXL", "YYC", "YYJ", "YYR", "YYT", "YYZ", "YZF", "YZV",
    "ZAG", "ZBK", "ZNZ", "ZRH", "ZUH"
]


# Co chcę zrobić ?
# 1. Wybrać z tej listy 'data' tylko te rekordy które odpowiadają danemu lotnisku

def read_data_from_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)

        data = [line for line in reader]

        return data


def choose_data_by_airport(data, airport_code):
    return [line for line in data if line[0] == airport_code]

def countFlightsForAirport(data):
    return len(data)


def getDelays(data, forType):
    delays = [int(line[4]) for line in data if line[2] == forType]
    # print("Arrival delays: ", delays)
    if len(delays) == 0:
        return None
    return delays


def calculate_mean_arrival_delay(data):
    delays = getDelays(data, 'Arrival')
    if delays is None:
        return None
    meanTime = sum(delays) / len(delays)
    # print("Mean delay: ", meanTime)
    return meanTime


def calculate_mean_departure_delay(data):
    delays = getDelays(data, 'Departure')
    if delays is None:
        return None
    meanTime = sum(delays) / len(delays)
    # print("Mean delay: ", meanTime)
    return meanTime


def calculate_median_arrival_delay(data):
    delays = getDelays(data, 'Arrival')
    if delays is None:
        return None
    median = np.median(delays)
    # print("median: ", median)
    return median


def calculate_median_departure_delay(data):
    delays = getDelays(data, 'Departure')
    if delays is None:
        return None
    median = np.median(delays)
    # print("median: ", median)
    return median


def calculate_variance_arrival_delay(data):
    delays = getDelays(data, 'Arrival')
    if delays is None:
        return None
    variance = np.var(delays)
    # print("variance: ", variance)
    return variance


def calculate_variance_departure_delay(data):
    delays = getDelays(data, 'Departure')
    if delays is None:
        return None
    variance = np.var(delays)
    # print("variance: ", variance)
    return variance


def calculate_standard_deviation_arrival_delay(data):
    delays = getDelays(data, 'Arrival')
    if delays is None:
        return None
    standardDeviation = np.std(delays)
    # print("variance: ", variance)
    return standardDeviation


def calculate_standard_deviation_departure_delay(data):
    delays = getDelays(data, 'Departure')
    if delays is None:
        return None
    standardDeviation = np.std(delays)
    # print("variance: ", variance)
    return standardDeviation


def calculate_statistics(data):
    meanArrivalDelay = calculate_mean_arrival_delay(data)
    meanDepartureDelay = calculate_mean_departure_delay(data)
    medianArrivalDelay = calculate_median_arrival_delay(data)
    medianDepartureDelay = calculate_median_departure_delay(data)
    variantArrivalDelay = calculate_variance_arrival_delay(data)
    variantDepartureDelay = calculate_variance_departure_delay(data)

    return [meanArrivalDelay, meanDepartureDelay, medianArrivalDelay, medianDepartureDelay, variantArrivalDelay,
            variantDepartureDelay]


def get_some_elements_from_list(data):
    newList = []

    for i in range(10):
        newList.append(random.choice(data))

    return newList


def generateChartDelayArrival(testData):
    meanArrListX = []
    meanArrListY = []

    for stat in testData:
        meanArrListX.append(stat[0])
        meanArrListY.append(stat[1][0])

    for i in range(len(meanArrListY)):
        if meanArrListY[i] is None:
            meanArrListY[i] = 0

    return meanArrListX, meanArrListY

def generateChartDelayDeparture(testData):
    meanArrListX = []
    meanArrListY = []

    for stat in testData:
        meanArrListX.append(stat[0])
        meanArrListY.append(stat[1][1])

    for i in range(len(meanArrListY)):
        if meanArrListY[i] is None:
            meanArrListY[i] = 0

    return meanArrListX, meanArrListY


def generateChartAmountOfFlights(testData , results):
    ListX = []
    ListY = []

    for stat in testData:
        airport_code = stat[0]
        airport_data = [line for line in results if line[0] == airport_code]
        ListX.append(airport_code)
        ListY.append(countFlightsForAirport(airport_data))

    for i in range(len(ListY)):
        if ListY[i] is None:
            ListY[i] = 0

    return ListX, ListY

def get_month_number_from_datetime(datetime_str):
    datetime_str = datetime_str.strip(',')
    
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        month_number = dt.month
        return month_number
    except ValueError:
        return None

def plot_flights_per_month(flight_info):
    # Extract month and year from each flight record
    flight_months = [flight[3].strftime('%Y-%m') for flight in flight_info]

    # Count the number of flights for each month
    flight_counts = Counter(flight_months)

    # Separate the counts into two lists for plotting
    months = list(flight_counts.keys())
    counts = list(flight_counts.values())

    # Sort the months list to ensure the x-axis is in chronological order
    months.sort()
    counts = [flight_counts[month] for month in months]

    return months, counts

def generateChartAmountOfFlights123(data):
    ListX = []
    ListY = []

    flight_data = choose_flights_by_airports_randomly(airport_codes, data)

    for flight in flight_data:
        airport_code = flight[0]
        # Filter data for the current airport_code
        airport_specific_data = [f for f in flight_data if f[0] == airport_code]
        ListX.append(airport_code)
        # Now passing only one argument as expected by countFlightsForAirport
        ListY.append(countFlightsForAirport(airport_specific_data))

    for i in range(len(ListY)):
        if ListY[i] is None:
            ListY[i] = 0

    return ListX, ListY

def generateChartMeanFlights(results , type):

    df = pd.DataFrame(results, columns=['airport_code', 'flight_id', 'type', 'datetime', 'some_id', 'airport_code_dup', 'airport_name'])

    df_arrivals = df[df['type'] == type]

    airports = df_arrivals['airport_code'].unique()
    selected_airports = random.sample(list(airports), min(10, len(airports)))

    df_selected = df_arrivals[df_arrivals['airport_code'].isin(selected_airports)]
    grouped = df_selected.groupby('airport_code').size().reset_index(name='flight_count')

    mean_flights = grouped.groupby('airport_code')['flight_count'].mean().reset_index()


    return mean_flights['airport_code'] , mean_flights['flight_count']

def generateChartAmountOfAD_Flights(data , type):
    ListX = []
    ListY = []

    type_flight_data = []

    flight_data = choose_flights_by_airports_randomly(airport_codes, data)

    for flight in flight_data:
        if flight[2] == type: 
            type_flight_data.append(flight)

    for flight in type_flight_data:
        airport_code = flight[0]
        airport_specific_data = [f for f in flight_data if f[0] == airport_code]
        ListX.append(airport_code)
        ListY.append(countFlightsForAirport(airport_specific_data))

    for i in range(len(ListY)):
        if ListY[i] is None:
            ListY[i] = 0

    return ListX, ListY

def choose_flights_by_airports_randomly(airport_codes , flight_data):

    codes = random.sample(airport_codes, 10)

    chosen_fligths = []

    for code in codes:
        for flight in flight_data:
            if flight[0] == code:
                chosen_fligths.append(flight)

    return chosen_fligths

def countFlightsForOneAirport(code , data):
    return len([line for line in data if line[0] == code])

def countMonths(code, data):
    unique_months = set()

    airportData = [entry for entry in data if entry[0] == code]

    for entry in airportData:
        date = entry[3]
        year_month = (date.year, date.month)
        unique_months.add(year_month)

    return len(unique_months)

def countAllDelayTime(code , data):
    totalDelayTime = 0
    airportData = [f for f in data if f[0] == code]

    for entry in airportData:
        delayTime = entry[4]
        totalDelayTime += int(delayTime)
    return totalDelayTime


def checkFlights(airport_code, data):
    for flight in data:
        if flight[0] == airport_code:
            return True
    return False

def generateBasicDataForAiport(airport_code , data):

    dataList = []
    check =  checkFlights(airport_code , data)

    print(check)    

    if check == True:
    
        amountOfFlights = countFlightsForOneAirport(airport_code , data)
        meanAmountOfForMonthFlights = amountOfFlights / countMonths(airport_code , data)
        meanDelayTime = countAllDelayTime(airport_code , data) / amountOfFlights

    else:
        amountOfFlights = "No data"
        meanAmountOfForMonthFlights = "No data"
        meanDelayTime = "No data"

    print("Airport code: ", airport_code)
    print("Amount of flights: ", amountOfFlights)
    print("Mean amount of flights per month: ", meanAmountOfForMonthFlights)
    print("Mean delay time: ", meanDelayTime)

    dataList.append(airport_code)
    dataList.append(amountOfFlights)
    dataList.append(meanAmountOfForMonthFlights)
    dataList.append(meanDelayTime)

    return dataList