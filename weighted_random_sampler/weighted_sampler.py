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

            weight = weights(ave, pid, day, data)
            weight_sum = weight_sum + weight

            data[pid]["weights"][day] = weight
            dist[pid] = weight


        for pid, datas in data.items():
            data[pid]["weights"][day] = data[pid]["weights"][day] / weight_sum

            VA = VoseAlias(dist)
            selected = VA.sample_n(size=1)

            # update events array
            for pid, datas in data.items():
                data[pid]["events"][day]= int(selected[0] == pid)

            print(data[selected[0]]["name"], "are selected.")

    return(data)


if __name__ == "__main__":
    main()
