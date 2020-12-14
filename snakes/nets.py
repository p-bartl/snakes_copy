




class PetriNet (object) :
    """A Petri net. As soon as nodes are added to a `PetriNet`, they
    should be handled by name instead of by the `Place` or
    `Transition` instance. For instance:
    >>> n = PetriNet('N')
    >>> t = Transition('t')
    >>> n.add_transition(t)
    >>> n.has_transition('t') # use 't' and not t
    True
    >>> n.transition('t') is t
    True
    """
    def __init__ (self, name) :
        """Initialise with a name that may be an arbitrary string.
        >>> PetriNet('N')
        PetriNet('N')
        @param name: the name of the net
        @type name: `str`
        """
        self.name = name
        self._trans = {}
        self._place = {}
        self._node = {}
        self._declare = []
        self.globals = Evaluator()


#_________________________________________________________________

    def add_place (self, place) :
        """Add a place to the net. Each node in a net must have a name
        unique to this net, which is checked when it is added.
        >>> n = PetriNet('N')
        >>> n.place('p')
        Traceback (most recent call last):
          ...
        ConstraintError: place 'p' not found
        >>> n.add_place(Place('p', range(3)))
        >>> n.place('p')
        Place('p', MultiSet([...]), tAll)
        >>> n.place('p').tokens == MultiSet([0, 1, 2])
        True
        >>> n.add_place(Place('p'))
        Traceback (most recent call last):
          ...
        ConstraintError: place 'p' exists
        @param place: the place to add
        @type place: `Place`
        @raise ConstraintError: when a place with the same name exists
            already in the net
        """
        if place.name in self._place :
            raise ConstraintError("place '%s' exists" % place.name)
        elif place.name in self._trans :
            raise ConstraintError("a transition '%s' exists" % place.name)
        self._place[place.name] = place
        self._node[place.name] = place
        place.lock("name", self, place.name)
        place.lock("net", self, self)
        place.lock("pre", self, {})
        place.lock("post", self, {})

#________________________________________________________________________________

    def add_transition (self, trans) :
        """Add a transition to the net. Each node in a net must have a
        name unique to this net, which is checked when it is added.
        >>> n = PetriNet('N')
        >>> n.transition('t')
        Traceback (most recent call last):
          ...
        ConstraintError: transition 't' not found
        >>> n.add_transition(Transition('t', Expression('x==1')))
        >>> n.transition('t')
        Transition('t', Expression('x==1'))
        >>> n.add_transition(Transition('t'))
        Traceback (most recent call last):
          ...
        ConstraintError: transition 't' exists
        @param trans: the transition to add
        @type trans: `Transition`
        @raise ConstraintError: when a transition with the same name
            exists already in the net
        """
        if trans.name in self._trans :
            raise ConstraintError("transition '%s' exists" % trans.name)
        elif trans.name in self._place :
            raise ConstraintError("a place '%s' exists" % trans.name)
        self._trans[trans.name] = trans
        self._node[trans.name] = trans
        trans.lock("name", self, trans.name)
        trans.lock("net", self, self)
        trans.lock("pre", self, {})
        trans.lock("post", self, {})
        trans.guard.globals.attach(self.globals)
