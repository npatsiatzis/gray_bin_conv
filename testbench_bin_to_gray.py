import cocotb
from cocotb.triggers import Timer
import random
from cocotb_coverage.coverage import CoverPoint,coverage_db

g_width = int(cocotb.top.g_width)

covered_value = []
full = False

def gray_to_dec(n):
	inv = 0;
	# Taking xor until
	# n becomes zero
	while(n):
		inv = inv ^ n;
		n = n >> 1;
	return inv


# #Callback functions to capture the bin content showing
def notify_full():
	global full
	full = True


# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.bin",xf = lambda x : x.i_bin.value, bins = list(range(2**g_width)), at_least=1)
def number_cover(x):
	covered_value.append(x.i_bin.value)

async def init(dut,time_units=1):

	dut.i_bin.value = 0 

	await Timer(time_units,units = 'ns')
	dut._log.info("the core was initialized")

@cocotb.test()
async def test(dut):

	await init(dut,5)	
	while (full != True):
		bin_input = random.randint(0,2**g_width-1)
		while(bin_input in covered_value):
			bin_input = random.randint(0,2**g_width-1)


		dut.i_bin.value = bin_input
		await Timer(2,units = 'ns')
		number_cover(dut)
		coverage_db["top.bin"].add_threshold_callback(notify_full, 100)
		assert not (bin_input != gray_to_dec(dut.o_gray.value)),"Actual behavior different than the expected one"


	coverage_db.report_coverage(cocotb.log.info,bins=True)
	coverage_db.export_to_xml(filename="coverage_bin_gray.xml") 


