#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process

import vtk
import sys
import os
import optparse
import glob

import re

import parse_imx

RADIUS = 3  # For Open and Gauss
SCALE = 50.0  # For Rasterization


class RepairMeshParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)

        self.add_option("-a", "--areas", dest="areas_file",
                        help="The output areas file in csv", metavar="FILE")
        self.add_option("-i", "--input-vrml", dest="input_vrml",
                        help="The mesh to de repaired in vrml file format", metavar="FILE")
        self.add_option("-d", "--auto-dir", dest="vrmls_dir",
                        help="A directory with a bunch of vrmls", metavar="FILE")
        self.add_option("-o", "--output-dir", dest="output_dir",
                        help="The output dir ussed when provides a dir as input", metavar="FILE")
        self.add_option("-s", "--scale-factor", dest="scale", default=50.0,
                        help="Tehe scale factor used in the rasterization")
        self.add_option("-c", "--combine", action="store_true", dest="combine",
                        help="Combine all polydatas in one object")


def write_image(image, filename):
    """Write vtk image data to file."""
    aWriter = vtk.vtkMetaImageWriter()
    aWriter.SetInput(image)
    aWriter.SetFileName(filename)
    aWriter.SetFileDimensionality(3)
    aWriter.SetCompression(False)
    aWriter.Write()


def voxelizer(polydata, scale=SCALE):
    """ volume voxelization not anti-aliased """

    # Get selection boundaries.
    (minX, maxX, minY, maxY, minZ, maxZ) = [int(x * scale) for x in
                                            polydata.GetBounds()]  # convert tuple of floats to ints

    # print "  Selection bounds are %s"%str((minX, maxX, minY, maxY, minZ, maxZ))  #dimensions of the resulting image
    # print "  Dimensions: %s"%str((maxX - minX, maxY - minY, maxZ - minZ))

    padd = RADIUS + 6
    (minX, maxX, minY, maxY, minZ, maxZ) = (
        minX - padd, maxX + padd, minY - padd, maxY + padd, minZ - padd, maxZ + padd)

    ps1 = 1.0 / float(scale)  # pixel size for the stencil, make sure it's a float division!
    ps2 = 1.0  # pixel size for the image

    ## Convert a surface mesh into an image stencil that can be used to mask an image with vtkImageStencil.
    polyToStencilFilter = vtk.vtkPolyDataToImageStencil()
    polyToStencilFilter.SetInput(polydata)
    polyToStencilFilter.SetOutputWholeExtent(minX, maxX, minY, maxY, minZ, maxZ)
    polyToStencilFilter.SetOutputSpacing(ps1, ps1, ps1)
    polyToStencilFilter.SetOutputOrigin(0.0, 0.0, 0.0)
    polyToStencilFilter.Update()

    # Create an empty (3D) image of appropriate size.
    image = vtk.vtkImageData()
    image.SetSpacing(ps2, ps2, ps2)
    image.SetOrigin(0.0, 0.0, 0.0)
    image.SetExtent(minX, maxX, minY, maxY, minZ, maxZ)
    image.SetScalarTypeToUnsignedChar()
    image.AllocateScalars()

    # Mask the empty image with the image stencil.
    # First All the background to 0
    # Needed otherwise introduces noise
    stencil = vtk.vtkImageStencil()
    stencil.SetInput(image)
    stencil.SetStencil(polyToStencilFilter.GetOutput())
    stencil.ReverseStencilOff()
    stencil.SetBackgroundValue(0)
    stencil.Update()

    # Foreground to 255
    stencil2 = vtk.vtkImageStencil()
    stencil2.SetInput(stencil.GetOutput())
    stencil2.SetStencil(polyToStencilFilter.GetOutput())
    stencil2.ReverseStencilOn()
    stencil2.SetBackgroundValue(255)

    stencil2.Update()

    return stencil2.GetOutput()


def open_image(image, radius):
    openFilter = vtk.vtkImageDilateErode3D()
    openFilter.SetDilateValue(255)
    openFilter.SetErodeValue(0)
    openFilter.SetKernelSize(radius, radius, radius)
    openFilter.SetInput(image)
    openFilter.Update()
    return openFilter.GetOutput()


def dump_voxels(actor, filename):
    poly = actor.GetMapper().GetInput()
    pre_image = voxelizer(poly)
    image = open_image(pre_image, RADIUS)
    write_image(image, filename)


def open_actor(actor, actor_index=0, scale=SCALE):
    poly = actor.GetMapper().GetInput()
    pre_image = voxelizer(poly, scale)
    opened_image = open_image(pre_image, RADIUS)

    gauss = vtk.vtkImageGaussianSmooth()
    gauss.SetDimensionality(3)
    gauss.SetStandardDeviation(RADIUS, RADIUS, RADIUS)
    gauss.SetInput(opened_image)
    gauss.Update()

    image_to_contour = gauss.GetOutput()

    contour = vtk.vtkMarchingCubes()
    contour.SetInput(image_to_contour)
    contour.SetValue(0, 127.5)
    contour.ComputeScalarsOff()
    contour.Update()

    repared_poly = contour.GetOutput()

    if repared_poly.GetNumberOfCells() == 0:
        print "ERROR: number_of_cells = 0",
        # write_image(image_to_contour, "/tmp/%d.mhd"%actor_index)
        raise ValueError("ERROR: number_of_cells = 0")

    # (minX, maxX, minY, maxY, minZ, maxZ) = [int(x) for x in repared_poly.GetBounds()] #convert tuple of floats to ints
    # print "  Repared bounds are %s"%str((minX, maxX, minY, maxY, minZ, maxZ))  #dimensions of the resulting image
    # print "  Dimensions: %s"%str((maxX - minX, maxY - minY, maxZ - minZ))

    actor.GetMapper().SetInput(repared_poly)


def compute_area(actor):
    polydata = actor.GetMapper().GetInput()
    number_of_cells = polydata.GetNumberOfCells()
    area = 0
    for i in range(number_of_cells):
        area += vtk.vtkMeshQuality.TriangleArea(polydata.GetCell(i))

    return area


def combine_actors(actors_list):
    appender = vtk.vtkAppendPolyData()
    for actor in actors_list:
        poly = actor.GetMapper().GetInput()
        appender.AddInput(poly)
    appender.Update()
    combined_poly = appender.GetOutput()
    combined_actor = vtk.vtkActor()
    combined_actor.SetMapper(vtk.vtkPolyDataMapper())
    combined_actor.GetMapper().SetInput(combined_poly)
    return combined_actor


def show_actor(actor, ren, rw):
    ren.RemoveAllViewProps()
    ren.AddActor(actor)
    ren.ResetCamera()
    rw.Render()


def compute_all_areas(actors_list, scale=SCALE):
    areas = []
    for i, actor in enumerate(actors_list):
        # scale = SCALE
        sys.stdout.write("%d " % i)
        area_pre = compute_area(actor)
        try:
            open_actor(actor, i, scale)
        except ValueError, e:
            # [KNOWN BUG] The sizes are corrected, but not the position
            scale = scale * 2
            open_actor(actor, i, scale)
        area_post = compute_area(actor) / scale ** 2

        areas.append((i, area_pre, area_post, area_post / area_pre))
        sys.stdout.flush()
    print "\n"
    return areas


def compute_centroids(actors_list):
    return [a.GetCenter() for a in actors_list]


def csv_areas(actors_list, filename, scale=SCALE, names=None):
    centroids = compute_centroids(actors_list)  # Centroids of original actors
    print(
        "-------- Repairing original mesh and Calculating areas (This process might take a long time, please wait) -----------")
    areas = compute_all_areas(actors_list, scale)
    print("-------- Saving CSV file -----------")
    if names is not None:
        csv = "Object,Pre_Area,Post_Area,Post/Pre,X,Y,Z,Name\n"
        for i in range(len(areas)):
            data = []
            data.extend(areas[i])
            data.extend(centroids[i])
            data.append(names[i])
            csv += "%d,%f,%f,%f,%f,%f,%f,%s\n" % tuple(data)
    else:
        csv = "Object,Pre_Area,Post_Area,Post/Pre,X,Y,Z\n"
        for i in range(len(areas)):
            data = []
            data.extend(areas[i])
            data.extend(centroids[i])
            csv += "%d,%f,%f,%f,%f,%f,%f\n" % tuple(data)

    with open(filename, 'w') as f:
        f.write(csv)


def underScale(actor, scale):
    transform = vtk.vtkTransform()
    relation = float(1) / float(scale)
    transform.Scale(relation, relation, relation)

    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetInput(actor.GetMapper().GetInput())
    transformFilter.SetTransform(transform)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(transformFilter.GetOutput())
    actor.SetMapper(mapper)
    return actor


def reduceMesh(actor,reduction):
    decimate = vtk.vtkDecimatePro()
    decimate.SetInput(actor.GetMapper().GetInput())
    decimate.SetTargetReduction(reduction/100)
    decimate.Update()

    decimateMapper = vtk.vtkPolyDataMapper()
    decimateMapper.SetInput(decimate.GetOutput())
    actor.SetMapper(decimateMapper)
    return actor


# Only for future versions of VTK, at the moment is a beta feature
"""def save_obj(actor_list, dir, names):
    exporter = vtk.vtkObjExporter()
    if not os.path.isdir(dir):
        os.makedirs(dir)
    if names is not None:
        for actor, name in zip(actor_list, names):
            path = "%s/%s.obj" % (dir, name)
            exporter.SetFileName(path)
            exporter.SetInput(actor.GetMapper().GetInput())
            exporter.Write()
    else:
        for i, actor in enumerate(actor_list):
            path = "%s/%d.obj" % (dir, i)
            exporter.SetFileName(path)
            exporter.SetInput(actor.GetMapper().GetInput())
            exporter.Write()"""


def save_stl(actor, dir, name):
    exporter = vtk.vtkSTLWriter()
    if not os.path.isdir(dir):
        os.makedirs(dir)

    path = '%s/%s.stl' % (dir, name)
    exporter.SetFileName(path)
    exporter.SetInput(actor.GetMapper().GetInput())
    exporter.Write()


def save_vrml(name, dir, rw):
    if not os.path.isdir(dir):
        os.makedirs(dir)

    path = '%s/%s.vrml' % (dir, name)
    rw.Render()
    exporter = vtk.vtkVRMLExporter()
    exporter.SetFileName(path)
    exporter.SetRenderWindow(rw)
    rw.Render()
    exporter.Write()


def initActorForExport(actor, rw, scale,reduction):
    ren = rw.GetRenderers().GetFirstRenderer()
    ren.AddActor(reduceMesh(underScale(actor, scale),reduction))


def main(input_filename, areas_filename, scale, is_imx, exportType=False, reduction =30  ,combine=False):
    # TODO: The following doesn't hide the RenderWindow :/
    # factGraphics = vtk.vtkGraphicsFactory()
    # factGraphics.SetUseMesaClasses(1)
    # factImage = vtk.vtkImagingFactory()
    # factImage.SetUseMesaClasses(1)

    if is_imx:
        vrml_filename = os.path.splitext(input_filename)[0] + ".vrml"
        names_filename = os.path.splitext(input_filename)[0] + ".names"
        args = ["{}".format(input_filename), "{}".format(vrml_filename), "{}".format(names_filename)]
        p = Process(target=parse_imx.main, args=[args])
        p.start()
        p.join()

        names_list = []
        with open(names_filename) as f:
            for line in f:
                line = re.sub(r'\n', '', line)
                names_list.append(line)
    else:
        vrml_filename = input_filename
        names_list = None

    rw = vtk.vtkRenderWindow()
    # rwi = vtk.vtkRenderWindowInteractor()
    # rwi.SetRenderWindow(rw)
    rw.OffScreenRenderingOn()

    importer = vtk.vtkVRMLImporter()
    importer.SetFileName(vrml_filename)
    # importer = vtk.vtk3DSImporter()
    # importer.SetFileName("cube.3ds")
    importer.Read()
    importer.SetRenderWindow(rw)
    importer.Update()

    rw.Render()

    ren = importer.GetRenderer()
    actors = ren.GetActors()
    actors.InitTraversal()

    rwExport = vtk.vtkRenderWindow()
    rwExport.OffScreenRenderingOn()
    renExport = vtk.vtkRenderer()
    rwExport.AddRenderer(renExport)

    rwExport.Render()

    if is_imx:
        csv = "Object,Pre_Area,Post_Area,Post/Pre,X,Y,Z,Name\n"
    else:
        csv = "Object,Pre_Area,Post_Area,Post/Pre,X,Y,Z\n"

    print "-------- Repairing original mesh and Calculating areas (This process might take a long time, please wait) -----------"
    for i in range(ren.GetNumberOfPropsRendered()):
        sys.stdout.write("%d _" % i)
        actor = actors.GetNextActor()
        area_pre = compute_area(actor)
        centroid = actor.GetCenter()
        try:
            open_actor(actor, i, scale)
        except ValueError, e:
            # [KNOWN BUG] The sizes are corrected, but not the position
            scale = scale * 2
            open_actor(actor, i, scale)
        area_post = compute_area(actor) / scale ** 2

        if is_imx:
            data = []
            data.extend([i, area_pre, area_post, area_post / area_pre])
            data.extend(centroid)
            data.append(names_list[i])
            csv += "%d,%f,%f,%f,%f,%f,%f,%s\n" % tuple(data)

        else:
            data = []
            data.extend([i, area_pre, area_post, area_post / area_pre])
            data.extend(centroid)
            csv += "%d,%f,%f,%f,%f,%f,%f\n" % tuple(data)

        if exportType != "None":
            initActorForExport(actor, rwExport, scale,reduction)
            if names_list is not None:
                name = names_list[i]
            else:
                name = i

            if exportType == "Stl":
                save_stl(actor, os.path.splitext(input_filename)[0], str(name))
            elif exportType == "Vrml":
                save_vrml(str(name), os.path.splitext(input_filename)[0],rwExport)
            """elif exportType == "Obj":
                    print("-------- Saving obj files (This process might take a long time, please wait) -----------")
                    save_obj(actors_list, os.path.splitext(input_filename)[0], names_list)"""


        ren.RemoveActor(actor)
        renExport.RemoveActor(actor)



    with open(areas_filename, 'w') as f:
        f.write(csv)
    if is_imx:
        os.remove(vrml_filename)
        os.remove(names_filename)

    rw.Finalize()
    print ""
