from pygraphdb.graph_base import GraphBase
from pygraphdb.edge import Edge


class FullTest(object):

    def __init__(self, graph: GraphBase):
        self.graph = graph

    def run(self):
        g = self.graph
        edges = [
            Edge(1, 2, weight=4),
            Edge(2, 3, weight=20),
            Edge(3, 4, weight=10),
            Edge(4, 5, weight=3),
            Edge(5, 3, weight=2),
            Edge(4, 1, weight=5),
            Edge(8, 6, weight=4),
            Edge(8, 7, weight=2),
            Edge(6, 1, weight=3),
            Edge(7, 1, weight=2),
        ]
        # Fill the DB.
        es_last = 0
        vs_last = 0
        for e in edges:
            g.insert(e)
            assert g.edge_directed(e['v_from'], e['v_to']), \
                f'No directed edge: {e}'
            assert g.edge_undirected(e['v_from'], e['v_to']), \
                f'No undirected edge: {e}'
            # Make sure the size of the DB isn't getting smaller.
            # It may remain unchanged for persistent stores.
            es_count = g.count_edges()
            assert es_count >= es_last, 'Didnt update number of edges'
            es_last = es_count
            vs_count = g.count_vertexes()
            assert vs_count >= vs_last, 'Problems in counting nodes'
            vs_last = vs_count
        # Validate the queries.
        assert vs_last == 8, \
            f'count_nodes: {vs_last}'
        assert es_last == 10, \
            f'count_edges: {es_last}'
        assert g.count_followers(1) == (3, 10.0), \
            f'count_followers: {g.count_followers(1)}'
        assert g.count_following(1) == (1, 4.0), \
            f'count_following: {g.count_following(1)}'
        assert g.count_related(1) == (4, 14.0), \
            f'count_related: {g.count_related(1)}'
        assert g.vertexes_related(1) == {2, 4, 6, 7}, \
            f'vertexes_related: {g.vertexes_related(1)}'
        assert g.vertexes_related_to_related(8) == {1}, \
            f'vertexes_related_to_related: {g.vertexes_related_to_related(8)}'
        assert g.count_followers(5) == (1, 3.0), \
            f'count_followers: {g.count_followers(5)}'
        assert g.count_following(5) == (1, 2.0), \
            f'count_following: {g.count_following(5)}'
        # assert g.shortest_path(4, 3) == ([4, 5, 3], 5.0), \
        #     f'shortest_path: {g.shortest_path(4, 3)}'
        # Remove elements one by one.
        for e in edges:
            g.delete(e)
        # Bulk load data again.
        # Clear all the data at once.
