import json

CLOSEKEY = "4. close"

data_raw = json.load(open("data.json","r"))["Weekly Time Series"]
data = []
dates = list(data_raw.keys())[::-1]
for k in dates:
	data.append(float(data_raw[k][CLOSEKEY]))


# best lower and upper bound is -3 and 2 for IBM
# best lower and upper bound is -5.8 and 9.1 for S&P 500
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
			#money += shares*data[week]
			#shares = 0
			#print(money+shares*data[week],"sell")
			shares += money/data[week]
			money = 0
		if avgslope > upperbound:
			#shares += money/data[week]
			#money = 0
			#print(money+shares*data[week],"buy")
			money += shares*data[week]
			shares = 0

		sample = sample[1:]+[data[week]]

	money += shares*data[-1]
	inc_per_year = (((money/starting_money)**(1/len(data)))**52)*100 - 100
	iflazymoney = starting_money*data[-1]/data[0]
	iflazy_inc_per_year = (((iflazymoney/starting_money)**(1/len(data)))**52)*100 - 100
	
	
	return {
		"starting money":starting_money,
		"money": money,
		"inc per year":  inc_per_year,
		"iflazymoney": iflazymoney,
		"lazy inc per year": iflazy_inc_per_year
	}


result = calculatemoneymade(-5.8,9.1,1000)
# testing out inc per year calculation
#print((result["inc per year"]/100+1)**(int(dates[-1][:4])-int(dates[0][:4]))*result["starting money"],result["money"])
print(f"from {dates[0]} to {dates[-1]}")
print(f"bot inc per year: {result["inc per year"]:0.2f}%")
print(f"from ${result["starting money"]:0.2f} to ${result["money"]:0.2f}")
print(f"{result["money"]/result["starting money"]*100-100:0.0f}% increase")
print(f"not selling inc per year: {result["lazy inc per year"]:0.2f}%")
print(f"from ${result["starting money"]:0.2f} to ${result["iflazymoney"]:0.2f}")
print(f"{result["iflazymoney"]/result["starting money"]*100-100:0.0f}% increase")
