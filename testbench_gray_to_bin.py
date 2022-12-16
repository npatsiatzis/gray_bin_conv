import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ClockCycles,ReadOnly
from cocotb.result import TestFailure
import random
from cocotb_coverage.coverage import CoverCross,CoverPoint,coverage_db
from cocotb.binary import BinaryValue
import numpy as np

g_width = int(cocotb.top.g_width)

covered_value = []
full = False

def bin_to_gray(n):
	return (n ^ (n >> 1))


# #Callback functions to capture the bin content showing
def notify_full():
	global full
	full = True


# at_least = value is superfluous, just shows how you can determine the amount of times that
# a bin must be hit to considered covered
@CoverPoint("top.gray",xf = lambda x : x, bins = list(range(2**g_width)), at_least=1)
def number_cover(x):
	covered_value.append(x)

async def init(dut,time_units=1):

	dut.i_gray.value = 0 

	await Timer(time_units,units = 'ns')
	dut._log.info("the core was initialized")

@cocotb.test()
async def test(dut):

	await init(dut,5)	
	while (full != True):
		bin_input = random.randint(0,2**g_width-1)
		while(bin_input in covered_value):
			bin_input = random.randint(0,2**g_width-1)

		gray_input = bin_to_gray(bin_input)
		number_cover(bin_input)
		coverage_db["top.gray"].add_threshold_callback(notify_full, 100)
		dut.i_gray.value = gray_input
		await Timer(2,units = 'ns')
		assert not (bin_input != int(dut.o_bin.value)),"Actual behavior different than the expected one"


