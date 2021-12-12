# Configurations

One can overwrite the default configurations by providing a local ``config.json`` file that must reside in the same folder from which you run your code.

The default configuration is provided by the ``default_config.json`` file which is located in the ``rlxnix.utils`` package.

```json
{
    "log_level": "WARNING",
    "trace_configs": {
        "efish": {
            "spikes": ["Spikes", "Spikes-1", "Spikes-2"],
            "membrane voltage": ["V", "V-1", "V-2"],
            "global eod": ["EOD"],
            "local eod": ["LocalEOD", "LocalEOD-1", "LocalEOD-2"],
            "eod times": ["EOD events", "EOD_events"],
            "stimulus": ["GlobalEFieldStimulus"],
            "chirps": ["Chirps", "Chirps-1", "Chirps-2"]
        },
        "default": {
            "spikes": ["Spikes", "Spikes-1", "Spikes-2"],
            "membrane voltage": ["V", "V-1", "V-2"],
            "global eod": ["EOD"],
            "local eod": ["LocalEOD", "LocalEOD-1", "LocalEOD-2"]
        }
    }
}
```

So far it only defines two things:

1. The log level.
2. The trace configurations.

Local configurations always supersede the default configurations. Local and default configurations are handled by the ``rlxnix.utils.Config`` class.

## Logging

The log level defines what kind of information will be displayed on the command line. The default configuration sets the log level to "WARNING". That is, you will see issues that are warnings, errors or critical.

Valid settings for the ``log_level`` are ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, and ``DEBUG``.

``DEBUG`` will lead to the most verbose output.

## Trace configurations

The ``trace_configs`` section of the configuration file contains the mapping of signal names (such as "spikes", or "membrane voltage") to lists of trace names that are commonly used in the recording. The mappings are given for each plugin separately. For the moment this is only the ``efish`` plugin.
