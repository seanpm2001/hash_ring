from __future__ import absolute_import
import pytest

from hash_ring import HashRingNode, HashRing
from six.moves import range

pytestmark = [pytest.mark.benchmark]


@pytest.mark.benchmark(group='add_nodes')
@pytest.mark.parametrize('num_nodes', [5, 10, 25, 50, 100])
def test_ring_add_nodes_slow(benchmark, num_nodes):
    def ring_slow():
        r = HashRing()
        nodes = []
        for i in range(num_nodes):
            r.add_node('test-%i' % i, num_replicas=512)

        r.add_nodes(nodes)

    benchmark(ring_slow)


@pytest.mark.benchmark(group='add_nodes')
@pytest.mark.parametrize('num_nodes', [5, 10, 25, 50, 100])
def test_ring_add_nodes_fast(benchmark, num_nodes):
    def ring_fast():
        r = HashRing()
        nodes = []
        for i in range(num_nodes):
            nodes.append(HashRingNode('test-%i' % i, num_replicas=512))

        r.add_nodes(nodes)

    benchmark(ring_fast)


@pytest.mark.benchmark(group='find_node')
@pytest.mark.parametrize('num_nodes', [5, 10, 25, 50, 100])
def test_ring_find_node(benchmark, num_nodes):
    r = HashRing()
    nodes = []
    for i in range(num_nodes):
        r.add_node('test-%i' % i, num_replicas=512)

    r.add_nodes(nodes)

    def ring_lookup():
        return r.find_node('hello')

    assert benchmark(ring_lookup) == r.find_node('hello')


@pytest.mark.benchmark(group='find_nodes')
@pytest.mark.parametrize('num_nodes', [5, 10, 25, 50, 100])
def test_ring_find_nodes(benchmark, num_nodes):
    r = HashRing()
    nodes = []
    for i in range(num_nodes):
        r.add_node('test-%i' % i, num_replicas=512)

    r.add_nodes(nodes)

    def ring_lookup():
        return r.find_nodes('hello', 3)

    assert benchmark(ring_lookup) == r.find_nodes('hello', 3)
