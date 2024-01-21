from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer, GrammarFuzzer
from fuzzingbook.Grammars import trim_grammar
import grammar

from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer, exp_order
from fuzzingbook.GeneratorGrammarFuzzer import opts
from grammar import Database


class CustomFuzzer(ProbabilisticGeneratorGrammarFuzzer):
    def fuzz_tree(self):
        while True:
            tree = GrammarFuzzer.fuzz_tree(self)
            return tree
    
    def choose_tree_expansion(self, tree, expandable_children):
        #print("choosing an expansion")
        """Return index of subtree in `expandable_children`
           to be selected for expansion. Defaults to random."""
        (symbol, tree_children) = tree
        assert isinstance(tree_children, list)

        if len(expandable_children) == 1:
            # No choice
            return GrammarFuzzer.choose_tree_expansion(self, tree, expandable_children)

        expansion = self.find_expansion(tree)
        given_order = exp_order(expansion)
        if given_order is None:
            # No order specified
            return GrammarFuzzer.choose_tree_expansion(self, tree, expandable_children)

        nonterminal_children = [c for c in tree_children if c[1] != []]
        assert len(nonterminal_children) == len(given_order), \
            "Order must have one element for each nonterminal"

        # Find expandable child with lowest ordering
        min_given_order = None
        j = 0
        for k, expandable_child in enumerate(expandable_children):
            while j < len(nonterminal_children) and expandable_child != nonterminal_children[j]:
                j += 1
            assert j < len(nonterminal_children), "Expandable child not found"
            if self.log:
                print("Expandable child #%d %s has order %d" %
                      (k, expandable_child[0], given_order[j]))

            if min_given_order is None or given_order[j] < given_order[min_given_order]:
                min_given_order = k

        assert min_given_order is not None

        if self.log:
            print("Returning expandable child #%d %s" %
                  (min_given_order, expandable_children[min_given_order][0]))
        return min_given_order

class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
    
    def setup_fuzzer(self):
        # This function may be changed.
        self.count = 0
        self.grammar["<start>"] = [("<create_table_phase>", opts(prob = 1.0)), 
                                   "<create_index_view_phase>",
                                   "<other_phase>",
                                   ]
        self.fuzzer = CustomFuzzer(trim_grammar(self.grammar))

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        f = self.fuzzer.fuzz()
        
        if self.count < 1000:
            pass
        
        elif self.count>= 1000 and self.count <= 2000:
            self.grammar["<start>"] = [("<create_table_phase>",opts(prob=0.35)),
                                       ("<create_index_view_phase>", opts(prob=0.65)),
                                       "<other_phase>" ,
                                    ]
            self.fuzzer = CustomFuzzer(trim_grammar(self.grammar))
        else:
            self.grammar["<start>"] = [("<create_table_phase>", opts(prob=0.1)), 
                                       ("<create_index_view_phase>", opts(prob=0.1)),
                                       "<other_phase>",
                                    ]
            self.fuzzer = CustomFuzzer(trim_grammar(self.grammar))
        
        self.count += 1
        return f
