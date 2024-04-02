import json

CLOSEKEY = "Weekly Time Series"

data_raw = json.load(open("data.json","r"))
data = []
for k in data_raw:
	data.append(float(data_raw[k][CLOSEKEY]))


starting_money = 10000
money = starting_money
shares = 0


samplesize = 8 # in weeks
sample = []
for week in range(len(data)):
	if len(sample) < samplesize:
		sample.append(data[week])
		continue
	avgslope = 0
	for i in range(samplesize-1):
		avgslope+= (sample[i+1]-sample[i])/(samplesize-1)
	
	if avgslope < -2:
		shares += money/data[week]
		money = 0
	if avgslope > 2:
		money += shares*data[week]
		shares = 0

	if abs(avgslope)>2:
		print(money,shares)

	sample = sample[1:]+[data[week]]

money += shares*data[-1]
shares = 0

print("starting amount: ",starting_money)
print("ending amount: ", money)
print("% increase per year:",(((money/starting_money)**(1/len(data)))**52)*100 - 100)