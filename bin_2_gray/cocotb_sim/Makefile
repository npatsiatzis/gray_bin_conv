# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/../rtl/bin_to_gray.vhd
# use VHDL_SOURCES for VHDL files

bin_2_gray:
		rm -rf sim_build
		$(MAKE) sim MODULE=testbench_bin_to_gray TOPLEVEL=bin_to_gray

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim