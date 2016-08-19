#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

"""
Implementation of tree transformation algorithms for handling non-projective
trees in transition based systems. The procedure is defined in Joakim Nivre
and Jens Nilsson, ACL 2005. http://stp.lingfil.uu.se/~nivre/docs/acl05.pdf
"""


def adjacency_matrix(nodes):
    """Builds an adjacency matrix of a dependency graph"""
    adj_mat = np.zeros((len(nodes),) * 2, int)
    for node in nodes:
        if node.parent == 0:
            continue
        child = node.id - 1
        parent = node.parent - 1
        adj_mat[parent, child] = 1
    return adj_mat


def ul_parent(nodes, stack, lin_head_lbl):
    while stack:
        imd_parent = stack.pop()
        if lin_head_lbl.strip("%") == nodes[
                imd_parent].pdrel.split("|")[0].strip("%"):
            syntactic_head = imd_parent
            return syntactic_head
    return 0


def BFS(nodes, tree, lin_head, lin_head_lbl, node):
    """Breadth First Search to locate syntactic head of a
    non-projective node.
    """
    # TODO bit messy, improve!
    syntactic_head = lin_head
    adj_list = np.nonzero(tree[lin_head])[0]
    # original tree
    queue = [j for j in adj_list if "%" in nodes[j].pdrel and node != j]
    stack = []
    while queue:
        q_node = queue.pop(0)
        if q_node == node:
            continue
        if lin_head_lbl.strip("%") == nodes[
                q_node].pdrel.split("|")[0].strip("%"):
            lookdown_q_node = [
                j for j in np.nonzero(
                    tree[q_node])[0] if "%" in nodes[j].pdrel]
            if (lookdown_q_node == []):
                syntactic_head = q_node
                break
            else:
                queue.extend(lookdown_q_node)
        else:
            adj_list = [
                j for j in np.nonzero(
                    tree[q_node])[0] if "%" in nodes[j].pdrel]
            if queue == [] and adj_list == []:
                _head = ul_parent(nodes, stack, lin_head_lbl)
                if _head:
                    syntactic_head = _head
            queue.extend(adj_list)
        stack.append(q_node)
    return syntactic_head


def deprojectivize(nodes, scheme="head+path"):
    """PseudoProjectivisation: Reverse transformation of pseudo-projective
    arcs into non-projective arcs using BFS."""
    tree = adjacency_matrix(nodes)
    for nC in range(0, len(nodes)):
        node = nodes[nC]
        parent, drel = node.pparent, node.pdrel
        if '|' in drel:
            lin_head = parent - 1
            syntactic_label, lin_head_lbl = drel.split("|")
            if '%' in drel:
                syntactic_label += "%"
            syntactic_head = BFS(nodes, tree, lin_head, lin_head_lbl,
                                 node.id - 1)
            # parent should be other the dummy root i.e. > 0
            if syntactic_head == lin_head and nodes[lin_head].pparent:
                syntactic_head = BFS(nodes, tree, nodes[lin_head].pparent - 1,
                                     lin_head_lbl, lin_head)
            nodes[nC] = nodes[nC]._replace(pparent=syntactic_head + 1,
                                           pdrel=syntactic_label)
            tree = adjacency_matrix(nodes)
    return nodes
