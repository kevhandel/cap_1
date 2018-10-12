<img src="/figs/EPA.png"><br>
### The Toxic Release Inventory (TRI)
Contains EPA Data on Chemical Fates within US Industry
<p>&nbsp;

### Motivation and Background...

The United States Environmental Protection Agency (EPA) is charged with keepong our air, the waterways, and
ground free from harmful chemicals.   The Agency maintains a database which contains the "fate" of industrial
chemicals in use by US-based companies, so that we might better track the whereabouts of those which are
potentially harmful.

* Data on the amounts of each chemical traveling in any of the 60+ streams are delivered through self-reporting.
* Complete sets are available for years 1987 - 2016, inclusive.

The publicly-available repository contains over 6 million records on 600 unique chemicals traversing various pathways.
While the data are highly organized, the overlap of certain categories, some of which combine multiple
fates, and the emergence of new fates that did not appear in the earlier reports, does allow for obfuscation.

Plenty of ponderables served to motivate this study, such as:
* Do fates of chemicals predictable and reliably evolve over time?
* Can identified trends be correlated with enhanced Federal and/or local environmental regulations?  Might we become able to better predict the effect of future proposed regulation?
* Is the early data detectably padded due to the very lax reporting standards
which, anecdotally, resulted in over-reporting of certain hazardous chemicals?
* Are trends toward more society-wide recycling apparent in industry as well?

The primary goal was to plot a few fates of select chemicals in order to test for industry-wide evolution in chemical fate.
Quantification would involve Hypothesis Testing.

As the database contains no information regarding environmental regulation, regression testing to model the effects
of regulations would require merging this data with a secondary regulations database.
<p>&nbsp;

### Investigation...

The primary data source is the <a href="https://www.epa.gov/toxics-release-inventory-tri-program"> EPA's own website. </a>
A single csv contains all of the records.
A <a href="https://www.kaggle.com/epa/toxic-release-inventory">secondary copy</a> is housed on <a href="http://kaggle.com">Kaggle.com</a>,
where the records are housed in 29 separate files and sorted by calendar year.

Data was downloaded from both sites.  However, the csv file from the EPA site was corrupted, and when imported as a Pandas dataframe, did not reliably
return complete records.
As an alternative, we reconstructed a single database by merging all of the Kaggle files as individual Pandas dataframes, and saving this object in a
single csv file. Data values were maintained in their present form throughout the project.
At nearly one GB in size, the single file was far too massive to manage; we addressed the following issues while reorganizing the data:
* We shrunk the data by dropping 39 of the 109 columns that dealt with company info, EPA-specific chemical classification, or other EPA
geographical site-related information.  We kept all of the numeric columns associated with chemical fate.
* We found many rows with NaN values.  As these appeared to exist due to the expansion in the reporting options from original conception,
no data imputation was warranted at the early stage of exploration.
We then split the dataframe into 613 dataframes each of which housed the data for a unique chemical, and stored these as csv files.
* Each dataframe contained the 66 columns related to fate, and the file names were coded according to chemical name, which meant that the future process of querying any given chemical could be fairly well automated.  A lookup function initially queried the monster file for chemical names, and then stored these in a separate tiny file to be accessed at the startup of each session.
<p>&nbsp;

### Start the EDA...
<table>
<tr><td align="center">Some of the 630 chemicals<br><p>
<img src="/figs/ind_chem_long_jn.png" alt = "chemical in TRI" height="420" width="200"></td>
<td align="center">New individual csv files<br><p>
<img src="/figs/ind_chems.png" alt="chemical file names" height="200" width="200">
<p><p>
<img src="/figs/fates.png" alt="chemical fates" height="200" width="200">
<br>Fate classifcations
</td></tr>
<tr><td colspan=2 align="center"><center>Cross section of fate data for Benzene</center><br><p>
<img src="/figs/benzene_df.png" alt="Benzene data" height="280" width="500">
</td></tr>
<tr><td colspan="2" align="center">
<img src="/figs/chems.png" alt="all chemicals" height="240" width="400">
</td></tr>
</table>

<p>&nbsp;

### Graphing by the 1000's...
<table>
<tr><td align="center">A few graphs showing fate over time<br><p>
<img src="/figs/fig_chemicals_BENZENE_ON-SITE_RELEASE_TOTAL.png" alt = "Benzene on site release" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_BENZENE_TOTAL_RELEASES.png" alt = "Benzene total fig_chemicals_BENZENE_TOTAL_RELEASES" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_CREOSOTE_8.4_RECYCLING_ON-SITE.png" alt = "Creosote recycling on-site" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_ETHYLENE_5.1_FUGITIVE_AIR.png" alt = "Ethylene in air" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_METHANOL_5.1_FUGITIVE_AIR.png" alt = "Methanol in air" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_METHYL_ETHYL_KETONE_5.1_FUGITIVE_AIR.png" alt = "MEK in air" height="300" width="500"></td>
</tr><tr><td align="center">
<img src="/figs/fig_chemicals_TOLUENE_5.1_FUGITIVE_AIR.png" alt = "Toluene in air" height="300" width="500"></td>
</tr></table>

<p>&nbsp;

### Gathering Data...

To test the proposed hypothesis, "Fates of chemicals do not change over time across US industry",
we next sought to gather fate data for the compelling case of FUGITIVE AIR emissions, which
appeared to be diminishing over time, especially for volatile chemicals.  We divided the emissions
data for this fate into two temporal groupings: 1987-2001 and 2002-2016.

The next distribution graph of emission amounts would demonstrate that an effect is worthy of investigating emperically.

Had this worked well, we could select other fates and attempt to discover which ones change over time.

<p>&nbsp;

### Results...
The data are interesting in that emission fates exhibit marked variability over time for many of the chemicals.
However, without numerical analysis, we cannot test the data using regression models in an attempt to
ascertain true correlation between the various fates.
<p>&nbsp;

### Looking Ahead...
We certainly know that the chemical fate numbers in this database are intrinsically related since the database is
affords a complete accounting for the measured chemicals.  If one fate decreased as a percentage of the the total,
then one or more others must compensate.  Further, there may be correlation with outside forces, such as Environmental
regulations.  We may be able to develop a model that predicts the change in fates based upon regulation, for instance.

<p>&nbsp;

### Data Sources...
The US EPA maintains the TRI database.<br>
Kaggle.com maintains a copy of the original.<br>
With gratitude, we accessed both.
