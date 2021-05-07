import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F

import grb.utils as utils
from grb.attack.base import InjectionAttack
from grb.utils import evaluator


class SPEIT(InjectionAttack):
    def __init__(self, dataset, adj_norm_func=None, device='cpu'):
        self.dataset = dataset
        self.n_total = dataset.num_nodes
        self.n_test = dataset.num_test
        self.n_feat = dataset.num_features
        self.n_inject_max = 0
        self.n_edge_max = 0
        self.adj_norm_func = adj_norm_func
        self.device = device
        self.config = {}

    def set_config(self, **kwargs):
        self.config['lr'] = kwargs['lr']
        self.config['n_epoch'] = kwargs['n_epoch']
        self.config['feat_lim_min'] = kwargs['feat_lim_min']
        self.config['feat_lim_max'] = kwargs['feat_lim_max']
        self.config['inject_mode'] = kwargs['inject_mode']
        self.n_inject_max = kwargs['n_inject_max']
        self.n_edge_max = kwargs['n_edge_max']

    def attack(self, model, target_node):
        if 'inject_mode' in self.config:
            inject_mode = self.config['inject_mode']
        else:
            inject_mode = 'random-inter'
        model.to(self.device)
        features = self.dataset.features
        features = torch.FloatTensor(features).to(self.device)
        adj = self.dataset.adj
        adj_tensor = utils.adj_preprocess(adj, adj_norm_func=self.adj_norm_func, device=self.device)
        pred_orig = model(features, adj_tensor)
        origin_labels = torch.argmax(pred_orig, dim=1)
        adj_attack = self.injection(adj=adj,
                                    n_inject=self.n_inject_max,
                                    target_node=target_node,
                                    mode=inject_mode)

        features_attack = np.zeros([self.n_inject_max, self.n_feat])
        features_attack = self.update_features(model=model,
                                               adj_attack=adj_attack,
                                               features=features,
                                               features_attack=features_attack,
                                               origin_labels=origin_labels)

        return adj_attack, features_attack

    def injection(self, adj, n_inject, target_node, mode='random-inter'):
        def get_inject_list(adj, n_inter, inject_id, inject_tmp_list):
            i = 1
            res = []
            while len(res) < n_inter and i < len(inject_tmp_list):
                if adj[inject_id, inject_tmp_list[i]] == 0:
                    res.append(inject_tmp_list[i])
                i += 1

            return res

        def update_active_edges(active_edges, n_inject_edges, threshold):
            for i in active_edges:
                if n_inject_edges[i] >= threshold:
                    active_edges.pop(active_edges.index(i))

            return active_edges

        def inject(target_node_list, n_inject, n_test, mode='random-inter'):
            n_target = len(target_node_list)
            adj = np.zeros((n_inject, n_test + n_inject))

            if mode == 'random-inter':
                # target_node_list: a list of target nodes to be attacked
                n_inject_edges = np.zeros(n_inject)
                active_edges = [i for i in range(n_inject)]

                # create edges between injected node and target node
                for i in range(n_target):
                    if not active_edges:
                        break
                    inject_id = np.random.choice(active_edges, 1)
                    n_inject_edges[inject_id] += 1
                    active_edges = update_active_edges(active_edges, n_inject_edges, threshold=self.n_edge_max)
                    adj[inject_id, target_node_list[i]] = 1

                # create edges between injected nodes
                for i in range(len(active_edges)):
                    if not active_edges:
                        break
                    inject_tmp_list = sorted(active_edges, key=lambda x: n_inject_edges[x])
                    inject_id = inject_tmp_list[0]
                    n_inter = self.n_edge_max - n_inject_edges[inject_id]
                    inject_list = get_inject_list(adj, n_inter, inject_id, inject_tmp_list)

                    n_inject_edges[inject_list] += 1
                    n_inject_edges[inject_id] += len(inject_list)
                    active_edges = update_active_edges(active_edges, n_inject_edges, threshold=self.n_edge_max)
                    if inject_list:
                        adj[inject_id, n_test + np.array(inject_list)] = 1
                        adj[inject_list, n_test + inject_id] = 1

            elif mode == 'multi-layer':
                n_inject_edges = np.zeros(n_inject)
                n_inject_layer_1, n_inject_layer_2 = int(n_inject * 0.9), int(n_inject * 0.1)
                n_edge_max_layer_1 = int(self.n_edge_max * 0.9)
                active_edges = [i for i in range(n_inject_layer_1)]

                # create edges between noise node and test node
                for i in range(n_target):
                    if not active_edges:
                        break
                    inject_id = np.random.choice(active_edges, 1)
                    n_inject_edges[inject_id] += 1
                    active_edges = update_active_edges(active_edges, n_inject_edges, threshold=n_edge_max_layer_1)
                    adj[inject_id, target_node_list[i]] = 1

                # create edges between injected nodes
                for i in range(len(active_edges)):
                    if not active_edges:
                        break
                    inject_tmp_list = sorted(active_edges, key=lambda x: n_inject_edges[x])
                    inject_id = inject_tmp_list[0]
                    n_inter = n_edge_max_layer_1 - n_inject_edges[inject_id]
                    inject_list = get_inject_list(adj, n_inter, inject_id, inject_tmp_list)

                    n_inject_edges[inject_list] += 1
                    n_inject_edges[inject_id] += len(inject_list)

                    active_edges = update_active_edges(active_edges, n_inject_edges, threshold=n_edge_max_layer_1)

                    if inject_list:
                        adj[inject_id, n_test + np.array(inject_list)] = 1
                        adj[inject_list, n_test + inject_id] = 1

                noise_active_layer2 = [i for i in range(n_inject_layer_2)]
                noise_edge_layer2 = np.zeros(n_inject_layer_2)
                for i in range(n_inject_layer_1):
                    if not noise_active_layer2:
                        break
                    inject_list = np.random.choice(noise_active_layer2, 10)
                    noise_edge_layer2[inject_list] += 1
                    noise_active_layer2 = update_active_edges(noise_active_layer2, noise_edge_layer2,
                                                              threshold=self.n_edge_max)
                    adj[inject_list + n_inject_layer_1, i + n_test] = 1
                    adj[i, inject_list + n_inject_layer_1 + n_test] = 1

            else:
                print("Mode ERROR: 'mode' should be one of ['random-inter', 'multi-layer']")

            return adj

        # construct injected adjacency matrix
        adj_inject = inject(target_node, n_inject, self.n_test, mode)
        adj_inject = sp.hstack([sp.csr_matrix((n_inject, self.n_total - self.n_test)), adj_inject])
        adj_inject = sp.csr_matrix(adj_inject)
        adj_attack = sp.vstack([self.dataset.adj, adj_inject[:, :self.n_total]])
        adj_attack = sp.hstack([adj_attack, adj_inject.T])
        adj_attack = sp.coo_matrix(adj_attack)

        return adj_attack

    def update_features(self, model, adj_attack, features, features_attack, origin_labels):
        lr = self.config['lr']
        n_epoch = self.config['n_epoch']
        feat_lim_min, feat_lim_max = self.config['feat_lim_min'], self.config['feat_lim_max']

        adj_attacked_tensor = utils.adj_preprocess(adj_attack, adj_norm_func=self.adj_norm_func, device=self.device)
        features_attack = torch.FloatTensor(features_attack).to(self.device)
        features_attack.requires_grad_(True)
        optimizer = torch.optim.Adam([features_attack], lr=lr)
        model.eval()
        for i in range(n_epoch):
            features_concat = torch.cat((features, features_attack), dim=0)
            pred = model(features_concat, adj_attacked_tensor)
            pred_loss = -F.nll_loss(pred[:self.n_total][self.dataset.test_mask],
                                    origin_labels[self.dataset.test_mask]).to(self.device)
            optimizer.zero_grad()
            pred_loss.backward(retain_graph=True)
            optimizer.step()

            with torch.no_grad():
                features_attack.clamp_(feat_lim_min, feat_lim_max)
            print("Epoch {}, Loss: {:.5f}, Test acc: {:.5f}".format(i, pred_loss,
                                                                    evaluator.eval_acc(
                                                                        pred[:self.n_total][self.dataset.test_mask],
                                                                        origin_labels[self.dataset.test_mask])))

        return features_attack