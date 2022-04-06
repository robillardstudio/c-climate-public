![installation detail](ccm.jpg)

Critical Climate Machine
========================

Gaëtan Robillard, installation repository, 2022.

Critical Climate Machine is a research based project that quantifies and reveals the mechanisms of online misinformation about global warming. The project consists of a data sculpture based on machine learning algorithms, a visualization and a sound installation. Made with wood and copper, the data sculpture is composed by a network of thirty two units, each embedding one processor (pi zero) connected to a row of 7 segments LED displays (56 units per row). This repository concerns the code for the data sculpture and the visualization, which itself is dipslayed on a HD screen.

This code has been developed by Gaëtan Robillard and Jolan Goulin, as part of the project [MediaFutures](#mediafutures) and [»The Intelligent Museum«, ZKM](#the-intelligent-museum).

Training set and analysis code is extended from article by Travis G. Coan, Constantine Boussalis, John Cook, and Mirjam Nanko, "Computer-assisted classification of contrarian claims about climate change", _Sci Rep 11_, 22320, Nature, 2021. [https://doi.org/10.1038/s41598-021-01714-4](https://doi.org/10.1038/s41598-021-01714-4)

--------------------------------------------------------

Updates

- Specifications about the modification of code
- Disclaimer about training dataset
- Footers (IM residency and MediaFutures)

--------------------------------------------------------

Description
-----------

_Detailed project description. Don't forget to include relevant attribution for forked, adapted, or inspired projects._

## Structure

Three main modules compose the current architecture:

1. `scenario.py`, on main device (pi 4)
2. `/claim_monitor`, on main device
3. `/machine_learning`, on a network of pi zero devices

The scenario and the claim monitor are connected to a mongoDB database.

start.sh is a bash script for autorun of claim monitor on main device.

## 1. Scenario

*Runs on main device, e.g. pi4*

The scenario works as a cycle for collecting data from the database (DB) and distributing it in the network.

Use scenario.py to:

- connect to the DB
- create a list of 32 sub lists of 28 tweets
- distribute each sublist to 32 IPs, via OSC protocol

**network.py is used to manage the pi zero network (32 servers) from the command line.**
Possible inputs are: `update`, `halt`, `reboot`

## 2. Claim monitor

*Runs on main device, e.g. pi4*

The module watches Twitter accounts for recent tweets and saves them in the database.

Use cl_monitor.py to:

- monitor accounts through Twitter API (Twitter developper account needed)
- writes found tweets in the DB
- classify most recent tweets in the DB

db.py is used to compare found tweets to existing entries in DB. cl_monitor.py updates the DB only when necessary.

ml_upd_db.py is used to classify tweets and write their labels on the DB, by using the ML algorithm Cards.

## 3. Machine learning

*Runs on each raspberry of the network, i.e. 32 pi0w*

For every cycle of the scenario, the server receives and classifies 28 tweets.

It uses ml.py for inference with Cards. 

server.launch executes server.py at each startup.

## Others

Use [cheat-sheet](cheat-sheet.md) to for few tips for debugging the installation

### Another module is being developped: Consult

A module for creating statistics from the data base:

- number of tweets in the last 24h, according to misinformation label
- total number of tweets in the data base, according to misinformation label

--------------------------------------------------------

Critical Climate Machine is part of the MediaFutures project. It has received funding from the European Union’s framework Horizon 2020 for
research and innovation programme under grant agreement No 951962.
Critical Climate Machine – Patterns of Heat is an artistic research within the framework of the Intelligent Museum Residency, Hertz Lab, ZKM
Center for Art and Media Karlsruhe.
