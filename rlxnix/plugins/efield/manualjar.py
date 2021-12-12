from rlxnix.base.repro import ReProRun


import nixio

from ...base.repro import ReProRun
from ...utils.mappings import DataType
from ...utils.config import Config

class ManualJar(ReProRun):
    """Class that represents the ManualJAR recording. It provides easy access to the EOD and, if given the eod_times trace and the relevant metadata.
    """
    _repro_name = "ManualJar"
    pluginset = "efield"
    signals = ["eod", "eod times"]

    def __init__(self, repro_run: nixio.Tag, traces, relacs_nix_version=1.1):
        super().__init__(repro_run, traces, relacs_nix_version=relacs_nix_version)
        self._config = Config()
        self._signal_trace_map = {}
        self._get_signal_trace_map()

    def _get_signal_trace_map(self):
        for s in self.signals:
            signal_traces = self._config.trace_configuration(self.pluginset, s)
            if signal_traces is not None:
                for t in self.traces:
                    if t in signal_traces:
                        self._signal_trace_map[s] = t

    def eod(self, stimulus_index=None, trace_name=None):
        """Return the global eod measurement for the whole repro run or during a certain stimulus presentation.

        Parameters
        ----------
        stimulus_index :  int, optional
            The stimulus index. If None, the spikes of the whole repro run will be read from file. By default None.
        trace_name : str, optional
            The name of the spikes event trace, by default None, i.e. will try to read the deafault from the configuration.

        Returns
        -------
        np.ndarray 
            the eod data
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("eod")
        self._check_trace(trace_name, data_type=DataType.Continuous)

        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)
        else:
            return self.trace_data(trace_name)

    def eod_times(self, stimulus_index=None, trace_name=None):
        """Read the EOD times from file. 

        Parameters
        ----------
        stimulus_index : int, optional
            stimulus index by default None
        trace_name : str, optional
            The name of the recorded event trace that stores the EOD times, by default None, i.e. read trace name from configuration file.

        Returns
        -------
        numpy.ndarray
            The EOD times.
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("eod times")
        self._check_trace(trace_name, DataType.Event)
        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)[0]
        else:
            return self.trace_data(trace_name)[0]

    def local_eod(self, stimulus_index=None, trace_name=None):
        """Read the local EOD  from file. 

        Parameters
        ----------
        stimulus_index : int, optional
            stimulus index by default None
        trace_name : str, optional
            The name of the recorded event trace that stores the local EOD recording, by default None, i.e. read trace name from configuration file.

        Returns
        -------
         Returns
        -------
        np.ndarray 
            the local eod data
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("local eod")
        self._check_trace(trace_name, DataType.Continuous)
        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)[0]
        else:
            return self.trace_data(trace_name)[0]
    
    @property
    def frequencies(self):
        """ The absolute frequencies of the stimuli in Hertz.

        Returns
        -------
        freqs: list of floats
            The absolute frequencies of the stimulus presentations in Hertz.
        """
        freqs = [s.metadata[s.name]["Frequency"][0][0] for s in self.stimuli]
        return freqs
