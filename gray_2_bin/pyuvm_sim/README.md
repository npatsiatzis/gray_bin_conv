![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/regression_pyuvm_gray_2_bin.yml/badge.svg)
![example workflow](https://github.com/npatsiatzis/gray_bin_conv/actions/workflows/coverage_pyuvm_gray_2_bin.yml/badge.svg)

### RTL implementation for gray to binary and vice versa code conversion

- run pyuvm testbench
    - $ make
- run unit testing of the pyuvm testbench
    - $  SIM=ghdl pytest -n auto -o log_cli=True --junitxml=test-results.xml --cocotbxml=test-cocotb.xml


