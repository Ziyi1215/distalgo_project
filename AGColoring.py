# -*- generated by 1.0.12 -*-
import da
PatternExpr_521 = da.pat.TuplePattern([da.pat.ConstantPattern('PAYLOAD'), da.pat.FreePattern('color'), da.pat.FreePattern('stage')])
PatternExpr_528 = da.pat.FreePattern('src')
_config_object = {}
import networkx as nx
import lib
import vis
import math

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_521, sources=[PatternExpr_528], destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_520])])

    def setup(self, neighbors, idmapping, n, nid, delta, q, color, **rest_664):
        super().setup(neighbors=neighbors, idmapping=idmapping, n=n, nid=nid, delta=delta, q=q, color=color, **rest_664)
        self._state.neighbors = neighbors
        self._state.idmapping = idmapping
        self._state.n = n
        self._state.nid = nid
        self._state.delta = delta
        self._state.q = q
        self._state.color = color
        self._state.delta = self._state.delta
        self._state.q = self._state.q
        self._state.counter = 0
        self._state.nid = self._state.nid
        self._state.idmapping = self._state.idmapping
        self._state.stage = 0
        self._state.reduced_color = None
        self._state.color = (math.floor((self._state.color / self._state.q)), (self._state.color % self._state.q))
        self._state.responded = []

    def run(self):
        self.send(('PAYLOAD', self._state.color, 0), to=self._state.neighbors)
        for i in range(self._state.q):
            super()._label('_st_label_270', block=False)
            _st_label_270 = 0
            while (_st_label_270 == 0):
                _st_label_270 += 1
                if (len(self._state.responded) == len(self._state.neighbors)):
                    _st_label_270 += 1
                else:
                    super()._label('_st_label_270', block=True)
                    _st_label_270 -= 1
            else:
                if (_st_label_270 != 2):
                    continue
            if (_st_label_270 != 2):
                break
            msgs = self._state.responded
            if (self._state.stage == 0):
                if any(map((lambda x: (x[1][1] == self._state.color[1])), msgs)):
                    self._state.color = (self._state.color[0], ((self._state.color[0] + self._state.color[1]) % self._state.q))
                else:
                    self._state.color = (0, self._state.color[1])
                    self.output(('My Color: %s' % str(self._state.color)))
                    self._state.stage = 1
                    self._state.reduced_color = self._state.color[1]
                self._state.responded.clear()
                self.send(('PAYLOAD', self._state.color, 0), to=self._state.neighbors)
            elif (self._state.stage == 1):
                (unfinished, finalized) = lib.list_group_by((lambda x: ((x[2] == 0) and (not (x[1][0] == 0)))), msgs)
                if unfinished:
                    self._state.responded.clear()
                    self.send(('PAYLOAD', self._state.color, 0), to=self._state.neighbors)
                else:
                    if (self._state.reduced_color <= (self._state.delta + 1)):
                        self.output(('Reduced color: ' + str(self._state.reduced_color)))
                    else:
                        finalized_colors = [(msg[1][1] if (msg[2] == 0) else msg[1]) for msg in finalized]
                        remaining_colors = (set([i for i in range((self._state.delta + 1))]) - set(finalized_colors))
                        self._state.reduced_color = min(remaining_colors)
                    self._state.responded.clear()
                    self.send(('PAYLOAD', self._state.reduced_color, 1), to=self._state.neighbors)
        self.output('exit')

    def _P_handler_520(self, color, stage, src):
        self._state.responded.append(('PAYLOAD', color, stage))
    _P_handler_520._labels = None
    _P_handler_520._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': 'reliable'}

    def run(self):
        n = 20
        ps = self.new(P, num=n)
        id_mapping = {p: id for (id, p) in enumerate(ps)}
        rev_mapping = {id: p for (id, p) in enumerate(ps)}
        G = lib.gen_random_graph(n)
        delta = lib.calc_delta(G)
        print(('Maximum degree: ' + str(delta)))
        for (id, adj) in G.adjacency():
            nbs_id = list(adj.keys())
            nbs_rev = [rev_mapping[i] for i in nbs_id]
            q = lib.choose_prime((2 * delta))
            self._setup({rev_mapping[id]}, (nbs_rev, id_mapping, n, id, delta, q, id))
        self._start(ps)
