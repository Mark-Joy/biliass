import argparse
import logging
import sys

from biliass import Danmaku2ASS


def main():
    logging.basicConfig(format="%(levelname)s: %(message)s")
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", metavar="OUTPUT", help="Output file")
    parser.add_argument("-s", "--size", metavar="WIDTHxHEIGHT", required=True, help="Stage size in pixels")
    parser.add_argument(
        "-fn",
        "--font",
        metavar="FONT",
        help="Specify font face [default: %s]" % "sans-serif",
        default="sans-serif",
    )
    parser.add_argument(
        "-fs",
        "--fontsize",
        metavar="SIZE",
        help=("Default font size [default: %s]" % 25),
        type=float,
        default=25.0,
    )
    parser.add_argument("-a", "--alpha", metavar="ALPHA", help="Text opacity", type=float, default=1.0)
    parser.add_argument(
        "-dm",
        "--duration-marquee",
        metavar="SECONDS",
        help="Duration of scrolling comment display [default: %s]" % 5,
        type=float,
        default=5.0,
    )
    parser.add_argument(
        "-ds",
        "--duration-still",
        metavar="SECONDS",
        help="Duration of still comment display [default: %s]" % 5,
        type=float,
        default=5.0,
    )
    parser.add_argument("-fl", "--filter", help="Regular expression to filter comments")
    parser.add_argument(
        "-flf", "--filter-file", help="Regular expressions from file (one line one regex) to filter comments"
    )
    parser.add_argument(
        "-p", "--protect", metavar="HEIGHT", help="Reserve blank on the bottom of the stage", type=int, default=0
    )
    parser.add_argument("-r", "--reduce", action="store_true", help="Reduce the amount of comments if stage is full")
    parser.add_argument("-f", "--format", choices=["xml", "protobuf"], default="xml", help="输入文件的格式（XML 或 protobuf）")
    parser.add_argument("file", metavar="FILE", help="Comment file to be processed")
    args = parser.parse_args()
    try:
        width, height = str(args.size).split("x", 1)
        width = int(width)
        height = int(height)
    except ValueError:
        raise ValueError("Invalid stage size: %r" % args.size)

    try:
        with open(args.file, "r" if args.format == "xml" else "rb") as f:
            input = f.read()
    except UnicodeDecodeError:
        logging.error("无法解码该文件，推测其为 protobuf 文件，请添加 `-f protobuf` 参数")
        sys.exit(1)

    if args.output:
        fo = open(args.output, "w", encoding="utf-8-sig", errors="replace", newline="\r\n")
    else:
        fo = sys.stdout
    output = Danmaku2ASS(
        input,
        width,
        height,
        args.format,
        args.protect,
        args.font,
        args.fontsize,
        args.alpha,
        args.duration_marquee,
        args.duration_still,
        args.filter,
        args.reduce,
    )
    fo.write(output)
    fo.close()


if __name__ == "__main__":
    main()
