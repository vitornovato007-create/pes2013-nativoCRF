import struct
import tempfile
import unittest
from pathlib import Path

from pes_asset_inspector import AuditError, inspect_afs, inspect_sfd


class AssetInspectorTests(unittest.TestCase):
    def test_valid_afs_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.img"
            data = bytearray(0x804)
            data[:8] = b"AFS\\x00" + struct.pack("<I", 1)
            data[8:16] = struct.pack("<II", 0x800, 4)
            data[0x800:0x804] = b"TEST"
            path.write_bytes(data)
            result = inspect_afs(path)
            self.assertEqual(result["entry_count"], 1)
            self.assertEqual(result["integrity"], "valid")

    def test_rejects_wrong_signature(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.img"
            path.write_bytes(b"NOPE" + b"\\x00" * 20)
            with self.assertRaises(AuditError):
                inspect_afs(path)

    def test_detects_out_of_bounds_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.img"
            data = bytearray(64)
            data[:8] = b"AFS\\x00" + struct.pack("<I", 1)
            data[8:16] = struct.pack("<II", 0x800, 20)
            path.write_bytes(data)
            self.assertEqual(inspect_afs(path)["integrity"], "check_required")

    def test_sfd_mpeg_pack_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.sfd"
            path.write_bytes(b"\\x00\\x00\\x01\\xba" + b"\\x00" * 64 + b"SofdecStream2")
            result = inspect_sfd(path)
            self.assertTrue(result["mpeg_program_stream_pack_header"])
            self.assertIn("SofdecStream2", result["markers_in_first_8_mib"])


if __name__ == "__main__":
    unittest.main()
