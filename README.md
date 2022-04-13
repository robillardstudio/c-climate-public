![installation detail](media/ccm.jpg)

Critical Climate Machine
========================

Gaëtan Robillard, installation repository, 2022.

Critical Climate Machine (Patterns of Heat) is a research based project that quantifies and reveals the mechanisms of online misinformation about global warming.

This code has been developed by Gaëtan Robillard and Jolan Goulin, as part of the project [MediaFutures](#mediafutures) and [»The Intelligent Museum«](#the-intelligent-museum).

Description
-----------

The project consists of a data sculpture based on machine learning algorithms, a visualization and a sound installation. Made with wood and copper, the data sculpture is composed by a network of thirty two units, each embedding one processor (pi zero wifi) displaying outputs on a row of 7 segments LED displays (56 digits per row). A main device (pi 4) runs the collection of data from Twitter and reads and writes the data on a Data Base. This repository concerns the code for the data sculpture.

### Structure

Three main modules compose the current architecture:

1. `/claim_monitor`, on main device
2. `/machine_learning`, on a network of pi zero devices
3. `scenario.py`, on main device

The scenario and the claim monitor are connected to a mongoDB database.

`start.sh` is a bash script for autorun of `claim_monitor/cl_monitor.py` on main device.

### 1. Claim monitor

*Runs on main device*

The module watches Twitter accounts for recent tweets and saves them in the Data Base.

Use `cl_monitor.py` to:

- monitor accounts through Twitter API (Twitter developper account needed)
- writes collected tweets in the DB
- classify most recent tweets from the DB (cf Subroutine)
- writte the classification output as a new attribute in the DB

**Subroutine**

`ml_upd_db.py` is used to classify tweets and write their labels in the DB, by using the trained ML model from `data/model.pkl`. `nTweets` is a variable used to limit for the number of inputs to run through the model.

### 2. Machine learning

*Runs on each raspberry of the network, i.e. 32 units (pi zero)*

For every cycle of the scenario (cf Scenario), each unit receives and classifies 28 new tweets. There are 18 labels ranging from 0 to 17.

Warning: the text below is clearly identified in the realm of cognitive sciences as known misleading claims about climate change. It should be recalled here that **97% of climate experts agree humans are causing global warming.**

![code sheet](media/labels-caption.png)

`server.launch` runs `server.py` at the unit startup. `server.py` receives data and instructions from the main device over wifi network.

See `ml.py` for ML inference and `model.pkl`, the trained model.

### 3. Scenario

*Runs on main device*

The scenario works as a cycle for collecting data from the DB and distributing it in the network.

Use `scenario.py` to:

- connect to the DB
- create a list of 32 sub lists of 28 tweets
- distribute each sublist to 32 IPs, via OSC protocol

**Network**

`network.py` is used to manage the pi zero network (32 servers) from the command line.
Possible inputs are: `update`, `halt`, `reboot`.

Requirements
------------

Dependencies (python librairies)

* scikit-learn
* numpy
* pymongo
* pymongo[srv]
* pickle

Data
-------

### Disclaimer

It was decided to publish here the traning data in csv format. The purpose is to allow the training of the model in case the `model.pkl` can't be read because of possible updates of the scikit-learn librairy. Another reason for our choice relies on the fact that the training data is entirely anonymised. Be aware the training data does not include the test set. For accessing the full dataset and learning about its method, please refer to References below. For any claim regarding the publication of the training data in the current repository, please contact gaetanrobillard.studio@gmail.com.

Path for accessing the training data : `machine_learning/dataset-training/training.csv`

To train the model and export new `.pkl` file, use `trainExportModel.py`.

### Note

Publishing the new twitter data in the Critical Climate Machine framework – in open data – is on its way.

References / Further Reading
----------------------------

Critical Climate Machine [on vimeo](https://vimeo.com/667971904)

Training set and analysis code is extended from article by Travis G. Coan, Constantine Boussalis, John Cook, and Mirjam Nanko, "Computer-assisted classification of contrarian claims about climate change", _Sci Rep 11_, 22320, Nature, 2021. [https://doi.org/10.1038/s41598-021-01714-4](https://doi.org/10.1038/s41598-021-01714-4)

Tips
-----------

Use [cheat-sheet](cheat-sheet.md) to get few tips for debugging the installation.

MediaFutures
--------------

Critical Climate Machine is part of the MediaFutures project. It has received funding from the European Union’s framework Horizon 2020 for
research and innovation programme under grant agreement No 951962.

![logos](media/logos-mediafutures-eu.png)

The Intelligent Museum
----------------------

An artistic-curatorial field of experimentation for deep learning and visitor participation

The [ZKM | Center for Art and Media](https://zkm.de/en) and the [Deutsches Museum Nuremberg](https://www.deutsches-museum.de/en/nuernberg/information/) cooperate with the goal of implementing an AI-supported exhibition. Together with researchers and international artists, new AI-based works of art will be realized during the next four years (2020-2023).  They will be embedded in the AI-supported exhibition in both houses. The Project „The Intelligent Museum” is funded by the Digital Culture Programme of the [Kulturstiftung des Bundes](https://www.kulturstiftung-des-bundes.de/en) (German Federal Cultural Foundation) and funded by the [Beauftragte der Bundesregierung für Kultur und Medien](https://www.bundesregierung.de/breg-de/bundesregierung/staatsministerin-fuer-kultur-und-medien) (Federal Government Commissioner for Culture and the Media).

As part of the project, digital curating will be critically examined using various approaches of digital art. Experimenting with new digital aesthetics and forms of expression enables new museum experiences and thus new ways of museum communication and visitor participation. The museum is transformed to a place of experience and critical exchange.

![Logo](media/Logo_ZKM_DMN_KSB.png)
