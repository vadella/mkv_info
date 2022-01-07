import datetime
import xml.etree.ElementTree as ET
from pathlib import Path

import mkv_info.library_xml as library_xml

DATA_DIR = Path("data")


def test_library() -> None:
    data_file = DATA_DIR / "videodb_min.xml"
    tree = ET.parse(data_file)
    root = tree.getroot()
    library = library_xml.VideoDatabase.from_data(root)
    assert len(library.movies) == 4
    assert library.movies[0] == library_xml.Movie(
        title="2001: A Space Odyssey",
        duration=datetime.timedelta(minutes=149),
        year=1968,
        streams=library_xml.StreamDetails(
            videos=(
                library_xml.VideoStream(codec="h264", width=1920, height=864,),
            ),
            audios=(
                library_xml.AudioStream(
                    codec="ac-3", language="eng", channels=6,
                ),
            ),
            subs=(
                library_xml.SubStream(language="eng",),
                library_xml.SubStream(language="dut",),
            ),
        ),
    )
