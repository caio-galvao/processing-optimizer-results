import os
import json
import sys

def main():
    demand_path = sys.argv[1]

    flavors = open(demand_path)

    flavors = [flavors.readline().split('\n')[0].split(',')[-1]]

    #All reserves are standard
    reserve_no1y_code = '4NA7Y494T4'
    reserve_prt1y_code = 'HU7G6KETJZ'
    reserve_all1y_code = '6QCMYABX3D'

    reserve_no3y_code = 'BPH4J8HBKS'
    reserve_prt3y_code = '38NPMPTW36'
    reserve_all3y_code = 'NQ3QZPMQV9'

    ondemand_code = 'JRTCKXETXF'
    hourly_cost_code = '6YS6EN2CT7'
    upfront_cost_code = '2TG2D8R56U'
    output = []
    ind = 0

    output_costs = open('reserve_prt1y_code2.csv', 'w')
    output_costs.write('Platform,Region,Instance,On.Demand_Hour,No.UP.1Y_Month,Part.UP.1Y_UP,Part.UP.1Y_Month,All.UP.1Y_UP,Part.UP.3Y_UP,Part.UP.3Y_Month,All.UP.3Y_UP\n')


    for flavor in flavors:
        os.system('aws pricing get-products --region us-east-1 \
            --service-code AmazonEC2 --filters Type=TERM_MATCH,Field=instanceType,Value={instanceType} \
            Type=TERM_MATCH,Field=location,Value="US East (N. Virginia)" \
            Type=TERM_MATCH,Field=usagetype,Value=BoxUsage:{instanceType} \
            Type=TERM_MATCH,Field=operatingSystem,Value=Linux \
            Type=TERM_MATCH,Field=preInstalledSw,Value=NA --max-results 30 --output json \
            > {instanceType}.json'.format(instanceType = flavor))
        print('Current: {}'.format(flavor))
        cur_cost = open(flavor + '.json', 'r')
        cur_cost = json.load(cur_cost)
        
        if len(cur_cost['PriceList']) != 0:
            product = json.loads(cur_cost['PriceList'][0])
            product_code = product['product']['sku']
            market_code = product_code + '.' + ondemand_code
            market_hourly_code = market_code + '.' + hourly_cost_code
            ondemand_cost = product['terms']['OnDemand'][market_code]
            ondemand_cost = ondemand_cost['priceDimensions'][market_hourly_code]['pricePerUnit']['USD']

            curr_reserve_code = reserve_prt1y_code # Change to the reserve code you are interested in.
            market_code = product_code + '.' + curr_reserve_code
            curr_reserve_hourly_code = market_code + '.' + hourly_cost_code

            try:
                reserve_cost_hourly = product['terms']['Reserved'][market_code]
                reserve_cost_hourly = reserve_cost_hourly['priceDimensions'][curr_reserve_hourly_code]['pricePerUnit']['USD']

                ## This part SHOULDN'T use in NO UPFRONT OPTIONS.
                curr_reserve_upfront_code = market_code + '.' + upfront_cost_code
                reserve_cost_upfront = product['terms']['Reserved'][market_code]
                reserve_cost_upfront = reserve_cost_upfront['priceDimensions'][curr_reserve_upfront_code]['pricePerUnit']['USD']
                
                ##para usar em no upfront
                #reserve_cost_upfront = 00.00000
                
                output.append(float(ondemand_cost))
                output.append(float(reserve_cost_hourly))
                output.append(float(reserve_cost_upfront))
                output_costs.write('Linux,US East (N. Virginia),{},${:.5f} per Hour,0,{:.5f},{:.5f},0,0,0,0\n'.format(flavor, float(ondemand_cost), float(reserve_cost_upfront), float(reserve_cost_hourly)))
            except:
                print("Flavor " + flavor + " não tem dados")
                output_costs.write('Linux,US East (N. Virginia),{}\n'.format(flavor))
                
        else:
            print('No offers')
            output.append(0.0)
            output.append(0.0)
            output.append(0.0)
        ind += 1
        os.system('rm {}.json'.format(flavor))
        print('Done {} of {}'.format(ind, len(flavors)))

    print(' '.join(list(map(str, output))))

if __name__ == "__main__":
    main()