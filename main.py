import json

CLOSEKEY = "4. close"

data_raw = json.load(open("data.json","r"))["Weekly Time Series"]
data = []
for k in data_raw:
	data.append(float(data_raw[k][CLOSEKEY]))


# best lower and upper bound is -3 and 2
def calculatemoneymade(lowerbound,upperbound,starting_money=1):
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
		
		if avgslope < lowerbound:
			shares += money/data[week]
			money = 0
		if avgslope > upperbound:
			money += shares*data[week]
			shares = 0

		sample = sample[1:]+[data[week]]

	money += shares*data[-1]
	inc_per_year = (((money/starting_money)**(1/len(data)))**52)*100 - 100
	
	return {
		"money": money,
		"inc per year":  inc_per_year
	}

print(calculatemoneymade(-3,2))