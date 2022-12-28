![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/regression.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/coverage.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/regression_pyuvm.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/coverage_pyuvm.yml/badge.svg)

### RTL implementation for gray to binary and vice versa code conversion


- CoCoTB testbench for functional verification
	- $ make
- CoCoTB-test unit testing to exercise the CoCoTB tests across a range of values for the generic parameters
    - $  SIM=ghdl pytest -n auto -o log_cli=True --junitxml=test-results.xml --cocotbxml=test-cocotb.xml


