import csv
import os
from datetime import datetime, timezone

def extract_status_bits(status_word):
    # print(status_word)
    binary_str = format(status_word,'032b')
    pos = [2, 19, 26, 27, 28]
    results = []

    for p in pos:
        results.append(binary_str[31-p])
    # print(results)
    return results

def save_data_to_csv(data, filename, log_position_velocity=True):
    # Create the subfolder if it doesn't exist
    folder_name = 'data_logging'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Construct the full file path
    file_path = os.path.join(folder_name, filename)

    # Define headers based on the logging preference
    # headers = [
    #     "packetCounter", "sampleTimeFine", "utcTime",
    #     "Roll", "Pitch", "Yaw", "q0", "q1", "q2", "q3",
    #     "RateOfTurnX", "RateOfTurnY", "RateOfTurnZ",
    #     "AccelerationX", "AccelerationY", "AccelerationZ",
    #     "MagneticFieldX", "MagneticFieldY", "MagneticFieldZ",
    #     "DeltaVX", "DeltaVY", "DeltaVZ",
    #     "DeltaQ0", "DeltaQ1", "DeltaQ2", "DeltaQ3",
    #     "FreeAccX", "FreeAccY", "FreeAccZ",
    #     "BarometricPressure", "Temperature", "StatusWord"
    # ]
    headers = [
        "packetCounter", "sampleTimeFine", "utcTime", "FormattedUtcTime",
        "Roll", "Pitch", "Yaw",
        "q0", "q1", "q2", "q3",
        "RateOfTurnX", "RateOfTurnY", "RateOfTurnZ",
        "AccelerationX", "AccelerationY", "AccelerationZ",
        "MagneticFieldX", "MagneticFieldY", "MagneticFieldZ",
        "DeltaVX", "DeltaVY", "DeltaVZ",
        "DeltaQ0", "DeltaQ1", "DeltaQ2", "DeltaQ3",
        "FreeAccX", "FreeAccY", "FreeAccZ",
        "BarometricPressure", "Temperature",
         "StatusWord", "GnssFix", "ClippingIndicatin", "GnssTimePulse", "RtkStatus",
    ]
    
    if log_position_velocity:
        headers += [
            "Latitude", "Longitude", "Altitude",
            "VelocityEast", "VelocityNorth", "VelocityUp",
        ]

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(headers)  # Write the header only if the file doesn't exist
        
        formattedUtcTime = datetime.fromtimestamp(data.utcTime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f %Z')
        status_bits = extract_status_bits(data.statusWord)
        print("STATUS BITS GnssFix,ClippingIndicatin,GnssTimePulse,RtkStatus", status_bits)


        row = [
            data.packetCounter if data.packetCounterAvailable else '',
            data.sampleTimeFine if data.sampleTimeFineAvailable else '',
            data.utcTime if data.utcTimeAvailable else '',
            formattedUtcTime,
            data.euler[0] if data.eulerAvailable else '',
            data.euler[1] if data.eulerAvailable else '',
            data.euler[2] if data.eulerAvailable else '',
            data.quat[0] if data.quaternionAvailable else '',
            data.quat[1] if data.quaternionAvailable else '',
            data.quat[2] if data.quaternionAvailable else '',
            data.quat[3] if data.quaternionAvailable else '',
            data.rot[0] * data.rad2deg if data.rotAvailable else '',
            data.rot[1] * data.rad2deg if data.rotAvailable else '',
            data.rot[2] * data.rad2deg if data.rotAvailable else '',
            data.acc[0] if data.accAvailable else '',
            data.acc[1] if data.accAvailable else '',
            data.acc[2] if data.accAvailable else '',
            data.mag[0] if data.magAvailable else '',
            data.mag[1] if data.magAvailable else '',
            data.mag[2] if data.magAvailable else '',
            data.deltaV[0] if data.deltaVAvailable else '',
            data.deltaV[1] if data.deltaVAvailable else '',
            data.deltaV[2] if data.deltaVAvailable else '',
            data.deltaQ[0] if data.deltaQAvailable else '',
            data.deltaQ[1] if data.deltaQAvailable else '',
            data.deltaQ[2] if data.deltaQAvailable else '',
            data.deltaQ[3] if data.deltaQAvailable else '',
            data.freeAcc[0] if data.freeAccAvailable else '',
            data.freeAcc[1] if data.freeAccAvailable else '',
            data.freeAcc[2] if data.freeAccAvailable else '',
            data.baropressure if data.baropressureAvailable else '',
            data.temperature if data.temperatureAvailable else '',
            data.statusWord if data.statusWordAvailable else '',
            status_bits[0],
            status_bits[1],
            status_bits[2],
            status_bits[4] + status_bits[3],
        ]
        if log_position_velocity:
            row += [
                data.latlon[0] if data.latlonAvailable else '',
                data.latlon[1] if data.latlonAvailable else '',
                data.altitude if data.altitudeAvailable else '',
                data.vel[0] if data.velocityAvailable else '',
                data.vel[1] if data.velocityAvailable else '',
                data.vel[2] if data.velocityAvailable else ''
            ]

        writer.writerow(row)  # Write the data row
