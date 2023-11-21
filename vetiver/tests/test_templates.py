import vetiver
from tempfile import TemporaryDirectory
from pathlib import Path


def test_monitoring_dashboard(snapshot):
    with TemporaryDirectory() as tempdir:
        file_path = Path(tempdir, "monitoring_dashboard.qmd")
        vetiver.monitoring_dashboard(path=file_path)
        snapshot.snapshot_dir = "./vetiver/tests/snapshots"
        contents = open(file_path).read()
        snapshot.assert_match(contents, "monitoring_dashboard.qmd")
