#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import optparse
import glob
import sys
import os
import re
from multiprocessing import Process
import parse_imx

class ComputeAreasParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)

        self.add_option("-a", "--areas", dest="areas_file",
                        help="The output areas file in csv", metavar="FILE")
        self.add_option("-v", "--input-vrml", dest="input_vrml",
                        help="The mesh to meassure in vrml file format", metavar="FILE")
        self.add_option("-w", "--auto-vrml-dir", dest="vrmls_dir",
                        help="A directory with a bunch of vrmls", metavar="FILE")
        self.add_option("-i", "--input-imx", dest="input_imx",
                        help="The mesh to meassure in imx file format", metavar="FILE")
        self.add_option("-j", "--auto-imx-dir", dest="imxs_dir",
                        help="A directory with a bunch of imxs", metavar="FILE")
        self.add_option("-o", "--output-dir", dest="output_dir",
                        help="The output dir ussed when provides a dir as input", metavar="FILE")


def compute_area(actor):
    polydata = actor.GetMapper().GetInput()
    number_of_cells = polydata.GetNumberOfCells()
    area = 0
    for i in range(number_of_cells):
        area += vtk.vtkMeshQuality.TriangleArea(polydata.GetCell(i))

    return area


def show_actor(actor, ren, rw):
    ren.RemoveAllViewProps()
    ren.AddActor(actor)
    ren.ResetCamera()
    rw.Render()


def compute_all_areas(actors_list):
    areas = []
    for actor, i in zip(actors_list, range(len(actors_list))):
        sys.stdout.write("%d " % i)
        area = compute_area(actor)
        areas.append((i, area))
        sys.stdout.flush()
    print "\n"
    return areas


def compute_centroids(actors_list):
    return [a.GetCenter() for a in actors_list]


def compute_names(names_list):
    return [[a] for a in names_list]

def csv_areas_vrml(actors_list, filename):
    centroids = compute_centroids(actors_list)  # Centroids of original actors
    areas = compute_all_areas(actors_list)

    csv = "Object,Area,X,Y,Z\n"
    for i in range(len(areas)):
        data = []
        data.extend(areas[i])
        data.extend(centroids[i])
        csv += "%d,%f,%f,%f,%f\n" % tuple(data)

    with open(filename, 'w') as f:
        f.write(csv)

def csv_areas_imx(actors_list, names_list, filename):
    centroids = compute_centroids(actors_list)  # Centroids of original actors
    areas = compute_all_areas(actors_list)
    names = compute_names(names_list)

    csv = "Object,Area,X,Y,Z,Name\n"
    for i in range(len(areas)):
        data = []
        data.extend(areas[i])
        data.extend(centroids[i])
        data.extend(names[i])
        csv += "%d,%f,%f,%f,%f,%s\n" % tuple(data)

    with open(filename, 'w') as f:
        f.write(csv)


def run(input_filename, areas_filename, is_vrml):

    rw = vtk.vtkRenderWindow()
    rw.OffScreenRenderingOn()

    if is_vrml:
        vrml_filename = input_filename
    else:
        vrml_filename = re.sub('.imx', '.vrml', input_filename)
        args = ["{}".format(input_filename), "{}".format(vrml_filename)]
        p = Process(target=parse_imx.main, args=[args])
        p.start()
        p.join()

        names_list = []
        names_pattern = '([\s]*DEF\sn)([\w]*)([\s]*Shape[\s]*{[\s]*)$'
        with open(vrml_filename) as f:
            for line in f:
                if re.search(names_pattern, line):
                    line = re.sub(names_pattern, r'\2', line)
                    names_list.append(line)

    importer = vtk.vtkVRMLImporter()
    importer.SetFileName(vrml_filename)
    importer.Read()
    importer.SetRenderWindow(rw)
    importer.Update()

    rw.Render()

    ren = importer.GetRenderer()
    actors = ren.GetActors()
    actors.InitTraversal()
    actors_list = [actors.GetNextActor() for x in range(ren.GetNumberOfPropsRendered())]

    if is_vrml:
        csv_areas_vrml(actors_list, areas_filename)
    else:
        csv_areas_imx(actors_list, names_list, areas_filename)

    rw.Finalize()

    if not is_vrml:
        os.remove(vrml_filename)


def main(args=None):
    args = sys.argv[1:] if args is None else args
    options, _args = ComputeAreasParser().parse_args(args)

    if options.vrmls_dir:
        vrmls = glob.glob(os.path.join(options.vrmls_dir, "*.vrml"))
        for vrml in vrmls:
            name = os.path.basename(vrml).replace('.vrml','')
            out_filename = os.path.join(options.output_dir, name + ".csv")
            print '*** ', name
            run(vrml, out_filename, True)
    elif options.input_vrml:
        print '*** ', options.input_vrml
        run(options.input_vrml, options.areas_file, True)
    elif options.imxs_dir:
        imxs = glob.glob(os.path.join(options.imxs_dir, "*.imx"))
        for imx in imxs:
            name = os.path.basename(imx).replace('.imx','')
            out_filename = os.path.join(options.output_dir, name + ".csv")
            print '*** ', name
            run(imx, out_filename, False)
    elif options.input_imx:
        print '*** ', options.input_imx
        run(options.input_imx, options.areas_file, False)

if __name__ == '__main__':
    main()
