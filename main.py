from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import pandas as pd
import time
from selenium.webdriver.common.by import By
import importlib
import main
import secret_stuff

path = secret_stuff.path_to_chromedriver

login = secret_stuff.login
pwd = secret_stuff.pwd

sec_trades = pd.read_csv('trades_sec.csv')
sec_trades['sell_date'] = sec_trades['sell_date'].astype(str)
sec_trades['buy_date'] = sec_trades['buy_date'].astype(str)

cryp_trades = pd.read_csv('trades_cryp.csv')
cryp_trades['sell_date'] = cryp_trades['sell_date'].astype(str)
cryp_trades['buy_date'] = cryp_trades['buy_date'].astype(str)

payers_name = 'NATIONAL FINANCIAL SERVICES LLC'
payers_name_cryp = ''
address = '499 WASHINGTON BLVD'
address_cryp = ''
city = 'JERSEY CITY'
city_cryp = ''
state = 'NJ'
state_cryp = ''
zip = '07310'
zip_cryp = ''
payers_tin = '04-3523567'
payers_tin_cryp = ''
state_tax_widthheld = '0'
fed_tax_widthheld = '0'

# payers_name_el = address_el = city_el = state_el = zip_el = payers_tin_el = state_select_el = state_tax_widthheld_el = None

def openChrome():
	global driver
	#service = Service(executable_path=path)
	#driver = webdriver.Chrome(service=service)
	driver = uc.Chrome()  # This uses undetected-chromedriver
	driver.get("https://www.sprintax.com/ots/lets-talk-money-2020.html")

def setupInfo():
	global payers_name_el
	payers_name_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_employer_name"]')
	global address_el
	address_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_employer_address"]')
	global city_el
	city_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_employer_city"]')
	global state_el
	state_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_employer_state"]')
	global zip_el
	zip_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_employer_zip_code"]')
	global payers_tin_el
	payers_tin_el = driver.find_element(By.XPATH, '//*[@id="payers_federal_id"]')
	global state_select_el
	state_select_el = driver.find_element(By.XPATH, '//*[@id="statecode"]/option[6]') 
	global state_tax_widthheld_el
	state_tax_widthheld_el = driver.find_element(By.XPATH, '//*[@id="state_income_tax"]')
	global next_btn 
	next_btn = driver.find_element(By.XPATH, '//*[@id="footer"]/div[1]/div[3]/a') 
	global wash_sale_el
	wash_sale_el = driver.find_element(By.XPATH, '//*[@id="wash_sale_loss"]')
	global state_id_el
	state_id_el = driver.find_element(By.XPATH, '//*[@id="__employer_details_state_ein"]')
	

def runInfo():
	state_tax_widthheld_el.send_keys(state_tax_widthheld)
	state_select_el.click()
	payers_name_el.send_keys(payers_name)
	address_el.send_keys(address)
	city_el.send_keys(city)
	state_el.send_keys(state)
	zip_el.send_keys(zip)
	payers_tin_el.send_keys(payers_tin)

def setupTrade():
	global descp_el
	descp_el = driver.find_element(By.XPATH, '//*[@id="description"]') 
	global buy_date_el
	buy_date_el = driver.find_element(By.XPATH, '//*[@id="date_of_acquistion"]')
	global sell_date_el
	sell_date_el =  driver.find_element(By.XPATH, '//*[@id="date_of_sale"]') 
	global proceeds_el
	proceeds_el = driver.find_element(By.XPATH, '//*[@id="stocks_bonds"]') 
	global cost_el
	cost_el = driver.find_element(By.XPATH, '//*[@id="costs_other_basic"]') 
	global fed_tax_widthheld_el
	fed_tax_widthheld_el = driver.find_element(By.XPATH, '//*[@id="federal_income_tax"]') 
	global gross_rep_el
	gross_rep_el = driver.find_element(By.XPATH, '//*[@id="sim_reported_irs1"]/a') 
	global short_trm_el
	short_trm_el = driver.find_element(By.XPATH, '//*[@id="sim_gain_or_lost1"]/a') 
	global real_property_el
	real_property_el = driver.find_element(By.XPATH, '//*[@id="reported_gain_or_loss2"]')

def setupCryptoInfo():
	global crypto_add_transaction_el
	crypto_add_transaction_el = driver.find_element(By.XPATH, '//*[@id="r_1425_1_vctrans"]/div/div/a')


def coinTypeLookup(index):
	match cryp_trades.iloc[index]['asset']:
		case 'BTC':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[2]')
		case 'ETH':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[3]')
		case 'LTC':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[4]')
		case 'BCH':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[5]')
		case 'XRP':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[6]')
		case 'DOGE':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[7]')
		case 'XLM':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[8]')
		case 'ADA':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[9]')
		case 'DOT':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[10]')
		case 'SOL':
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[11]')
		case _:
			return driver.find_element(By.XPATH, f'//*[@id="__vctrans_descr_of_property_{index}"]/option[12]')


def setupCryptoTrade(index):
	global crypto_short_term_el
	crypto_short_term_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_type_of_transaction_{index}"]/option[2]')
	global crypto_long_term_el
	crypto_long_term_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_type_of_transaction_{index}"]/option[3]')
	global crypto_long_term_noncovered_el
	crypto_long_term_noncovered_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_long_tax_lots_{index}"]/option[4]')
	global crypto_short_term_noncovered_el
	crypto_short_term_noncovered_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_short_tax_lots_{index}"]/option[4]')
	global crypto_currency_el
	crypto_currency_el = coinTypeLookup(index)
	global crypto_sell_date_el
	crypto_sell_date_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_date_sold_{index}"]')
	global crypto_quantity_el
	crypto_quantity_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_quantity_{index}"]')
	global crypto_proceeds_el
	crypto_proceeds_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_proceeds_{index}"]')
	global crypto_acquisition_date_el
	crypto_acquisition_date_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_date_acquired_{index}"]')
	global crypto_cost_basis_el
	crypto_cost_basis_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_cost_{index}"]')
	global crypto_state_el
	crypto_state_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_state_{index}"]/option[6]')
	global crypto_not_eic_el
	crypto_not_eic_el = driver.find_element(By.XPATH, f'//*[@id="__vctrans_nec_income_{index}"]/option[3]')

def runCryptoTrade(index):
	if cryp_trades.iloc[index]['hold_period'] >= 365:
		crypto_long_term_el.click()
		crypto_long_term_noncovered_el.click()
	else:
		crypto_short_term_el.click()
		crypto_short_term_noncovered_el.click()
	crypto_currency_el.click()
	crypto_sell_date_el.send_keys(str(cryp_trades.iloc[index]['sell_date']))
	crypto_quantity_el.send_keys(str(cryp_trades.iloc[index]['quantity']))
	crypto_proceeds_el.send_keys(str(cryp_trades.iloc[index]['proceeds']))
	crypto_acquisition_date_el.send_keys(str(cryp_trades.iloc[index]['buy_date']))
	crypto_cost_basis_el.send_keys(str(cryp_trades.iloc[index]['cost_basis']))
	crypto_state_el.click()
	crypto_not_eic_el.click()

def executeCrypto(index):
	setupCryptoInfo()
	setupCryptoTrade(index)
	runCryptoTrade(index)

def runTrade(index):
	gross_rep_el.click()
	short_trm_el.click()
	real_property_el.click()
	fed_tax_widthheld_el.send_keys(fed_tax_widthheld)
	descp_el.send_keys(str(sec_trades.iloc[index]['descp']))
	buy_date_el.send_keys(str(sec_trades.iloc[index]['buy_date']))
	sell_date_el.send_keys(str(sec_trades.iloc[index]['sell_date']))
	proceeds_el.send_keys(str(sec_trades.iloc[index]['proceeds']))
	cost_el.send_keys(str(sec_trades.iloc[index]['cost']))
	wash_sale_el.send_keys(str(sec_trades.iloc[index]['wash']))

def execute(index,cryp=False):
	if cryp:
		executeCrypto(index)
	else:
		setupInfo()                                          
		runInfo()
	setupTrade()                                         
	runTrade(index,cryp)

def loop(start, end, cryp=False):
	while start <= end:
		execute(start,cryp)
		start+=1
		next_btn.click()
		time.sleep(5)

