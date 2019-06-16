
def get_total_route_time(route, ncars_by_route):
    total_time = 0
    for i, street in enumerate(route):
        if i >= ncars_by_route.shape[0]:
            total_time += 1
        else:
            total_time += ncars_by_route.loc[i, street] + 1
    return total_time
