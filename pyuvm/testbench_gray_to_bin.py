from cocotb.triggers import Timer
from pyuvm import *
import random
import cocotb
import pyuvm
from utils import Gray2BinBfm


g_width = int(cocotb.top.g_width)
covered_values = []


def bin_to_gray(n):
    return (n ^ (n >> 1))


# Sequence classes
class SeqItem(uvm_sequence_item):

    def __init__(self, name, gray):
        super().__init__(name)
        self.gray = gray

    def randomize_operands(self):
        self.gray = random.randint(0,2**g_width-1)

    def randomize(self):
        self.randomize_operands()

    def __eq__(self, other):
        same = self.gray == other.gray
        return same

class RandomSeq(uvm_sequence):
    async def body(self):
        while(len(covered_values) != 2**g_width):
            data_tr = SeqItem("data_tr", None)
            await self.start_item(data_tr)
            data_tr.randomize_operands()
            while(data_tr.gray in covered_values):
                data_tr.randomize_operands()
            covered_values.append(data_tr.gray)
            await self.finish_item(data_tr)


class TestAllSeq(uvm_sequence):

    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq("random")
        await random.start(seqr)

class Driver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def start_of_simulation_phase(self):
        self.bfm = Gray2BinBfm()

    async def launch_tb(self):
        await self.bfm.reset()
        self.bfm.start_bfm()

    async def run_phase(self):
        await self.launch_tb()
        while True:
            data = await self.seq_item_port.get_next_item()
            await self.bfm.send_data(data.gray)
            result = await self.bfm.get_result()
            self.ap.write(result)
            data.result = result
            self.seq_item_port.item_done()


class Coverage(uvm_subscriber):

    def end_of_elaboration_phase(self):
        self.cvg = set()

    def write(self, data):
        gray = data
        if(int(gray) not in self.cvg):
            self.cvg.add(int(gray))

    def report_phase(self):
        try:
            disable_errors = ConfigDB().get(
                self, "", "DISABLE_COVERAGE_ERRORS")
        except UVMConfigItemNotFound:
            disable_errors = False
        if not disable_errors:
            if len(set(covered_values) - self.cvg) > 0:
                self.logger.error(
                    f"Functional coverage error. Missed: {set(covered_values)-self.cvg}")   
                assert False
            else:
                self.logger.info("Covered all input space")
                assert True


class Scoreboard(uvm_component):

    def build_phase(self):
        self.data_fifo = uvm_tlm_analysis_fifo("data_fifo", self)
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.data_get_port = uvm_get_port("data_get_port", self)
        self.result_get_port = uvm_get_port("result_get_port", self)
        self.data_export = self.data_fifo.analysis_export
        self.result_export = self.result_fifo.analysis_export

    def connect_phase(self):
        self.data_get_port.connect(self.data_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)

    def check_phase(self):
        passed = True
        try:
            self.errors = ConfigDB().get(self, "", "CREATE_ERRORS")
        except UVMConfigItemNotFound:
            self.errors = False
        while self.result_get_port.can_get():
            _, actual_result = self.result_get_port.try_get()
            data_success, data = self.data_get_port.try_get()
            if not data_success:
                self.logger.critical(f"result {actual_result} had no command")
            else:
                gray = data
                if(gray == bin_to_gray(int(actual_result))):
                    pass
                    self.logger.info("PASSED")
                else:
                    self.logger.error("FAILED")

                    passed = False
        assert passed


class Monitor(uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.bfm = Gray2BinBfm()
        self.get_method = getattr(self.bfm, self.method_name)

    async def run_phase(self):
        while True:
            datum = await self.get_method()
            self.logger.debug(f"MONITORED {datum}")
            self.ap.write(datum)


class AluEnv(uvm_env):

    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = Driver.create("driver", self)
        self.data_mon = Monitor("data_mon", self, "get_data")
        self.coverage = Coverage("coverage", self)
        self.scoreboard = Scoreboard("scoreboard", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.data_mon.ap.connect(self.scoreboard.data_export)
        self.data_mon.ap.connect(self.coverage.analysis_export)
        self.driver.ap.connect(self.scoreboard.result_export)


@pyuvm.test()
class AluTest(uvm_test):
    """Test Gray 2 Bin with random values"""

    def build_phase(self):
        self.env = AluEnv("env", self)

    def end_of_elaboration_phase(self):
        self.test_all = TestAllSeq.create("test_all")

    async def run_phase(self):
        self.raise_objection()
        await self.test_all.start()
        await Timer(2,units = 'ns') # to do last transaction
        self.drop_objection()