#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk
import sys
import os
import optparse
import glob

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
    (minX, maxX, minY, maxY, minZ, maxZ) = [int(x * scale) for x in polydata.GetBounds()]  #convert tuple of floats to ints

    #print "  Selection bounds are %s"%str((minX, maxX, minY, maxY, minZ, maxZ))  #dimensions of the resulting image
    #print "  Dimensions: %s"%str((maxX - minX, maxY - minY, maxZ - minZ))

    padd = RADIUS+6
    (minX, maxX, minY, maxY, minZ, maxZ) = (minX-padd, maxX+padd, minY-padd, maxY+padd, minZ-padd, maxZ+padd)

    ps1 = 1.0 / float(scale)  # pixel size for the stencil, make sure it's a float division!
    ps2 = 1.0        # pixel size for the image

    ## Convert a surface mesh into an image stencil that can be used to mask an image with vtkImageStencil.
    polyToStencilFilter = vtk.vtkPolyDataToImageStencil()
    polyToStencilFilter.SetInput(polydata)
    polyToStencilFilter.SetOutputWholeExtent(minX, maxX, minY, maxY, minZ, maxZ)
    polyToStencilFilter.SetOutputSpacing(ps1, ps1, ps1)
    polyToStencilFilter.SetOutputOrigin(0.0, 0.0, 0.0)
    polyToStencilFilter.Update()

    # Create an empty (3D) image of appropriate size.
    image = vtk.vtkImageData();
    image.SetSpacing(ps2, ps2, ps2);
    image.SetOrigin(0.0, 0.0, 0.0);
    image.SetExtent(minX, maxX, minY, maxY, minZ, maxZ);
    image.SetScalarTypeToUnsignedChar();
    image.AllocateScalars();

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

    #image_to_contour = pre_image
    #image_to_contour = opened_image
    image_to_contour = gauss.GetOutput()

    contour = vtk.vtkMarchingCubes()
    contour.SetInput(image_to_contour)
    contour.SetValue(0, 127.5)
    contour.ComputeScalarsOff()
    contour.Update()

    repared_poly = contour.GetOutput()

    if repared_poly.GetNumberOfCells() == 0:
        print "ERROR: number_of_cells = 0",
        #write_image(image_to_contour, "/tmp/%d.mhd"%actor_index)
        raise ValueError("ERROR: number_of_cells = 0")
    else:
        print '_  ',

    #(minX, maxX, minY, maxY, minZ, maxZ) = [int(x) for x in repared_poly.GetBounds()] #convert tuple of floats to ints
    #print "  Repared bounds are %s"%str((minX, maxX, minY, maxY, minZ, maxZ))  #dimensions of the resulting image
    #print "  Dimensions: %s"%str((maxX - minX, maxY - minY, maxZ - minZ))

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
    for actor, i in zip(actors_list, range(len(actors_list))):
        # scale = SCALE
        sys.stdout.write("%d " % i)
        area_pre = compute_area(actor)
        try:
            open_actor(actor, i, scale)
        except ValueError, e:
            # [KNOWN BUG] The sizes are corrected, but not the position
            scale = scale * 2
            open_actor(actor, i, scale)
        area_post = compute_area(actor) / scale**2

        areas.append( (i, area_pre, area_post, area_post / area_pre) )
        sys.stdout.flush()
    print "\n"
    return areas

def compute_centroids(actors_list):
    return [a.GetCenter() for a in actors_list]


def csv_areas(actors_list, filename, scale=SCALE):
    centroids = compute_centroids(actors_list) # Centroids of original actors
    areas = compute_all_areas(actors_list, scale)

    csv = "Object,Pre_Area,Post_Area,Post/Pre,X,Y,Z\n"
    for i in range(len(areas)):
        data = []
        data.extend(areas[i])
        data.extend(centroids[i])
        csv += "%d,%f,%f,%f,%f,%f,%f\n" % tuple(data)

    with open(filename, 'w') as f:
        f.write(csv)

def save_vrml(actors_list, output_filename, rw):
    exporter = vtk.vtkVRMLExporter()
    exporter.SetFileName(output_filename)
    exporter.SetRenderWindow(rw)
    ren = rw.GetRenderers().GetFirstRenderer()
    for actor in actors_list:
        ren.AddActor(actor)
    ren.ResetCamera()
    rw.Render()
    exporter.Write()


def main(input_filename, areas_filename, scale, combine=False):

    # TODO: The following doesn't hide the RenderWindow :/
    #factGraphics = vtk.vtkGraphicsFactory()
    #factGraphics.SetUseMesaClasses(1)
    #factImage = vtk.vtkImagingFactory()
    #factImage.SetUseMesaClasses(1)

    rw = vtk.vtkRenderWindow()
    #rwi = vtk.vtkRenderWindowInteractor()
    #rwi.SetRenderWindow(rw)
    rw.OffScreenRenderingOn()

    importer = vtk.vtkVRMLImporter()
    importer.SetFileName(input_filename)
    #importer = vtk.vtk3DSImporter()
    #importer.SetFileName("cube.3ds")
    importer.Read()
    importer.SetRenderWindow(rw)
    importer.Update()

    rw.Render()

    ren = importer.GetRenderer()
    actors = ren.GetActors()
    actors.InitTraversal()
    actors_list = [actors.GetNextActor() for x in range(ren.GetNumberOfPropsRendered())]

    if combine:
        actors_list = [combine_actors(actors_list)]

    csv_areas(actors_list, areas_filename, scale)
    save_vrml(actors_list, 'out.vrml', rw)
    rw.Finalize()


if __name__ == "__main__":

    options, _args = RepairMeshParser().parse_args()

    SCALE = float(options.scale)
    print "Remeshing with scale factor: ", SCALE
    if options.combine:
        print "Combining all polydatas in one object"

    if options.vrmls_dir:
        vrmls = glob.glob(os.path.join(options.vrmls_dir, "*.vrml"))
        for vrml in vrmls:
            name = os.path.basename(vrml).replace('.vrml','')
            out_filename = os.path.join(options.output_dir, name + ".csv")

            print '*** ', name
            main(vrml, out_filename, SCALE, options.combine)
    else:
        main(options.input_vrml, options.areas_file, SCALE, options.combine)
