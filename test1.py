
import sys, os
import requests
from harvest_trading212 import get_tags
import datetime

api_key = '3bade15813ae479c5bd26b3aa8914369'

enterprise_values = ['date', 'stockPrice', 'numberOfShares', 'marketCapitalization', 
					 'minusCashAndCashEquivalents', 'addTotalDebt', 'enterpriseValue'] # date?
ratios_ttm = ["dividendYielTTM", "dividendYielPercentageTTM", "peRatioTTM", "pegRatioTTM",
			  "payoutRatioTTM", "currentRatioTTM", "quickRatioTTM", "cashRatioTTM", "daysOfSalesOutstandingTTM",
			  "daysOfInventoryOutstandingTTM", "operatingCycleTTM", "daysOfPayablesOutstandingTTM",
			  "cashConversionCycleTTM", "grossProfitMarginTTM", "operatingProfitMarginTTM", 
			  "pretaxProfitMarginTTM", "netProfitMarginTTM", "effectiveTaxRateTTM", "returnOnAssetsTTM",
			  "returnOnEquityTTM", "returnOnCapitalEmployedTTM", "netIncomePerEBTTTM", "ebtPerEbitTTM",
			  "ebitPerRevenueTTM", "debtRatioTTM", "debtEquityRatioTTM", "longTermDebtToCapitalizationTTM",
			  "totalDebtToCapitalizationTTM", "interestCoverageTTM", "cashFlowToDebtRatioTTM",
			  "companyEquityMultiplierTTM", "receivablesTurnoverTTM", "payablesTurnoverTTM",
			  "inventoryTurnoverTTM", "fixedAssetTurnoverTTM", "assetTurnoverTTM", "operatingCashFlowPerShareTTM",
			  "freeCashFlowPerShareTTM", "cashPerShareTTM", "operatingCashFlowSalesRatioTTM", "freeCashFlowOperatingCashFlowRatioTTM",
			  "cashFlowCoverageRatiosTTM", "shortTermCoverageRatiosTTM", "capitalExpenditureCoverageRatioTTM",
			  "dividendPaidAndCapexCoverageRatioTTM", "priceBookValueRatioTTM", "priceToBookRatioTTM",
			  "priceToSalesRatioTTM", "priceEarningsRatioTTM", "priceToFreeCashFlowsRatioTTM", "priceToOperatingCashFlowsRatioTTM",
			  "priceCashFlowRatioTTM", "priceEarningsToGrowthRatioTTM", "priceSalesRatioTTM", "dividendYieldTTM",
			  "enterpriseValueMultipleTTM", "priceFairValueTTM"]
key_metrics_values = ['date', 'revenuePerShare', 'netIncomePerShare', 'operatingCashFlowPerShare', 'freeCashFlowPerShare', 
				   'cashPerShare', 'bookValuePerShare', 'tangibleBookValuePerShare', 'shareholdersEquityPerShare', 
				   'interestDebtPerShare', 'marketCap', 'enterpriseValue', 'peRatio', 'priceToSalesRatio', 'pocfratio', 
				   'pfcfRatio', 'pbRatio', 'ptbRatio', 'evToSales', 'enterpriseValueOverEBITDA', 'evToOperatingCashFlow', 
				   'evToFreeCashFlow', 'earningsYield', 'freeCashFlowYield', 'debtToEquity', 'debtToAssets', 'netDebtToEBITDA', 
				   'currentRatio', 'interestCoverage', 'incomeQuality', 'dividendYield', 'payoutRatio', 'salesGeneralAndAdministrativeToRevenue', 
				   'researchAndDdevelopementToRevenue', 'intangiblesToTotalAssets', 'capexToOperatingCashFlow', 'capexToRevenue', 
				   'capexToDepreciation', 'stockBasedCompensationToRevenue', 'grahamNumber', 'roic', 'returnOnTangibleAssets', 
				   'grahamNetNet', 'workingCapital', 'tangibleAssetValue', 'netCurrentAssetValue', 'investedCapital', 'averageReceivables', 
				   'averagePayables', 'averageInventory', 'daysSalesOutstanding', 'daysPayablesOutstanding', 'daysOfInventoryOnHand', 
				   'receivablesTurnover', 'payablesTurnover', 'inventoryTurnover', 'roe', 'capexPerShare']
# 1. TTM figures can also be used to calculate financial ratios. The price/earnings ratio is often referred to as 
#    P/E (TTM) and is calculated as the stock's current price, divided by a company's trailing 12-month earnings per share (EPS).

def get_company_stat(stock):
	BS = requests.get('https://financialmodelingprep.com/api/v3/enterprise-values/%s?apikey=%s' % (stock, api_key))
	BS = BS.json()
	print("BS 2 = ", BS)

	if 'Error Message' in BS:
		print("ERROR: %s" % BS['Error Message'])
		sys.exit()

	if not BS or BS[0]['marketCapitalization'] is None:
		return None
	else:
		return BS[0]


def get_ratios(stock):
	BS = requests.get('https://financialmodelingprep.com/api/v3/ratios-ttm/%s?apikey=%s' % (stock, api_key))
	BS = BS.json()
	print("BS 1 = ", BS)

	if 'Error Message' in BS:
		print("ERROR: %s" % BS['Error Message'])
		sys.exit()

	if 'status' in BS:
		if BS['status'] == 404:
			print("ERROR: 404")
			return None
		elif BS['status'] == 500:
			print("ERROR: 500")
			return None

	if not BS or BS[0]['peRatioTTM'] is None:
		return None
	else:
		return BS[0]


def get_key_metrics(stock):
	BS = requests.get('https://financialmodelingprep.com/api/v3/key-metrics/%s?apikey=%s' % (stock, api_key))
	BS = BS.json()
	print("BS 0 = ", BS)

	if 'Error Message' in BS:
		print("ERROR: %s" % BS['Error Message'])
		sys.exit()

	if 'status' in BS:
		if BS['status'] == 404:
			print("ERROR: 404")
			return None
		elif BS['status'] == 500:
			print("ERROR: 500")
			return None

	if not BS or BS[0]['bookValuePerShare'] is None:
		return None
	else:
		return BS[0]


def main():
	# Get list of ticker symbols from trading212
	tags = get_tags()
	print("num of tags: %d" % len(tags))

	filename = 'existing_tags.txt'
	file_handle = 'w'
	# Check whether file exists... in which case we might attach
	if os.path.isfile(filename):
		filesize = os.path.getsize(filename)
		if filesize != 0:
			with open(filename, 'r') as f:
				for line in f:
					if line[0] != ' ':
						dummy = line.split()
			file_handle = 'a'

	with open(filename, file_handle) as f: 
		# Do we need to write a header?
		start = -1
		if file_handle == 'a':
			print("dummy = ", dummy)
			if dummy and dummy[0] != '#':
				start = int(dummy[-1])
		else:
			# write header
			f.write("# ticker ")
			for header in enterprise_values:
				f.write("%s " % header)
			for header in key_metrics_values:
				f.write("%s " % header)
			f.write("tag_id\n")
		print("start = ", start)

		# write values
		for ii, tag in enumerate(tags):
			print("tag = ", tag)
			if ii > start and tag[0] not in ['2', '3', '4', '5', '6', '8']:
				key_metrics = get_key_metrics(tag)
				if key_metrics is None:
					print("Can't find key metrics for %s" % tag)
				else:
					company_stat = get_company_stat(tag)
					if company_stat is not None:
						f.write('%s ' % tag)
						for header in enterprise_values:
							if header == 'date':
								f.write('%s ' % key_metrics[header])
							else:
								f.write('%f ' % company_stat[header])
						for header in key_metrics_values:
							if key_metrics[header] is None:
								f.write('None ')
							elif header == 'date':
								f.write('%s ' % key_metrics[header])
							else:
								f.write('%f ' % key_metrics[header])
						f.write('%d\n' % ii)


if __name__ == "__main__":
    main()
