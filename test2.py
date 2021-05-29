
import sys, os
import requests
from harvest_trading212 import get_tags
from scrape_pb import get_pb, get_pe
import datetime
import time

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

	filename = 'existing_tags_pe.txt'
	with open(filename, 'w') as f: 
		f.write('# tag pevalue tag_id\n')
		for ii, tag in enumerate(tags):
			if tag[0] not in ['2', '3', '4', '5', '6', '8']:
				value = get_pe(tag)
				if value:
					print("found %f of %s\n" % (value, tag))
					f.write("%s %f %d\n" % (tag, value, ii))

	return


if __name__ == "__main__":
    main()
