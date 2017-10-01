#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import optparse
import glob
import sys
import os


class ComputeAreasParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)

        self.add_option("-a", "--areas", dest="areas_file",
                        help="The output areas file in csv", metavar="FILE")
        self.add_option("-i", "--input-vrml", dest="input_vrml",
                        help="The mesh to meassure in vrml file format", metavar="FILE")
        self.add_option("-d", "--auto-dir", dest="vrmls_dir",
                        help="A directory with a bunch of vrmls", metavar="FILE")
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


def csv_areas(actors_list, filename):
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


def run(input_filename, areas_filename):

    rw = vtk.vtkRenderWindow()
    rw.OffScreenRenderingOn()

    importer = vtk.vtkVRMLImporter()
    importer.SetFileName(input_filename)
    importer.Read()
    importer.SetRenderWindow(rw)
    importer.Update()

    rw.Render()

    ren = importer.GetRenderer()
    actors = ren.GetActors()
    actors.InitTraversal()
    actors_list = [actors.GetNextActor() for x in range(ren.GetNumberOfPropsRendered())]

    csv_areas(actors_list, areas_filename)
    rw.Finalize()


def main(args=None):
    args = sys.argv[1:] if args is None else args
    options, _args = ComputeAreasParser().parse_args(args)

    if options.vrmls_dir:
        vrmls = glob.glob(os.path.join(options.vrmls_dir, "*.vrml"))
        for vrml in vrmls:
            name = os.path.basename(vrml).replace('.vrml','')
            out_filename = os.path.join(options.output_dir, name + ".csv")

            print '*** ', name
            run(vrml, out_filename)
    else:
        run(options.input_vrml, options.areas_file)


if __name__ == '__main__':
    main()
