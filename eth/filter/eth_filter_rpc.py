import unittest
from utils import Utils
from common import eth as eth_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestEthNamespaceFilterRPC(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "eth"
    waiting_count = 2

    def test_eth_newFilter_error_no_param(self):
        method = f"{self.ns}_newFilter"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_eth_newFilter_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        params = [{"fromBlock": "1234"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_eth_newFilter_error_unsupported_block_tag_param(self):
        method = f"{self.ns}_newFilter"
        params = [{"fromBlock": "pending"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)
        params = [{"toBlock": "pending"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_eth_newFilter_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_newBlockFilter_success_wrong_value_param(self):
        method = f"{self.ns}_newBlockFilter"
        params = ["abcd"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_newBlockFilter_success(self):
        method = f"{self.ns}_newBlockFilter"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_newPendingTransactionFilter_success_wrong_value_param(self):
        method = f"{self.ns}_newPendingTransactionFilter"
        params = ["abcd"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_newPendingTransactionFilter_success(self):
        method = f"{self.ns}_newPendingTransactionFilter"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_uninstallFilter_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_uninstallFilter_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [1234]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_uninstallFilter_success_false(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [filterId + "1"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_uninstallFilter_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterChanges_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterChanges_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [1234]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterChanges_error_wrong_value_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [filterId + "1"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "FilterNotFound", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterChanges_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterLogs_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterLogs_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [1234]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterLogs_error_wrong_value_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [filterId + "1"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "FilterNotFound", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getFilterLogs_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [filterId]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getLogs_error_no_param(self):
        method = f"{self.ns}_getLogs"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_eth_getLogs_error_wrong_type_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "fromBlock"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_eth_getLogs_error_unsupported_block_tag_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "pending"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)
        params = [{"toBLock": "pending"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_eth_getLogs_success_wrong_value_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "0xffffffff"}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_getLogs_success(self):
        method = f"{self.ns}_getLogs"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_eth_subscribe_success(self):
        method = f"{self.ns}_subscribe"
        fromBlock = "latest"
        params = ["newHeads"]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        subId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_unsubscribe"
        params = [subId]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newFilter_error_no_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newFilter_error_wrong_type_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newFilter_error_unsupported_block_tag_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newFilter_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newBlockFilter_success_wrong_value_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newBlockFilter_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newPendingTransactionFilter_success_wrong_value_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_newPendingTransactionFilter_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_uninstallFilter_error_no_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_uninstallFilter_error_wrong_type_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_uninstallFilter_success_false"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_uninstallFilter_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterChanges_error_no_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterChanges_error_wrong_type_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterChanges_error_wrong_value_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterChanges_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterLogs_error_no_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterLogs_error_wrong_type_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterLogs_error_wrong_value_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getFilterLogs_success"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getLogs_error_no_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getLogs_error_wrong_type_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getLogs_error_unsupported_block_tag_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getLogs_success_wrong_value_param"))
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_getLogs_success"))
        """
        suite.addTest(TestEthNamespaceFilterRPC("test_eth_subscribe_success"))
        """
        return suite
