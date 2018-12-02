import math
from vose_sampler import VoseAlias

"""
Calculate weighted probabilities for Vose Alias Sampling.


Values specific to advent calendar application, from data object

 * people:          number of people                        
 * days:            total number of days in time interval   
 * single_avail:    daily availability                      
 * group_avail:     number of people available on the day   
 * avail_days:      number of available days                
 * accrued_events:  number of positive events               
 
Derived values 
 * expected_events: average number of events
 * weight:          calculated
"""

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y


def day_count(day, data):
    """count the number of people available on a particular day"""
    count = 0
    for pid in data:
        count = count + data[pid]["avail"][day]
    return count


def count_days(day, pid, data):
    """count the number available days left for a particular person"""
    count = 0
    for day in range(day, len(data[pid]["avail"])):
        count = count + data[pid]["avail"][day]
    return count


def calc_weights(pid, day, data, calendar):

    options = calendar['calendars']
    days = calendar['days']
    people = calendar['people']

    pref = sum(data[pid]["pref"])
    # options = len(data[pid]["pref"])

    group_avail = day_count(day, data)
    avail_days = count_days(day,pid,data)
    single_avail = data[pid]["avail"][day]
    accrued_events = sum(data[pid]["events"])

    days_left = days - day
    expected_events = days / people

    a = safe_div(single_avail, group_avail)                # group size factor
    b = (expected_events - accrued_events)          # positive event factor
    c = (avail_days - days_left)                    # availability factor
    # d = (options / pref)                            # preference factor

    weight = a * (math.exp(b) / math.exp(c))

    return weight


def main(people_data, calendar_data):

    data = people_data
    days = calendar_data['days']

    # initialise weight
    for pid, datas in data.items():
        data[pid]["weights"] = [0] * days

    # initialise events
    for pid, datas in data.items():
        data[pid]["events"] = [0] * days

    # initialise dist
    dist = {}
    winners = []

    for day in range(days):
        weight_sum = 0

        for pid, datas in data.items():

            # weight = weights(ave, pid, day, data)
            weight = calc_weights(pid, day, data, calendar_data)
            weight_sum = weight_sum + weight
            # assign weight to data structure
            data[pid]["weights"][day] = weight

        for pid, datas in data.items():
            data[pid]["weights"][day] = safe_div(data[pid]["weights"][day], weight_sum)

            # allocate distribution
            dist[pid] = data[pid]["weights"][day]

        VA = VoseAlias(dist)
        selected = VA.sample_n(size=1)

        # update events array
        for pid, datas in data.items():
            data[pid]["events"][day]= int(selected[0] == pid)

        # assign winners array
        winners.append(data[selected[0]]["name"])

    return data, winners


if __name__ == "__main__":

    from get_data import people_data

    calendar_data = {
        'days': 48,
        'calendars': 2,
        'people': len(people_data)
    }

    data, winners = main(people_data, calendar_data)
    days = calendar_data['days']

    # print event array
    for pid, datas in data.items():
        print(data[pid]["events"], sum(data[pid]["events"]))

    # print winners by name
    print(winners)

