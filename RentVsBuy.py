# Tommy Murray
# tkm2uft

import pandas as pd
import matplotlib.pyplot as plt
import json

'''
Program to determine whether buying or renting a home is preferable.

This requires a csv containing annual values of the stock market (S&P 500), 
real estate appreciation, andinflation.
I have submitted a copy of the necessary CSV to github. I acquired the data
from Professor Damodoran's website (linked below):
https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html

4 main metrics are calculated annually for both the homeowning option and renting option:
Annual costs, total costs, investment value, and net worth.
Annual costs are costs incurred that year.
Total costs are are the sum of all costs up through that year to date (YTD).
Investment value is measured differently for the two options.
    For the housing option, the current investment value is the value of the individual's equity in the house.
    For the renting option, any money that would have been spent on housing costs that is not spent on rent costs is presumed to be invested in stocks.
    The current investment value is the value of an investment in stocks.
Net worth is value of the investment in that year minus total costs in that year.

These 4 annual metrics are stored in 8 lists (4 for homeowning, 4 for renting).
These lists are called the "comparison analysis," as they compare homeowning vs renting.

These 4 metrics are graphed across the timespan of the mortgage. 4 graphs are produced, each
showing the performance of homeowning and renting for a single metric.

Additionally, an amortization schedule is produced showing the montlhy mortgage payments
if the homeowning option were to chosen. These payments are split into principal repayments and interest fees.

The ultimate product is a json file containing the amortization schedule
and the comparison analysis.

'''


def compound_growth(principal, rate, time):
    # Calculates compound interest
    amount = principal * (pow((1 + rate / 100), time))
    cg = amount - principal
    return amount, cg

def sum_compound_growth(principal, rate, time):
    # Calculates the summation of all years from a compounding interest (i.e. value after year 1 + value after year 2 ...)
    summation = 0
    for i in range(time + 1):
        summation += compound_growth(principal, rate, i)[0]
    return summation
      
# Read in the data
finance_data = pd.read_csv(r'damodaran finance data.csv')

# Extract several variables from the data while error-catching
while True:
    try:
        # Define expected annual inflation
        inflation = finance_data['Inflation Rate'].mean()*100
        
        # Define expected annual stock appreciation
        stock_appr = finance_data['S&P 500 (includes dividends)'].mean()*100
        adj_stock_appr = stock_appr - inflation
        
        # Define expected annual housing appreciation
        house_appr = finance_data['Real Estate'].mean()*100
        adj_house_appr = house_appr - inflation
        break
    except KeyError:
        print('There was an error: the column title you tried to call does not exist in the file you loaded')
        break
    
    
# Define rent cost variables:

# Annual rent
rent = 24000

# Annual renter's insurance
rent_insur = 200

# Define homeowning variables:
    
# Cost of the house
house_cost = 800000

# Percent of the down payment
pct_down_pymt = 25

# Length of the mortgage (years)
mortg_timespan = 30

# Annual interest rate on mortgage
annual_interest = 3

# State house is located in
state = 'VA'

# Annual repair fees for the house
repair_fees = 400

# Annual HOA fees for the house
hoa_fees = 360

# Annual housing insurance
house_insur = 5000

# Transaction costs from the purchase of the house
transaction_costs = 16000

# Closing costs from the sale of the house
closing_costs = 40000

# Calculate housing costs variables
mortg_principal = house_cost - house_cost*pct_down_pymt/100
remaining_mortg_principal = mortg_principal

monthly_interest = annual_interest/100/12

num_months = 12 * mortg_timespan

monthly_mortg_pymt = mortg_principal * ( monthly_interest * (1 + monthly_interest)**num_months ) / ( (1 + monthly_interest)**num_months - 1)

annual_mortg_pymt = 12 * monthly_mortg_pymt

# Calculate renting gains variables
# Note: renting gains is defined as money that would have been spent on housing fees
# but is instead able to be invested in the stock market.
# The intial investment presumes the money that would have been spent securing
# the house purchase is instead invested (down payment and transaction costs)
initial_invsmt = house_cost*pct_down_pymt/100 + transaction_costs

# ANNUAL FOR-LOOP
# For-loop that iterates through each year of the mortgage, calculating:
# the annual house costs,
# the total house costs (up through that year, that is, YTD year-to-date), 
# the value of the owned house (increases due to equity in the house rising from to principal repayments and also due to appreciation of the real estate market), 
# the annual rent costs,
# the total rent costs (YTD),
# the value of the investment (stocks purchased in the renting scenario),
# an individual's net worth (YTD) from homeowning
# an individual's net worth (YTD) from renting.

# Additionally, there is a MONTHLY FOR-LOOP inside. This calculates the monthly
# amortization schedule (composed of monthly principal payments and monthly interest fees)

# Define variables necessary for the for-loop.
total_house_costs = 0

list_total_house_costs = []

list_annual_house_costs = []

house_value = house_cost

list_house_values = []

list_owned_house_values = []

total_rent_costs = 0

list_total_rent_costs = []

list_annual_rent_costs = []

invsmt_value = initial_invsmt

list_invsmt_values = []

list_net_worth_house = []

list_net_worth_rent = []


list_monthly_interest_pymt = []
list_monthly_principal_pymt = []

year_counter = 0

list_year_counter = []

# Execute annual for-loop
for year in range(mortg_timespan):
        
    year_counter += 1
    list_year_counter.append(year_counter)
    
    # Execute monthly for-loop
    annual_principal_pymt = 0
    for month in range(12):
        monthly_interest_pymt = remaining_mortg_principal*annual_interest/100/12
        list_monthly_interest_pymt.append(monthly_interest_pymt)
        
        monthly_principal_pymt = monthly_mortg_pymt - monthly_interest_pymt
        list_monthly_principal_pymt.append(monthly_principal_pymt)
        
        annual_principal_pymt += monthly_principal_pymt
        
        remaining_mortg_principal -= monthly_principal_pymt
        
    # Calculate annual housing costs
    house_insur = compound_growth(house_insur, inflation, 1)[0]
    
    annual_house_costs = annual_mortg_pymt + repair_fees + hoa_fees + house_insur

    total_house_costs += annual_house_costs
    
    list_total_house_costs.append(total_house_costs)
    
    list_annual_house_costs.append(annual_house_costs)
    
    # Calculate the house value
    house_value = compound_growth(house_value, adj_house_appr, 1)[0]
    
    list_house_values.append(house_value)
    
    # Calculate the value of the individual's equity in the house
    pct_house_owned = pct_down_pymt/100 + (mortg_principal-remaining_mortg_principal)/house_cost
    owned_house_value = pct_house_owned * house_value
    
    list_owned_house_values.append(owned_house_value)
    
    # Calculate annual renting costs
    rent = compound_growth(rent, inflation, 1)[0]
    
    rent_insur = compound_growth(rent_insur, inflation, 1)[0]
    
    annual_rent_costs = rent + rent_insur
    
    list_annual_rent_costs.append(annual_rent_costs)
    
    total_rent_costs += annual_rent_costs
    
    list_total_rent_costs.append(total_rent_costs)
    
    # Calculate annual investment
    # Note: as noted above, the investment is defined as any money that would have been
    # spent on housing but is instead invested in the stock market. Annual investment
    # is the house costs for that year less the rent costs for that year.
    annual_invsmt = annual_house_costs - annual_rent_costs
    
    # Update the investment value
    invsmt_value += annual_invsmt
    
    invsmt_value = compound_growth(invsmt_value, adj_stock_appr, 1)[0]
    
    list_invsmt_values.append(invsmt_value)
    
    # Calculate YTD net worth. Net worth is defined as gains less losses. Gains
    # are either the owned house value or the stock investment value. Losses are
    # either the total house costs or total rent costs.
    net_worth_house = owned_house_value - total_house_costs
    
    list_net_worth_house.append(net_worth_house)
    
    net_worth_rent = invsmt_value - total_rent_costs
    
    list_net_worth_rent.append(net_worth_rent)

# Create the amortization schedule as a dataframe
amortization_schedule = pd.DataFrame(
    {'monthly interest payment': list_monthly_interest_pymt,
     'monthly principal payment': list_monthly_principal_pymt
     })

# Create the yearly data table as a dataframe
comparison_analysis = pd.DataFrame(
    {'year': list_year_counter,
     'annual homeowning costs': list_annual_house_costs,
     'annual renting costs': list_annual_rent_costs,
     'total homeowning costs (YTD)': list_total_house_costs,
     'total renting costs (YTD)': list_total_rent_costs,
     'owned house value': list_owned_house_values,
     'investment value': list_invsmt_values,
     'net worth (homeowning) (YTD)': list_net_worth_house,
     'net worth (renting) (YTD)': list_net_worth_rent
     })

# Plot graphs comparing the outcomes of homeowning vs renting across the entire
# mortgage period

plt.plot(list_year_counter, list_annual_house_costs, label = "annual homeowning costs")
plt.plot(list_year_counter, list_annual_rent_costs, label = "annual renting costs")
plt.legend()
plt.title("Annual Costs")
plt.show()

plt.plot(list_year_counter, list_total_house_costs, label = "total homeowning costs (YTD)")
plt.plot(list_year_counter, list_total_rent_costs, label = "total renting costs (YTD)")
plt.legend()
plt.title("Total Costs")
plt.show()

plt.plot(list_year_counter, list_owned_house_values, label = "owned house value")
plt.plot(list_year_counter, list_invsmt_values, label = "investment value")
plt.legend()
plt.title("Gains")
plt.show()

plt.plot(list_year_counter, list_net_worth_house, label = "net worth (homeowning) (YTD)")
plt.plot(list_year_counter, list_net_worth_rent, label = "net worth (renting) (YTD)")
plt.legend()
plt.title("Net worth")
plt.show()

# Create a dictionary containing the amortization schedule and all columns from the
# annual data table
dict_final_data = {
        'amortization schedule':
         {'monthly principal repayments': list_monthly_principal_pymt,
          'monthly interest fees': list_monthly_interest_pymt
             },
         'comparison analysis':
        {'year': list_year_counter,
        'annual homeowning costs': list_annual_house_costs,
        'annual renting costs': list_annual_rent_costs,
        'total homeowning costs (YTD)': list_total_house_costs,
        'total renting costs (YTD)': list_total_rent_costs,
        'owned house value': list_owned_house_values,
        'investment value': list_invsmt_values,
        'net worth (homeowning) (YTD)': list_net_worth_house,
        'net worth (renting) (YTD)': list_net_worth_rent
        }
    }

# Turn dict_final_data into a json as a final deliverable

out_file = open("json_annual_data.json", "w") 

json.dumps(dict_final_data, indent = 6)

out_file.close() 

