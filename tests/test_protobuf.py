from biliass import ReadCommentsBilibiliProtobuf


def test_xml_v1():
    with open("./tests/test_files/test.protobuf", "rb") as f:
        ReadCommentsBilibiliProtobuf(f.read(), 10)