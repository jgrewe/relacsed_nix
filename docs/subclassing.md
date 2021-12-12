# Creating your own ReProRun Class

The ``rlxnix.base.repro.ReProRun`` class represents a single run of a relacs RePro. This RePro runs with a given parametrization and may or may not put out stimuli to drive the recorded neuron. What a RePro does is unknown to ``rlxnix`` so the respective ``rlxnix.base.repro.ReProRun`` class provides a generic way for accessing data and metadata.

relacs RePros are tailored for a certain type of experiment. They are assorted into plugin sets. Those, that are of particular importance for us (at least at the moment), are the *efish* and *efield* plugins.

The submodule ``rlxnix.plugins.efish`` currently contains modules specifically adapted to provide easier access to the data and metadata stored by the RePros of some of the efish plugin set. If you want to write your own class for one of the RePros for which ``rlxnix`` does not have an equivalent you need to subclass ``rlxnix.base.repro.ReProRun``.

## Important

When subclassing ``rlxnix.base.repro.ReRroRun`` there are a few things to take care of:

1. Make sure, that the respective ``__init__.py`` (e.g. the one in the ``rlxnix.plugins.efish`` module) imports your class. Otherwise rlxnix will not find it and the default ``ReProRun`` class will be used.
2. If you create a new ``rlxnix.plugins`` submodule make sure to import it in the ``rlxnix.plugins.__init__.py`` file.
3. **Do not overwrite** the ``ReProRun.start_time``, ``ReProRun.stop_time``, and ``ReProRun.duration`` in your class. These properties are essential to find the stimuli that belong to the repro run.
