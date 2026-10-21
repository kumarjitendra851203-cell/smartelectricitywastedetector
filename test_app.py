import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest = None

@unittest.skipIf(AppTest is None, "streamlit not installed")
class AppTests(unittest.TestCase):
    def test_app_runs_without_errors(self):
        at = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=60).run()
        self.assertEqual(len(at.exception), 0, [e.value for e in at.exception])
        self.assertEqual(len(at.tabs), 4)
        [r for r in at.radio if r.label == "Model"][0].set_value("Tiered slabs").run()
        self.assertEqual(len(at.exception), 0)

if __name__ == "__main__":
    unittest.main()
