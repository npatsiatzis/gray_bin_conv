# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08
SIM_ARGS += --wave=wave.ghw

VHDL_SOURCES += $(PWD)/../rtl/gray_to_bin.vhd
# use VHDL_SOURCES for VHDL files


gray_2_bin:
		rm -rf sim_build
		$(MAKE) sim MODULE=tb TOPLEVEL=gray_to_bin

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim