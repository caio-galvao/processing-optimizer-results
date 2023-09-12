import csv

def get_price(instanceType, market):
    filename = 'reserve_prt1y_code.csv'
    with open(filename, mode='r') as file:
        while True:
            line = file.readline()
            if not line: 
                break
            #line: timeId, instanceType, market, count
            line = line.split(',') 
            if line[0] == 'Platform': #header
                continue

            if line[2] == instanceType:
                cost = 0
                if market == 'od':
                    cost = float(line[3])
                elif market == 'r':
                    cost = float(line[4])
                return cost
        print(instanceType)
        return 0

filename = "total_purchases.csv"
max_t = 26299
opt_vs_all_od = [[0, 0] for i in range(max_t + 1)]
od_vs_re = [[0, 0] for i in range(max_t + 1)]

with open(filename, mode='r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        #line: timeId, instanceType, market, count
        timeId, instanceType, market, count = line.split(',')
        if timeId == 'timeId': #header
            continue

        timeId = int(timeId)
        count = int(count)

        if market == 'OnDemand':
            od_vs_re[timeId][0] += count * get_price(instanceType, 'od')
            opt_vs_all_od[timeId][0] += count * get_price(instanceType, 'od')
        elif market == 'Reserved':
            od_vs_re[timeId][1] += count * get_price(instanceType, 'r')
            opt_vs_all_od[timeId][0] += count * get_price(instanceType, 'r')

        opt_vs_all_od[timeId][1] += count * get_price(instanceType, 'od')
    
output1 = open('opt_vs_all_od.csv', 'w')
writer1 = csv.writer(output1)
writer1.writerow(['timeId', 'opt_cost', 'all_od_cost'])
for line in opt_vs_all_od:
    writer1.writerow(line)
output1.close()

output2 = open('od_vs_re.csv', 'w')
writer2 = csv.writer(output2)
writer2.writerow(['timeId', 'od_cost', 'res_cost'])
for line in od_vs_re:
    writer2.writerow(line)
output2.close()