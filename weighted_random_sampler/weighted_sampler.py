from vose_sampler import VoseAlias

def day_count(day, data):
    count = 0
    for x in data:
        count = count + data[x]["avail"][day]
    return count

def weights(ave, pid, day_id, data):
    np_d = day_count(day_id, data)
    ne_i = data[pid]["events"][day_id]
    nd_i = sum(data[pid]["avail"])
    av_i = data[pid]["avail"][day_id]
    weight = (1./np_d)*(ave - ne_i)*(av_i/nd_i)
    return weight


def main():

    from get_data import people_data, calendar_data
    data = people_data

    # main
    day = 0
    days = 5
    people = 3
    ave = (days/people)
    weight_sum = 0

    # initialise weight
    for pid, datas in data.items():
        data[pid]["weights"] = [0] * days

    # initialise events
    for pid, datas in data.items():
        data[pid]["events"] = [0] * days

    # initialise dist
    dist = {}

    for pid, datas in data.items():

        weight_i = weights(ave, pid, day, data)
        weight_sum = weight_sum + weight_i

        data[pid]["weights"][day] = weight_i
        dist[pid] = weight_i

        print(pid, weight_i)

    for pid, datas in data.items():
        data[pid]["weights"] = data[pid]["weights"][day] / weight_sum
        print(pid, data[pid]["weights"])

    VA = VoseAlias(dist)
    selected = VA.sample_n(size=1)

    print(data[selected[0]]["name"], "are selected.")
    print(data)


if __name__ == "__main__":
    main()
