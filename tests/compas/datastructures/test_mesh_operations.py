import pytest

from compas.datastructures import Mesh
from compas.datastructures import mesh_insert_vertex_on_edge
from compas.datastructures import mesh_substitute_vertex_in_faces


@pytest.fixture
def mesh_0():
    vertices = [
        [1.0, 0.0, 0.0],
        [1.0, 2.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 1.0, 0.0],
        [0.0, 0.0, 0.0]
    ]
    faces = [
        [0, 1, 2],
        [0, 3, 1]
    ]

    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def mesh_quads():
    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 1.0, 0.0],
    ]
    faces = [
        [0, 1, 2, 3],
        [1, 4, 5, 2]
    ]

    return Mesh.from_vertices_and_faces(vertices, faces)


def test_insert_vertex_on_edge(mesh_0):
    mesh_insert_vertex_on_edge(mesh_0, 0, 1)
    assert len(mesh_0.face_vertices(0)) == 4
    assert len(mesh_0.face_vertices(1)) == 4
    assert mesh_0.face_vertex_descendant(0, 0) == 5
    assert mesh_0.face_vertex_descendant(1, 1) == 5

    mesh_insert_vertex_on_edge(mesh_0, 0, 2, 4)
    assert len(mesh_0.face_vertices(0)) == 5
    assert mesh_0.face_vertex_descendant(0, 2) == 4


def test_mesh_substitute_vertex_in_faces(mesh_0):
    mesh_substitute_vertex_in_faces(mesh_0, 0, 4)
    assert 4 in mesh_0.face_vertices(0)
    assert 0 not in mesh_0.face_vertices(0)
    assert 4 in mesh_0.face_vertices(1)
    assert 0 not in mesh_0.face_vertices(1)
    mesh_substitute_vertex_in_faces(mesh_0, 4, 0, [1])
    assert 4 in mesh_0.face_vertices(0)
    assert 0 not in mesh_0.face_vertices(0)
    assert 0 in mesh_0.face_vertices(1)
    assert 4 not in mesh_0.face_vertices(1)


def test_mesh_split_face(mesh_quads):
    mesh_quads.split_face(0, 0, 2)
    assert mesh_quads.number_of_faces() == 3


def test__split_face_vertex_not_in_face(mesh_quads):
    with pytest.raises(ValueError):
        mesh_quads.split_face(0, 0, 4)


def test_mesh_split_face_vertex_nbors(mesh_quads):
    with pytest.raises(ValueError):
        mesh_quads.split_face(0, 0, 1)
