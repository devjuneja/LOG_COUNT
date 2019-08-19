from datetime import datetime, timedelta
import re

i_current_year = 2019


def is_two_hours(time_current, time_log):
    """Return true if current time is less than two hours from log time"""
    # timedelta object for two hours
    time_two_hours = timedelta(hours=2)
    time_difference = time_current-time_log
    return time_difference <= time_two_hours


def count_flaps(s_logs, time_device):
    """Return number of flaps within two hours of current device time."""
    i_count_logs = 0
    # dictionary for months
    d_months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }

    # Regex pattern to match and group log entry
    # 1. Month
    # 2. Day
    # 3. Hour
    # 4. Minute
    # 5. Second
    # 6. Millisecond
    log_pattern = re.compile(
        "[0-9]*:\s+.*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+" +
        "([0-9]+)\s+([0-9]+):([0-9]+):([0-9]+).([0-9])+")

    # Loop through each log line
    for log in s_logs.split("\n"):
        log_match = log_pattern.match(log)
        log_time = datetime(
            i_current_year,
            d_months[log_match.group(1)],
            int(log_match.group(2)),
            int(log_match.group(3)),
            int(log_match.group(4)),
            int(log_match.group(5)))
        i_count_logs = i_count_logs + is_two_hours(time_device, log_time)

    # Return count of flaps within two hours
    return int(i_count_logs/2)


reference_datetime = datetime(2019, 1, 13, 3, 50, 33)
# output of:
# sh logg | i DUAL-5-NBRCHANGE.*<neighbour-ip>\s
logs = '''000048: Jan 13 03:50:33.749: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX(GigabitEthernet0/0) is up: new adjacency
000047: Jan 13 02:31:27.677: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX(GigabitEthernet0/0) is up: new adjacency
000045: Jan 13 02:20:10.940: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX (GigabitEthernet0/0) is up: new adjacency
000047: Jan  3 03:07:21.283: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX (GigabitEthernet0/0) is up: new adjacency
000047: Jan  3 02:48:21.379: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX (GigabitEthernet0/0) is up: new adjacency
000047: Jan  3 02:04:00.043: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX (GigabitEthernet0/0) is up: new adjacency
000048: Jan  3 01:50:54.129: %DUAL-5-NBRCHANGE: EIGRP-IPv4 100: Neighbor XXXX (GigabitEthernet0/0) is up: new adjacency'''

print(count_flaps(logs, reference_datetime))
