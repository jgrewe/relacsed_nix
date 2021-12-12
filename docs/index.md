# The **rlxnix** package

Library for reading [relacs](https://relacs.net)-flavoured [NIX](https://github.com/g-node/nix) files.

## A brief intro

[**relacs**](https://relacs.net) is used to record data and put out stimuli in the context of electrophysiological experiments. It is highly configurable and flexible. What it does is controlled in so-called "**Re**search**Pro**tokols" (RePro). These RePros are organized as **Pluginsets**. Whenever a RePro is active, it will dump continuously sampled and/or event **traces** along with all metadata it knows to file. It may or may not control the stimulation of the recorded system. Usually, the settings of a RePro (the **metadata**) completely define its behavior. In the extreme, however, the stimulus that the RePro puts out changes dynamically depending on the neuronal responses and may vary from trial to trial. Therefore a very flexible storage approach is needed and the generic nature of the [NIX](https://github.com/g-node/nix) data model is well suited for this but, otoh, being generic and flexible makes it a little more demanding to read the data.

**rlxnix** simplifies reading of the data from nix files and smooths some edges of a generic data storage. In the context of **NIX** we would say that **rlxnix** is a high-level API for reading relacs-flavoured nix files.

## Further resources

Sources on [GitHub](https://github.com/relacs/relacsed_nix)

[License](https://github.com/relacs/relacsed_nix/blob/master/LICENSE.md)
