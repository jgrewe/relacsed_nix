import nixio

from ...base.repro import ReProRun
from ...utils.mappings import DataType
from ...utils.config import Config


class EfishEphys(ReProRun):
    """Superclass that bundles some common data access methods for electrophysiological data recorded by running one of the relacs/efish plugins.

    It defines methods to get the commonly recorded data and event traces directly. These are the membrane voltage, the spikes, the eod-times, the local and global eod recordings and the stimulus output. It handles the mapping from the trace names in the nix file. E.g. Action potential times (spikes) are often stored in the event traces Spikes or Spikes-1. 
    Some of these name mappings are provided in the ``rlxnix.utils.default_config.json`` file. They can be overwritten by local configurations.

    Any subclass will inherit this functionality.
    """
    pluginset = "efish"
    signals = ["spikes", "membrane voltage", "local eod", "global eod", "eod times", "stimulus"]

    def __init__(self, repro_run: nixio.Tag, traces, relacs_nix_version=1.1):
        super().__init__(repro_run, traces, relacs_nix_version=relacs_nix_version)
        self._config = Config()
        self._signal_trace_map = {}
        self._spike_times = None
        self._get_signal_trace_map()

    def _get_signal_trace_map(self):
        for s in self.signals:
            signal_traces = self._config.trace_configuration(self.pluginset, s)
            if signal_traces is not None:
                for t in self.traces:
                    if t in signal_traces:
                        self._signal_trace_map[s] = t

    def spikes(self, stimulus_index=None, trace_name=None):
        """Return the spike times for the whole repro run or during a certain stimulus presentation.

        Parameters
        ----------
        stimulus_index : int, optional
            The stimulus index. If None, the spikes of the whole repro run will be read from file. By default None.
        trace_name : str, optional
            The name of the spikes event trace, by default None, i.e. try to find the default traces.

        Returns
        -------
        numpy ndarray
            The spike times in seconds. Times are relative to stimulus onset.
        """
        if self._spike_times is not None and stimulus_index is None:
            return self._spike_times
        if trace_name is None:
            trace_name = self._signal_trace_map.get("spikes")
        self._check_trace(trace_name, DataType.Event)

        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)[0]
        else:
            self._spike_times = self.trace_data(trace_name)[0]
            return self._spike_times

    def local_eod(self, stimulus_index=None, trace_name=None):
        """Return the local eod measurement for the whole repro run or during a certain stimulus presentation.

        Parameters
        ----------
        stimulus_index :  int, optional
            The stimulus index. If None, the spikes of the whole repro run will be read from file. By default None.
        trace_name : str, optional
            The name of the spikes event trace, by default None, i.e. will try to read the deafault from the configuration.

        Returns
        -------
        np.ndarray 
            the local eod data
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("local eod")
        self._check_trace(trace_name, data_type=DataType.Continuous)

        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)
        else:
            return self.trace_data(trace_name)

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
            the local eod data
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("global eod")
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

    def membrane_voltage(self, stimulus_index=None, trace_name=None):
        """Returns the membrane potential measurement for the whole repro run or during a certain stimulus presentation.

        Parameters
        ----------
        stimulus_index : int, optional
            The stimulus index. If None, the voltage trace of the whole repro run will be read from file. By default None.
        trace_name : str, optional
            The name of the membrane voltage trace, by default None, i.e. will try the trace specified in the configurations.

        Returns
        -------
        np.ndarray 
            the membrane potential
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("membrane voltage")
        self._check_trace(trace_name, data_type=DataType.Continuous)

        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)
        else:
            return self.trace_data(trace_name)

    def stimulus_output(self, stimulus_index=None, trace_name=None):
        """Returns the recorded stimulus trace for the whole repro run or during a certain stimulus presentation.

        Parameters
        ----------
        stimulus_index : int, optional
            The stimulus index. If None, the stimulus trace of the whole repro run will be read from file. By default None.
        trace_name : str, optional
            The name of the recorded trace, by default None, i.e. use the trace specified in the configurations.

        Returns
        -------
        np.ndarray 
            the stimulus trace
        np.ndarray
            the respective time axis
        """
        if trace_name is None:
            trace_name = self._signal_trace_map.get("stimulus")
        self._check_trace(trace_name, data_type=DataType.Continuous)

        if stimulus_index is not None:
            self._check_stimulus(stimulus_index)
            return self.stimuli[stimulus_index].trace_data(trace_name)
        else:
            return self.trace_data(trace_name)