from Generator import Generator
import sys, os, argparse


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def main(argv):
    parser = argparse.ArgumentParser(description='Generate Data Sets for Object detection!')
    parser.add_argument('-p', help="Pfad zum Ordner des Datasets.", action=FullPaths, type=is_dir, metavar='PATH')

    parser.add_argument('-c', help="Bestimmte Klassen setzen.", metavar='classes', type=int, nargs='*')
    parser.add_argument('--zip', dest='zip', action='store_true')
    parser.add_argument('--stat_csv', dest='csv', action='store_true')
    parser.add_argument('--stat_img', dest='img', action='store_true')
    parser.add_argument('--del_img', dest='delete', action='store_true')
    parser.add_argument('--train_csv', dest='train', action='store_true')

    args = parser.parse_args(argv)

    if args.c:
        generator = Generator(args.p, args.c)
    else:
        generator = Generator(args.p)

    if args.delete:
        generator.deleteEmptyImages()

    if args.zip:
        generator.createDataSetZIP()

    if args.csv:
        generator.createCSVOverview()

    if args.img:
        generator.createPieChart()

    if args.train:
        generator.createCSVLabelMap()

if __name__ == '__main__':
    main(sys.argv[1:])