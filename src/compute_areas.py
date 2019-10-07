import glob
import optparse
import os

import sys

import repair_mesh
import VrmlCleaner


class ComputeAreasParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)

        self.add_option("-a", "--areas", dest="areas_file",
                        help="The output areas file in csv", metavar="FILE")
        self.add_option("-v", "--input-vrml", dest="input_vrml",
                        help="The mesh to meassure in vrml file format", metavar="FILE")
        self.add_option("-e", "--export-path", dest="export_path", help="path to save original and repaired meshes",
                        metavar="FILE")
        self.add_option("-w", "--auto-vrml-dir", dest="vrmls_dir",
                        help="A directory with a bunch of vrmls", metavar="FILE")
        self.add_option("-i", "--input-imx", dest="input_imx",
                        help="The mesh to meassure in imx file format", metavar="FILE")
        self.add_option("-j", "--auto-imx-dir", dest="imxs_dir",
                        help="A directory with a bunch of imxs", metavar="FILE")
        self.add_option("-o", "--output-dir", dest="output_dir",
                        help="The output dir ussed when provides a dir as input", metavar="FILE")
        self.add_option("-s", "--save", dest="save", help="save the reapired VRML", metavar="BOOLEAN")

        self.add_option("-p", "--precision", dest="precision", help="Set the precision for repair method",
                        metavar="INT")

        self.add_option("-r", "--reduction", dest="reduction", help="Set the reduction for export meshes",
                        metavar="DOUBLE")

        self.add_option("-f", "--fragments", dest="segments", help="repair segments", metavar="BOOLEAN")

        self.add_option("-k", "--kernel-size", dest="kernelSize", help="Set kernel Size", metavar="INT")

        self.add_option("-c", "--cleanVrml", dest="cleanVrml", help="Set vrml cleaner", metavar="BOOLEAN")


PRECISION = 50


def isVRML1(inFile):
    input = open(inFile, "r")
    line = input.readline()
    return "V1.0" in line


def main(args=None):
    args = sys.argv[1:] if args is None else args
    options, _args = ComputeAreasParser().parse_args(args)
    save = options.save
    precision = int(options.precision)
    reduction = 100 - float(options.reduction)  # The parameter of method set the tarjet reduction
    segments = options.segments
    kernelSize = int(options.kernelSize)
    cleanVrml = options.cleanVrml == "True"

    if options.vrmls_dir:
        vrmls = glob.glob(os.path.join(options.vrmls_dir, "*.vrml"))
        for file in vrmls:
            name = os.path.basename(file).replace('.vrml', '')
            ext = os.path.splitext(file)[1]
            dir = os.path.splitext(file)[0]
            out_filename = os.path.join(options.output_dir, name + ".csv")
            print('*** ', name)
            if ext == ".imx":
                repair_mesh.main(file, out_filename, precision, True, options.export_path, save, reduction, kernelSize)
            elif ext == ".vrml":
                vrmlFile = file
                if cleanVrml:
                    vrmlCleaned = dir + "Cleaned.vrml"
                    VrmlCleaner.clean(file, vrmlCleaned, segments)
                    vrmlFile = vrmlCleaned
                repair_mesh.main(vrmlFile, out_filename, precision, False, options.export_path, save, reduction, kernelSize)
                if cleanVrml:
                    os.remove(vrmlCleaned)
    elif options.input_vrml:
        print('*** ', options.input_vrml)
        file = options.input_vrml
        ext = os.path.splitext(file)[1]
        dir = os.path.splitext(file)[0]
        if ext == ".imx":
            repair_mesh.main(file, options.areas_file, precision, True, options.export_path, save, reduction, kernelSize)
        elif ext == ".vrml":
            if cleanVrml:
                vrmlCleaned = dir + "Cleaned.vrml"
                VrmlCleaner.clean(file, vrmlCleaned, segments)
                file = vrmlCleaned

            repair_mesh.main(file, options.areas_file, precision, False, options.export_path, save, reduction, kernelSize)
            if cleanVrml:
                os.remove(file)

    print("")
    print("---------------EXECUTION FINISHED---------------")


if __name__ == '__main__':
    main()
