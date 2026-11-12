import re
import unittest
from pathlib import Path
from conveyancing_skill.engine import ROOT

class SetupPackTests(unittest.TestCase):
    def test_all_repo_paths_named_in_setup_guide_exist(self):
        guide=(ROOT/'docs/CONVEYANCING_SETUP.md').read_text(encoding='utf8')
        paths=re.findall(r'`((?:templates|knowledge)/[^`]+)`',guide)
        self.assertGreaterEqual(len(paths),15)
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT/path).is_file(),path)
