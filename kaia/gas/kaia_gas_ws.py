import unittest
from utils import Utils
from common import kaia as kaia_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceGasWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "kaia"
    waiting_count = 2

    def test_kaia_maxPriorityFeePerGas_success(self):
        method = f"{self.ns}_maxPriorityFeePerGas"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_feeHistory_success(self):
        method = f"{self.ns}_feeHistory"
        blockCount = 3
        lastBlock = "latest"
        rewardPercentiles = [20, 30, 50]
        params = [blockCount, lastBlock, rewardPercentiles]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        length = len(result["reward"])
        self.assertLessEqual(length, blockCount)
        self.assertEqual(length, len(result["gasUsedRatio"]))
        self.assertEqual(length + 1, len(result["baseFeePerGas"]))

        lastBlock = "pending"
        params = [blockCount, lastBlock, rewardPercentiles]
        result2, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        length = len(result2["reward"])
        self.assertLessEqual(length, blockCount)
        self.assertEqual(length, len(result2["gasUsedRatio"]))
        self.assertEqual(length + 1, len(result2["baseFeePerGas"]))

        # NOTE: Making the difference between latest and pending Receipts is hard, so we check the gap between the two oldest block
        # on CN, the both oldest block gap is expected to be 1
        # (on EN, the oldest block is expected to be the same)
        # But there is a timing issue on CN if the block is finalized between the two testing API calls, so we allow 2
        self.assertLessEqual(int(result2.get("oldestBlock"), 16) - int(result.get("oldestBlock"), 16), 2)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()

        suite.addTest(TestKaiaNamespaceGasWS("test_kaia_maxPriorityFeePerGas_success"))
        suite.addTest(TestKaiaNamespaceGasWS("test_kaia_feeHistory_success"))

        return suite
