class Node:

    def __init__(self, id, label, interval):
        self.id = id
        self.label = label
        self.interval = interval

class Edge:

    def __init__(self, id, label, interval, source, target):
        self.id = id
        self.label = label
        self.interval = interval
        self.source = source
        self.target = target

class Nodes:
    
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.steps = []
        self.read('debug.txt')
        self.cur_index = 0
        self.cur_nodes = {i: self.nodes[i] for i in self.steps[0]['mnodes'] if not i in self.steps[0]['rnodes']}

    def __len__(self):
        return len(self.steps)
        
    def __getitem__(self, index):
        if index > self.cur_index:
            add, mnodes, rnodes =  1, 'mnodes', 'rnodes'
        else:
            add, mnodes, rnodes = -1, 'rnodes', 'mnodes'
        
        while self.cur_index != index:
            if add ==  1: self.cur_index += 1
            for i in self.steps[self.cur_index][mnodes]:
                self.cur_nodes[i] = self.nodes[i]
            for i in self.steps[self.cur_index][rnodes]:
                del self.cur_nodes[i]
            if add == -1: self.cur_index -= 1
        return self.steps[self.cur_index]['gonext'], self.cur_nodes

        
    def read(self, fileName):
        maxid = -1
        ndids = []
        with open(fileName, 'r') as file:
            lines = iter(file.readlines())
            lines.__next__()
            while True:
                try: 
                    gonext = int(lines.__next__())
                except StopIteration: 
                    break
                remove = [int(i) for i in lines.__next__().split()]
                self.steps.append({'gonext': gonext, 'mnodes': [], 'rnodes': []})
                for line in lines:
                    if line == '\n': break
                    line = [int(i) for i in line.split()]
                    maxid += 1
                    self.steps[-1]['mnodes'].append(maxid)
                    if len(ndids) > line[0]:
                        if ndids[line[0]] != -1: 
                            self.steps[-1]['rnodes'].append(ndids[line[0]])
                            for i in range(3):
                                self.edges[3*ndids[line[0]]+i].interval[1] = len(self.steps)
                            self.nodes[ndids[line[0]]].interval[1] = len(self.steps)
                        ndids[line[0]] = maxid
                    else:
                        ndids.append(maxid)
                    for i in range(3):
                        self.edges.append(Edge(3*maxid+i, i, [len(self.steps), -1], maxid, line[i] if line[i] >= len(ndids) else ndids[line[i]]))
                    self.nodes.append(Node(maxid, line[-1] >>2, [len(self.steps), -1]))
                for indx in remove:
                    if ndids[indx] != -1:
                        self.steps[-1]['rnodes'].append(ndids[indx])
                        ndids[indx] = -1
                        for i in range(3):
                            self.edges[3*ndids[indx]+i].interval[1] = len(self.steps)
                        self.nodes[ndids[indx]].interval[1] = len(self.steps)

        for n in self.nodes:
            if n.interval[1] == -1:
                n.interval[1] = len(self.steps)

        for e in self.edges:
            if e.interval[1] == -1:
                e.interval[1] = len(self.steps)

    def write(self):
        nodes = open('debug_nodes.csv', mode='w')
        print('iteration, action, id, label', file=nodes)
        edges = open('debug_edges.csv', mode='w')
        print('iteration, action, id, label, source, target', file=edges)
        for i, step in enumerate(self.steps):
            for n in step['rnodes']:
                print(f'{i}, remove, {n},',  file=nodes)
                for e in range(3*n,3*n+3):
                    print(f'{i}, remove, {e}, , ,', file=edges)
            for n in step['mnodes']:
                print(f'{i}, insert, {n}, {self.nodes[n].label}',  file=nodes)
                for e in range(3*n,3*n+3):
                    edge = self.edges[e]
                    print(f'{i}, insert, {e}, {edge.label}, {edge.source}, {edge.target}', file=edges)

if __name__ == '__main__':
    Nodes().write()
