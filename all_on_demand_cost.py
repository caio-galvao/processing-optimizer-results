def get_all_od_cost(opt_vs_all_od, demand_path, prices):
    with open(demand_path, mode='r') as file:
        line = file.readline()
        instances_types = line.split(',')
        while True:
            line = file.readline()
            if not line:
                break
            #line: timeId, instanceType, market, count
            line = line.split(',')
            if line[0] == 'Hour': #header
                continue
            
            time = int(line[0])

            for i in range(1, len(line)):
                usage = int(line[i])
                instanceType = instances_types[i]
                instance_prices = prices.get(instanceType)
                if instance_prices != None:
                    opt_vs_all_od[time][2] += usage * instance_prices[0]
    return opt_vs_all_od