#!/usr/env python


class ArcEager(object):
    def SHIFT(self, config, label=None):
        """Moves the input from buffer to stack."""
        b0 = config.b0
        config.stack.append(b0)
        config.b0 = b0 + 1

    def RIGHTARC(self, config, label=None):
        """Right reduces the tokens at the buffer and stack. s0 -> b0"""
        b0 = config.b0
        s0 = config.stack[-1]
        s0N = config.nodes[s0]
        config.nodes[b0] = config.nodes[b0]._replace(pparent=s0N.id,
                                                     pdrel=label)
        config.nodes[s0] = config.nodes[s0]._replace(
                                        right=config.nodes[s0].right + [b0])
        config.stack.append(b0)
        config.b0 = b0 + 1

    def LEFTARC(self, config, label=None):
        """Left reduces the tokens at the stack and buffer. b0 -> s0"""
        b0 = config.b0
        s0 = config.stack.pop()
        b0N = config.nodes[b0]
        config.nodes[s0] = config.nodes[s0]._replace(pparent=b0N.id,
                                                     pdrel=label)
        config.nodes[b0] = config.nodes[b0]._replace(
                                        left=config.nodes[b0].left + [s0])

    def REDUCE(self, config, label=None):
        """pops the top of the stack if it has got its head."""
        config.stack.pop()

    def isFinalState(self, configs):
        """Checks if the parser is in final config i.e. all the input is
        consumed and both the stack and queue are empty.
        """
        for config in configs:
            # if any config is not in terminal state dont stop.
            if not (len(config.stack) == 0 and
                    len(config.nodes[config.b0:]) == 1):
                return False
        return True

    def get_valid_transitions(self, config):
        moves = {
            0: self.SHIFT,
            1: self.LEFTARC,
            2: self.RIGHTARC,
            3: self.REDUCE
            }
        b0 = config.b0
        if len(config.nodes[b0:]) == 1:
            assert(config.nodes[b0].id == 0)
            del moves[0]
            del moves[2]

        if len(config.stack) == 0:
            del moves[3]
        elif (config.nodes[b0:]):
            if config.nodes[config.stack[-1]].pparent == -1:
                del moves[3]

        if len(config.stack) < 1:
            del moves[1]
            del moves[2]
        else:
            if config.nodes[config.stack[-1]].pparent > -1:
                del moves[1]
            if config.nodes[b0].pparent > -1:
                del moves[2]
        return moves
