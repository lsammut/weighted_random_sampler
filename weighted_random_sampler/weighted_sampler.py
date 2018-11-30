import math
from vose_sampler import VoseAlias

def day_count(day, data):
    count = 0
    for pid in data:
        count = count + data[pid]["avail"][day]
    return count

def weights(ave, pid, day_id, data):
    np_d = day_count(day_id, data)
    ne_i = data[pid]["events"][day_id]
    nd_i = sum(data[pid]["avail"])
    av_i = data[pid]["avail"][day_id]

    weight = (1./np_d)*(ave - ne_i)*(av_i/nd_i)

    return weight


def calc_weights(pid, day_id, data, calendar):

    options = calendar['calendars']
    days = calendar['days']
    people = calendar['people']

    days_left = days - day_id
    expected_events = days / people

    # pref = sum(data[pid]["pref"])
    # options = len(data[pid]["pref"])
    group_avail = day_count(day_id, data)   # np_d
    avail_days = sum(data[pid]["avail"])    # nd_i
    single_avail = data[pid]["avail"][day_id] # av_i
    accrued_events = sum(data[pid]["events"]) # ne_i


    a = (single_avail/group_avail)                    # group size factor
    b = (expected_events - accrued_events)  # positive event factor
    c = (1. / avail_days)           # availability factor
    d = (expected_events - accrued_events - days_left)
    # d = (options / pref)                    # preference facgtor

    weight = a * math.exp(d)

    return weight

def main():

    from get_data import people_data, calendar_data

    data = people_data
    days = calendar_data['days']
    people = calendar_data['people']
    ave = (days / people)


    # initialise weight
    weight_sum = 0
    for pid, datas in data.items():
        data[pid]["weights"] = [0] * days

    # initialise events
    for pid, datas in data.items():
        data[pid]["events"] = [0] * days

    # initialise dist
    dist = {}

    for day in range(days):

        for pid, datas in data.items():

            # weight = weights(ave, pid, day, data)
            weight = calc_weights(pid, day, data, calendar_data)
            weight_sum = weight_sum + weight

            data[pid]["weights"][day] = weight

        for pid, datas in data.items():
            data[pid]["weights"][day] = data[pid]["weights"][day] / weight_sum

            # allocate distribution
            dist[pid] = data[pid]["weights"][day]

        VA = VoseAlias(dist)
        selected = VA.sample_n(size=10)

        # update events array
        for pid, datas in data.items():
            data[pid]["events"][day]= int(selected[0] == pid)

        # print(data[selected[0]]["name"], "are selected.")

    # print(data)

    for pid, datas in data.items():
        print(data[pid]["events"], sum(data[pid]["events"]))

    return(data)


if __name__ == "__main__":
    main()
