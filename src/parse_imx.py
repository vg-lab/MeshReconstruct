#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as et
# stats de 6909 espinas , media = 415 , min = 34 , max =2546
MAX_VERTEX_TO_SPINE = 10000
MIN_VERTEX_TO_SPINE = 10


def create_names_file(names_filename):
    text = ''
    with open(names_filename, 'w') as f:
        f.write(text)


def create_vrml(vrml_filename):
    text = '#VRML V2.0 utf8\n#Inventor V2.1 ascii\n\n'
    with open(vrml_filename, 'w') as f:
        f.write(text)


def append_to_names_file(names_filename, text):
    with open(names_filename, 'a') as f:
        f.write(text + '\n')


def append_to_vrml(vrml_filename, text):
    with open(vrml_filename, 'a') as f:
        f.write(text + '\n')


def format_imx_vec3(color):
    color = color.replace('((', '')
    color = color.replace('))', '')
    color = color.replace(',', ' ')
    return color


def format_imx_scalar(scalar):
    scalar = scalar.replace('(', '')
    scalar = scalar.replace(')', '')
    return scalar


def split_list(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]


def parse_material(node, vrml_filename, tab):
    append_to_vrml(vrml_filename, tab + 'appearance Appearance {')
    tab += '  '
    append_to_vrml(vrml_filename, tab + 'material Material {')
    tab += '  '
    children = len(node.getchildren())
    count = 1
    for child in node:
        comma = ''
        if count < children:
            comma = ','
        if 'Color' in child.tag:
            child.text = format_imx_vec3(child.text)
            if child.tag == 'ambientColor':
                ambientIntensities = [float(x) for x in child.text.split()]
                ambientIntensity = 0.0
                for ac in ambientIntensities:
                    ambientIntensity += ac
                ambientIntensity /= 3.0
                child.tag = 'ambientIntensity'
                child.text = str(ambientIntensity)
        if 'shininess' == child.tag or 'transparency' == child.tag:
            child.text = format_imx_scalar(child.text)
        append_to_vrml(vrml_filename, tab + child.tag + ' ' + child.text + comma)
        count += 1
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + '}')
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + '}')


def parse_bpSurfaces(node, vrml_filename, tab):
    max_triangle = 0

    all_vertices_list = []
    all_triangles_list = []
    vertices_list = []
    normals_list = []

    for surface in node.findall('surface'):
        for vertices in surface.findall('vertices'):
            vertices_str = re.sub(r'\"', '', vertices.text)
            all_vertices_list += vertices_str.split()
        triangles_list = []
        for triangles in surface.findall('triangles'):
            triangles_str = re.sub('\"', '', triangles.text)
            triangles_list += triangles_str.split()
        triangles_list = [int(x) + max_triangle for x in triangles_list]
        max_triangle = max(triangles_list) + 1
        all_triangles_list += triangles_list

    all_vertices_list = iter(split_list(all_vertices_list, 3))

    for index, item in enumerate(all_vertices_list, 0):
        if index % 2 == 0:
            vertices_list += item
        else:
            normals_list += item

    #Si el numero de vertices no coincide con el de una espina se ignora
    if MAX_VERTEX_TO_SPINE > len(vertices_list) > MIN_VERTEX_TO_SPINE:
        return all_triangles_list, normals_list, tab, vertices_list, vrml_filename
    return False


def printSurface(tuple):
    (all_triangles_list,normals_list,tab,vertices_list,vrml_filename) =  tuple

    # patterns to parse vertices && triangles
    vertex_pattern = '[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
    vertices_pattern = '(' + vertex_pattern + '\s' + vertex_pattern + '\s' + vertex_pattern + ')'
    triangle_pattern = '([-+]?\d+)'
    triangles_pattern = triangle_pattern + '\s' + triangle_pattern + '\s' + triangle_pattern + '\s' + triangle_pattern + '\s' + triangle_pattern + '\s' + triangle_pattern

    append_to_vrml(vrml_filename, tab + 'geometry IndexedFaceSet {')
    tab += '  '
    # vertices
    if len(vertices_list) > 0:
        append_to_vrml(vrml_filename, tab + 'coord Coordinate {')
        tab += '  '
        append_to_vrml(vrml_filename, tab + 'point [')
        tab += '  '

        vertices_text = ' '.join(str(x) for x in vertices_list)
        vertices_text = re.sub(vertices_pattern, tab + r'\1,\n', vertices_text)
        vertices_text = re.sub(r',\n$', r'', vertices_text)
        append_to_vrml(vrml_filename, vertices_text)

        tab = tab[:-2]
        append_to_vrml(vrml_filename, tab + ']')
        tab = tab[:-2]
        append_to_vrml(vrml_filename, tab + '}')

    # normals
    if len(normals_list) > 0:
        append_to_vrml(vrml_filename, tab + 'normal Normal {')
        tab += '  '
        append_to_vrml(vrml_filename, tab + 'vector [')
        tab += '  '

        normals_text = ' '.join(str(x) for x in normals_list)
        normals_text = re.sub(vertices_pattern, tab + r'\1,\n', normals_text)
        normals_text = re.sub(r',\n$', r'', normals_text)
        append_to_vrml(vrml_filename, normals_text)

        tab = tab[:-2]
        append_to_vrml(vrml_filename, tab + ']')
        tab = tab[:-2]
        append_to_vrml(vrml_filename, tab + '}')

    # vertices triangles && normal triangles
    if len(all_triangles_list) > 0:

        triangles_text = ' '.join(str(x) for x in all_triangles_list)
        triangles_text = re.sub(triangles_pattern, tab + r'\1, \2, \3, -1, \4, \5, \6, -1,\n', triangles_text)
        triangles_text = re.sub(r',\n$', r'', triangles_text)

        if len(vertices_list) > 0:
            append_to_vrml(vrml_filename, tab + 'coordIndex [ ')
            tab += '  '
            append_to_vrml(vrml_filename, triangles_text)
            tab = tab[:-2]
            append_to_vrml(vrml_filename, tab + ']')

        if len(normals_list) > 0:
            append_to_vrml(vrml_filename, tab + 'normalIndex [ ')
            tab += '  '
            append_to_vrml(vrml_filename, triangles_text)
            tab = tab[:-2]
            append_to_vrml(vrml_filename, tab + ']')
    append_to_vrml(vrml_filename, tab + 'ccw TRUE')
    append_to_vrml(vrml_filename, tab + 'solid FALSE')
    append_to_vrml(vrml_filename, tab + 'convex TRUE')
    append_to_vrml(vrml_filename, tab + 'creaseAngle 0')
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + '}')


def parse_bpSurfaceComponent(node, vrml_filename, names_filename, tab):
    for child in node:
        if child.tag == 'bpComponentGroup':
            parse_bpComponentGroup(child, vrml_filename, names_filename, tab)
        elif child.tag == 'bpSurfacesViewer':
            parse_bpSurfacesViewer(child, vrml_filename, names_filename, tab)


def parse_bpSurfacesViewer(node, vrml_filename, names_filename, tab):
    bpSurface = node.find('bpSurfaces')
    if bpSurface is not None:
        result = parse_bpSurfaces(bpSurface,vrml_filename,tab)
        if isinstance(result,tuple): # si es una tupla el metodo ha determinado que es una espina
            shape = 'Shape {'
            bpSurfaceComponent = node.find('bpSurfaceComponent')
            if bpSurfaceComponent is not None:
                name = bpSurfaceComponent.find('name')
                if name is not None:
                    if name.text is not None:
                        append_to_names_file(names_filename, name.text)
                    else:
                        append_to_names_file(names_filename, '')
            append_to_vrml(vrml_filename, tab + shape)
            tab += '  '
            printSurface(result)
            material = bpSurfaceComponent.find('material')
            if material is not None:
                parse_material(material, vrml_filename, tab)
            tab = tab[:-2]
            append_to_vrml(vrml_filename, tab + '}')

    """ shape = 'Shape {'
    bpSurfaceComponent = node.find('bpSurfaceComponent')
    if bpSurfaceComponent is not None:
        name = bpSurfaceComponent.find('name')
        if name is not None:
            if name.text is not None:
                append_to_names_file(names_filename, name.text)
            else:
                append_to_names_file(names_filename, '')
    append_to_vrml(vrml_filename, tab + shape)
    tab += '  '
    for child in node:
        if child.tag == 'bpSurfaces':
            parse_bpSurfaces(child, vrml_filename, tab)
        elif child.tag == 'bpSurfaceComponent':
            material = child.find('material')
            if material is not None:
                parse_material(material, vrml_filename, tab)
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + '}') #"""


def parse_bpComponentGroup(node, vrml_filename, names_filename, tab):
    append_to_vrml(vrml_filename, tab + 'Group {')
    tab += '  '
    append_to_vrml(vrml_filename, tab + 'children [')
    tab += '  '
    for child in node:
        if child.tag == 'bpComponentGroup':
            parse_bpComponentGroup(child, vrml_filename, names_filename, tab)
        elif child.tag == 'bpSurfacesViewer':
            parse_bpSurfacesViewer(child, vrml_filename, names_filename, tab)
        elif child.tag == 'bpSurfaceComponent':
            parse_bpSurfaceComponent(child, vrml_filename, names_filename, tab)
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + ']')
    tab = tab[:-2]
    append_to_vrml(vrml_filename, tab + '}')


def parse_bpSurfaceApplication(node, vrml_filename, names_filename, tab):
    for child in node:
        if child.tag == 'bpComponentGroup':
            parse_bpComponentGroup(child, vrml_filename, names_filename, tab)
        elif child.tag == 'bpSurfacesViewer':
            parse_bpSurfacesViewer(child, vrml_filename, names_filename, tab)
        elif child.tag == 'bpSurfaceComponent':
             parse_bpSurfaceComponent(child, vrml_filename, names_filename, tab)


def parse_root(node, vrml_filename, names_filename):
    bpSurfaceApplication = node.find('bpSurfaceApplication')
    if bpSurfaceApplication is not None:
        print('parsing imx file to vrml format... '),
        tab = ''
        create_vrml(vrml_filename)
        create_names_file(names_filename)
        parse_bpSurfaceApplication(bpSurfaceApplication, vrml_filename, names_filename, tab)

        print('[DONE]')
    else:
        print 'Error in imx file: bpSurfaceApplication node not found!'


def main(args):
    if args is not None:
        imx_filename = args[0]
        vrml_filename = args[1]
        names_filename = args[2]
        root = et.parse(imx_filename).getroot()
        parse_root(root, vrml_filename, names_filename)
    else:
        print 'Error: no arguments passed to parser.'


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
