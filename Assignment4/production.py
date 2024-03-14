# If you do choose to read this file (which we wouldn't recommend), the
# following nomenclature conventions may be helpful:
# * The variable "rule" generally represents a rule, which takes the form
#   "IF(..., THEN(...))".  A rule has an "antecedent" (consisting of one or more
#   "conditions") and a "consequent" (also called an "action" in some places).
# * The variable "data" generally represents a set of "assertions".

import re
from utils import *
try:
    set()
except NameError:
    from sets import Set as set, ImmutableSet as frozenset

try:
    sorted([])
except NameError:
    def sorted(lst):
        new_lst = list(lst)
        new_lst.sort()
        return new_lst

def forward_chain(rules, data, apply_only_one=True, verbose=False):
    """
    Apply a list of IF-expressions (rules) through a set of data (assertions)
    in order.  Return the modified data set that results from the rules.

    Set apply_only_one=True to get the behavior we describe in class. When it's
    False, a rule that fires will do so for _all_ possible bindings of its
    variables at the same time, making the code considerably more efficient.
    If your rules have any NOTs or DELETEs, your results may wildly vary based
    on the value of apply_only_one; otherwise, the results will be the same.
    """
    old_data = ()

    while set(old_data) != set(data):
        old_data = list(data)
        for rule in rules:
            data = rule.apply(data, apply_only_one, verbose)
            if set(data) != set(old_data):
                break

    return data

def instantiate(template, values_dict):
    """
    Given an expression ('template') with variables in it,
    replace those variables with values from values_dict.

    For example:
    >>> instantiate("sister (?x) {?y)", {'x': 'Lisa', 'y': 'Bart'})
    => "sister Lisa Bart"
    """
    if (isinstance(template, AND) or isinstance(template, OR) or
        isinstance(template, NOT)):

        return template.__class__(*[populate(x, values_dict)
                                    for x in template])
    elif isinstance(template, str):
        return AIStringToPyTemplate(template) % values_dict
    else: raise ValueError("Don't know how to populate a %s" % \
      type(template))

# alternate name for instantiate
populate = instantiate

def match(template, AIStr):
    """
    Given two strings, 'template': a string containing variables
    of the form '(?x)', and 'AIStr': a string that 'template'
    matches, with certain variable substitutions.

    Returns a dictionary of the set of variables that would need
    to be substituted into template in order to make it equal to
    AIStr, or None if no such set exists.
    """
    try:
        return re.match( AIStringToRegex(template),
                         AIStr ).groupdict()
    except AttributeError: # The re.match() expression probably
                           # just returned None
        return None

def is_variable(str):
    """Is 'str' a variable, of the form '(?x)'?"""
    return isinstance(str, str) and str[0] == '(' and \
      str[-1] == ')' and re.search( AIStringToRegex(str) )

def variables(exp):
    """
    Return a dictionary containing the names of all variables in
    'exp' as keys, or None if there are no such variables.
    """
    try:
        return re.search( AIStringToRegex(exp).groupdict() )
    except AttributeError: # The re.match() expression probably
                           # just returned None
        return None

class IF(object):
    """
    A conditional rule.

    This should have the form IF( antecedent, THEN(consequent) ),
    or IF( antecedent, THEN(consequent), DELETE(delete_clause) ).

    The antecedent is an expression or AND/OR tree with variables
    in it, determining under what conditions the rule can fire.

    The consequent is an expression or list of expressions that
    will be added when the rule fires. Variables can be filled in
    from the antecedent.

    The delete_clause is an expression or list of expressions
    that will be deleted when the rule fires. Again, variables
    can be filled in from the antecedent.
    """
    def __init__(self, conditional, action = None,
                 delete_clause = ()):
        # Deal with an edge case imposed by type_encode()
        if type(conditional) == list and action == None:
            return self.__init__(*conditional)

        # Allow 'action' to be either a single string or an
        # iterable list of strings
        if isinstance(action, str):
            action = [ action ]

        self._conditional = conditional
        self._action = action
        self._delete_clause = delete_clause

    def apply(self, data, apply_only_one, verbose):
        """
        Return a new set of data updated by the conditions and
        actions of this IF statement.

        If 'apply_only_one' is True, after adding one datum,
        return immediately instead of continuing. This is the
        behavior described in class, but it is slower.
        """
        verbose = int(verbose) # False -> 0, True -> 1

        new_data = data[:] # Preserve ordering of data to get bindings!
        old_data_count = len(new_data) #original number of assertions
        bindings = list(RuleExpression().test_term_matches(self._conditional,
                                                      new_data))
        if len(bindings) > 0 and verbose >= 2:
            print("Rule matches: {}".format(self))

        new_data = list(new_data)
        new_data_set = set(new_data)
        for k in bindings:
            rule_fired = False
            if verbose >= 2:
                print(" {}".format(k))
            for a in self._action:
                new_datum = populate(a, k)
                new_data_set.add(new_datum)
                if len(new_data_set) != old_data_count:
                    new_data.append(new_datum)
                    old_data_count = len(new_data_set) #update old_data_count
                    rule_fired = True
                    if verbose >= 1:
                        if verbose <= 1: print("Rule: {}".format(self))
                        print("  Added assertion: {}".format(new_datum))
                else:
                    if verbose >= 2:
                        print("  Assertion is already present: {}".format(new_datum))
            for d in self._delete_clause:
                try:
                    delete_datum = populate(d, k)
                    new_data_set.remove(delete_datum) # Throws KeyError if failure
                    new_data.append(new_datum)
                    old_data_count = len(new_data_set) #update old_data_count
                    rule_fired = True
                    if verbose >= 1:
                        if verbose <= 1: print("Rule: {}".format(self))
                        print("  Deleted assertion: {}".format(delete_datum))
                except KeyError:
                    if verbose >= 2:
                        print("  Assertion doesn't exist, so it was not deleted: {}".format(new_datum))
            if apply_only_one and rule_fired:
                return tuple(new_data)

        return tuple(new_data)

    def __str__(self):
        if self._delete_clause == ():
            return "IF({}, {})".format( self._conditional,
                                        self._action)
        else:
            return "IF({}, {}, {})".format( self._conditional,
                                            self._action,
                                            self._delete_clause)

    def antecedent(self):
        return self._conditional

    def consequent(self):
        # Note that while _conditional points to a string, an AND, or an OR;
        #  _action points to a THEN(___) instead of just the ___. From a data
        #  science perspective this may be correct, but from a semantic standpoint
        #  this wouldn't hold up in court: After all, in "IF P, THEN Q", P is 
        #  the antecedent, not "IF P". So why should "THEN Q" be labeled as the
        #  consequent? Anyway, because in this lab, all antecedents are single
        #  items, just return _action[0] instead of _action as the consequent.
        return self._action[0]

    __repr__ = __str__

class RuleExpression(list):
    """
    The parent class of AND, OR, and NOT expressions.

    Just like Sums and Products from lab 0, RuleExpressions act
    like lists wherever possible. For convenience, you can leave
    out the brackets when initializing them: AND([1, 2, 3]) == AND(1, 2, 3).
    """
    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], list)
            and not isinstance(args[0], RuleExpression)):
            args = args[0]
        list.__init__(self, args)

    def conditions(self):
        """
        Return the conditions contained by this RuleExpression.
        This is the same as converting it to a list.
        """
        return list(self)

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join([repr(x) for x in self]) )

    __repr__ = __str__

    def test_term_matches(self, condition, data, context_so_far = None):
        """
        Given an condition (which might be just a string), check
        it against the data (assertions).
        """
        data = list(data)
        if context_so_far == None: context_so_far = {}

        # Deal with nesting first
        # If we're a nested term, we already have a test function; use it
        if not isinstance(condition, str):
            return condition.test_matches(data, context_so_far)

        # basestring case
        else:
            return self.basecase_bindings(condition, data, context_so_far)

    def basecase_bindings(self, condition, data, context_so_far):
        for assertion in data:
            bindings = match(condition, assertion)
            if bindings is None: continue
            try:
                context = NoClobberDict(context_so_far)
                context.update(bindings)
                yield context
            except ClobberedDictKey:
                pass

    def get_condition_vars(self):
        if hasattr(self, '_condition_vars'):
            return self._condition_vars

        condition_vars = set()

        for condition in self:
            if isinstance(condition, RuleExpression):
                condition_vars |= condition.get_condition_vars()
            else:
                condition_vars |= AIStringVars(condition)

        return condition_vars

    def test_matches(self, data, context_so_far=None):
        raise NotImplementedError

    def __eq__(self, other):
        return type(self) == type(other) and list.__eq__(self, other)

    def __hash__(self):
        return hash((self.__class__.__name__, list(self)))

class AND(RuleExpression):
    """A conjunction of patterns, all of which must match."""
    class FailMatchException(Exception):
        pass

    def test_matches(self, data, context_so_far=None):
        if context_so_far == None: context_so_far = {}
        return self._test_matches_iter(data, list(self))

    def _test_matches_iter(self, data, conditions=None, cumulative_dict=None):
        """
        Recursively generate all possible matches.
        """
        # Set default values for variables.  We can't set these
        # in the function header because values defined there are
        # class-local, and we need these to be reinitialized on
        # each function call.
        if cumulative_dict == None:
            cumulative_dict = NoClobberDict()

        # If we have no more conditions to analyze, pass the
        # dictionary that we've accumulated back up the
        # function-call stack.
        if len(conditions) == 0:
            yield cumulative_dict
            return

        # Recursive Case
        condition = conditions[0]
        for bindings in self.test_term_matches(condition, data,
                                               cumulative_dict):
            bindings = NoClobberDict(bindings)

            try:
                bindings.update(cumulative_dict)
                for bindings2 in self._test_matches_iter(data, conditions[1:],
                                                         bindings):
                    yield bindings2
            except ClobberedDictKey:
                pass


class OR(RuleExpression):
    """A disjunction of patterns, one of which must match."""
    def test_matches(self, data, context_so_far = {}):
        for condition in self:
            for bindings in self.test_term_matches(condition, data):
                yield bindings

class NOT(RuleExpression):
    """A RuleExpression for negation. A NOT clause must only have
    one part."""
    def test_matches(self, data, context_so_far=None):
        if context_so_far == None: context_so_far = {}
        assert len(self) == 1 # We're unary; we can only process one condition

        try:
            new_key = populate(self[0], context_so_far)
        except KeyError:
            new_key = self[0]

        matched = False
        for x in self.test_term_matches(new_key, data):
            matched = True

        if matched:
            return
        else:
            yield NoClobberDict()


class THEN(list):
    """
    A THEN expression is a container with no interesting semantics.
    """
    def __init__(self, *args):
        if (len(args) == 1 and isinstance(args[0], list)
            and not isinstance(args[0], RuleExpression)):
            args = args[0]
        super(list, self).__init__()
        for a in args:
            self.append(a)

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([repr(x) for x in self]) )

    __repr__ = __str__


class DELETE(THEN):
    """
    A DELETE expression is a container with no interesting
    semantics. That's why it's exactly the same as THEN.
    """
    pass

def uniq(lst):
    """
    this is like list(set(lst)) except that it gets around
    unhashability by stringifying everything.  If str(a) ==
    str(b) then this will get rid of one of them.
    """
    seen = {}
    result = []
    for item in lst:
        if str(item) not in seen:
            result.append(item)
            seen[str(item)]=True
    return result

def simplify(node):
    """
    Given an AND/OR tree, reduce it to a canonical, simplified
    form, as described in the lab.

    You should do this to the expressions you produce by backward
    chaining.
    """
    if not isinstance(node, RuleExpression): return node
    branches = uniq([simplify(x) for x in node])
    if isinstance(node, AND):
        return _reduce_singletons(_simplify_and(branches))
    elif isinstance(node, OR):
        return _reduce_singletons(_simplify_or(branches))
    else: return node

def _reduce_singletons(node):
    if not isinstance(node, RuleExpression): return node
    if len(node) == 1: return node[0]
    return node

def _simplify_and(branches):
    for b in branches:
        if b == FAIL: return FAIL
    pieces = []
    for branch in branches:
        if isinstance(branch, AND): pieces.extend(branch)
        else: pieces.append(branch)
    return AND(*pieces)

def _simplify_or(branches):
    for b in branches:
        if b == PASS: return PASS
    pieces = []
    for branch in branches:
        if isinstance(branch, OR): pieces.extend(branch)
        else: pieces.append(branch)
    return OR(*pieces)

PASS = AND()
FAIL = OR()
run_conditions = forward_chain

# Pretty printer for a goal tree
def pretty_goal_tree(tree, ind=0, use_ind=False, end="\n"):
    net_ind = ind if use_ind else 0
    # print("Test: " + str(tree))
    if isinstance(tree, AND) or isinstance(tree, OR):
        class_name = tree.__class__.__name__

        # Print out header like "AND ("
        unindented_header = "{}( ".format(class_name, ind)
        indented_header = (net_ind * " ") + unindented_header
        pretty_goal_tree(indented_header, ind, False, end="")
       
        # Indentation of children
        sub_ind = ind + len(unindented_header)

        conditions = list(tree) 
        if conditions == []:
            pretty_goal_tree(" )", ind, False)
            return

        # Recursive step 
        if len(conditions) == 1:
            pretty_goal_tree(conditions[0], sub_ind, False, end="")
            pretty_goal_tree(" )", sub_ind, False, end=end)
        elif len(conditions) == 2:
            pretty_goal_tree(conditions[0], sub_ind, False)
            pretty_goal_tree(conditions[1], sub_ind, True, end="")
            pretty_goal_tree(" )", sub_ind, False, end=end)
        else:
            pretty_goal_tree(conditions[0], sub_ind, False)
            for cond in conditions[1:-1]:
                pretty_goal_tree(cond, sub_ind, True)
            pretty_goal_tree(conditions[-1], sub_ind, True, end="")
            pretty_goal_tree(" )", sub_ind, False, end=end)
    else:
        # Print the string
        print((net_ind * " ") + str(tree), end=end)
