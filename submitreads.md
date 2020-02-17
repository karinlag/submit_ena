# How to submit reads programmatically

Assumptions for this tutorial: a submitter has one or more readsets that they wish to submit. These files are on a linux system, and the user wants to submit them via the linux command line.


## Links and resources

Most of the information in this tutorial is found here:
* [The ENA tutorial](https://ena-docs.readthedocs.io/en/latest/)

To understand more about the relationships between files, see this page describing the data model:
 * [The ENA metadata model](https://ena-docs.readthedocs.io/en/latest/submit/general-guide/metadata.html)

This tutorial suggests using the tools found in this github repository to help with the submission process. Note: this uses python2. If using this script, the "fix_files.py" script in this repository can be used to adjust the name of the files.

* [The Public Health England's submission tools](https://github.com/phe-bioinformatics/ena_submission)

## Brief overview of the process

This process consists of three steps:

1. Transfer the read files to the ENA dropbox.
1. Create XML files that describe the submission.
1. Transfer XML files. With that, the files are submitted.

The fastq files are transferred using FTP to a user specific location on the ENA server.  The XML are transferred using 'curl'. The XML files transferred describe the data being submitted. These files are interlinked by referring to each other in such a way that they, together with the read files, put together a read set submission.

To transfer read and XML files, the person submitting them must have [registered an account at ENA with a username and password](https://ena-docs.readthedocs.io/en/latest/general-guide/registration.html). If the submitter does not have an account at ENA yet, one must be created.

## Fastq read file transfer

Read files can be transferred to ENA using for instance FTP. Data is then put into a user specific area. Users should not expect the data to be there for more than two months.

Before transferring, make sure that the file is zipped and that a checksum file for each file has been made. If using the PHE scripts, this file will be made for you.

A checksum file contains a "number" calculated on the basis of the file content. If the file changes, for instance by not being completely transferred, a checksum can reveal that. A checksum file is a file named fastq.gz.md5, i.e. the full sample filename followed by ".md5". To make a set of md5 checksum files for all files in a directory, do the following:


```bash
for f in *.gz; do md5sum $f > $f.md5; done
```
These links contain more information on how to prepare your files.

* [On how to prep the files](https://ena-docs.readthedocs.io/en/latest/fileprep/preparation.html)

Once the files are prepared, they need to be transferred to ENA. Note: only the fastq files themselves need to be transferred, not the md5 files. For a recipe on how to do that, see the link below. If transferring from a linux system, see the instructions on how to upload using FTP.  

* [On how to transfer fastq files to ENA](https://ena-docs.readthedocs.io/en/latest/fileprep/upload.html)

The file names of the files transferred will be referred to in the read pair Run file, mentioned below.

## XML Files

Once the read files themselves have been transferred, we can now proceed with making the necessary XML files.

A read set submission consists of creating and transferring the following set of [XML](https://en.wikipedia.org/wiki/XML) files:

* Study (project): this is the file that will describe the study, and which will result in a ENA accession number for your reads.
* Sample: a study consists of one or more samples. This file contains sample information. One file can contain information regarding one to many samples.
* Experiment: each sample has been sequenced. This then constitutes an experiment, which is then described in this file. One Experiment file can contain one to many experiments.
* Run: within each experiment, one or more sequencing runs have been done. In most cases, when there is only one pair of fastq files, there will be only one Run per Experiment. If there are more, more Runs  describing each run has to be created. One Run file can contain one to many Runs. This is the file that contains the filenames of the files transferred to the ENA dropbox above.
* Submission: whenever a file (any of the ones mentioned above) is to be transferred to ENA, a file has to accompany it that tells the system on the other side what is to be done with it. This is the role of the submission file.  

When submitting files, ENA recommends to do a test against the test server first. This will check that the files submitted have the right format etc. The web addresses for both can be [found on the ENA pages](https://ena-docs.readthedocs.io/en/latest/general-guide/programmatic.html).


### Creating the necessary files

In this section, the necessary files and their formats are described. Note, these files can contain significantly more information than described here - see the ENA webpages for more information. The minimum versions given here were generously contributed by [@martinghunt](https://github.com/martinghunt) and the [Iqbal lab](https://github.com/iqbal-lab-org). They are also adjusted so as to resemble the output from the PHE scripts mentioned above.

If using the PHE submission scripts, you will need to create the following files (see more on the PHE github pages):
* A comma separated (csv) file containing all the information that you want to submit with your reads. The minimum is sample, taxon_id, scientific name and description. More information can be added here, see below.
* An abstract file that describes your study.

If using the PHE scripts, it is useful to gather these in the directory above the read set.

#### The study file

This is the file that describes what the study in question was. There are some essential pieces of information that is needed to create this one:

* Project alias - a specific tag for this study. Will be used by other entries.
* Title - a name for the project/study.
* Description - a text description of the project/study. This should contain information regarding how many samples are included and a bit about library prep and how they were sequenced.

This is how the file looks:

```
<?xml version="1.0" ?>
<PROJECT_SET>
   <PROJECT alias="project_alias" center_name="center name">
      <TITLE>title text</TITLE>
      <DESCRIPTION>description text</DESCRIPTION>
      <SUBMISSION_PROJECT>
         <SEQUENCING_PROJECT/>
      </SUBMISSION_PROJECT>
   </PROJECT>
</PROJECT_SET>
```

To create the study file using the PHE scripts, you will need the abstract file mentioned above. The command asks for a REFNAME, which is the same as the project alias. Note, the PHE scripts produces a file containing STUDY instead of PROJECT, this is ok.

#### The sample file

This file describes the sample(s) in your read set. This file can contain many sample entries in one file. This is done by having multiple SAMPLE sections in the file. One SAMPLE section begins with the "<SAMPLE...>" tag, and ends with the "</SAMPLE...>" tag.

Some values need to be specified here (per sample):
- Sample alias - a specific tag for this sample. Will be used by other entries.
- Center name - the name of the institution sequencing/submitting the reads (should be the same as above)
- Title - Name for the sample
- Taxon id - NCBI taxonomic identifier for the sample

```
<?xml version="1.0" ?>
<SAMPLE_SET>
   <SAMPLE alias="sample alias" center_name="center name">
      <TITLE>title</TITLE>
      <SAMPLE_NAME>
         <TAXON_ID>42</TAXON_ID>
      </SAMPLE_NAME>
   </SAMPLE>
</SAMPLE_SET>
```
In this XML snippet, other information can also be added as SAMPLE ATTRIBUTEs. Some things that should be considered is to add the isolation year (collection_date) and what it was isolated from (isolation_source). That could then look like this:

```
<?xml version="1.0" ?>
<SAMPLE_SET>
   <SAMPLE alias="sample alias" center_name="center name">
      <TITLE>title</TITLE>
      <SAMPLE_NAME>
         <TAXON_ID>42</TAXON_ID>
      </SAMPLE_NAME>
      <SAMPLE_ATTRIBUTES>
         <SAMPLE_ATTRIBUTE>
            <TAG>collection_date</TAG>
            <VALUE>2016</VALUE>
            <TAG>isolation_source</TAG>
            <VALUE>horse</VALUE>        
         </SAMPLE_ATTRIBUTE>
      </SAMPLE_ATTRIBUTES>
   </SAMPLE>
</SAMPLE_SET>
```
The tags are in this case taken from the [minuimum information required for samples checklist](https://www.ebi.ac.uk/ena/data/view/ERC000011).

If using the PHE scripts, these values are all to be found in the sample information file. I suggest adding collection_date, isolation_source and geographic location. Note, before creating the sample XML file, the checksum file has to be made.

#### The experiment file

An experiment is in this context a library that results in sequences coming from one or multiple lanes (or equivalent) on a sequencing machine. This file contains the necessary information regarding sequencing platform and library protocols. The information needed for this file is the following:

- experiment alias - a name given specifically to this library
- center name - same as above
- title - a name for this library
- study_acc - this is the accession number given to the study submisson above. If not submitted yet, alternatively change "accession" to "refname" and give the alias that was set in the study xml file above
- sample_acc - this is the accession of the sample that this experiment belongs to. If the sample is not submitted yet, the same mechanism of referring to the sample alias by using "refname" instead of "accession" can be used.
- library name - a name for your library
- instrument - this value should refer to the sequencer that was used, [for a list, see this document](https://ena-docs.readthedocs.io/en/latest/reads/webin-cli.html#instrument).
- read length - this value is the length of your reads.

The values mentioned above have to be _replaced_ with values appropriate for the files in question. In addition, some values in the LIBRARY_DESCRIPTOR section have to be specified. These are prefilled in the example file. The documents mentioned below contain information regarding other values that are valid.

* WGS as the Library Strategy means that this is a whole genome sequencing experiment, [for more, see this document](https://www.ebi.ac.uk/ena/submit/reads-library-strategy).
* GENOMIC as the Library Source means that the DNA is genomic, [for more see this document](https://ena-docs.readthedocs.io/en/latest/reads/webin-cli.html#source).
* RANDOM as the Library Selection describes how XXXXXX was done, [for more, see this document](https://ena-docs.readthedocs.io/en/latest/reads/webin-cli.html?highlight=random#selection).
* NOMINAL_LENGTH as the read length.

```
<?xml version="1.0" ?>
<EXPERIMENT_SET>
   <EXPERIMENT alias="experiment alias" center_name="center name">
      <TITLE>title</TITLE>
      <STUDY_REF accession="study_acc"/>
      <DESIGN>
         <DESIGN_DESCRIPTION/>
         <SAMPLE_DESCRIPTOR accession="sample_acc"/>
         <LIBRARY_DESCRIPTOR>
            <LIBRARY_NAME>library name</LIBRARY_NAME>
            <LIBRARY_STRATEGY>WGS</LIBRARY_STRATEGY>
            <LIBRARY_SOURCE>GENOMIC</LIBRARY_SOURCE>
            <LIBRARY_SELECTION>RANDOM</LIBRARY_SELECTION>
            <LIBRARY_LAYOUT>
               <PAIRED NOMINAL_LENGTH="200"/>
            </LIBRARY_LAYOUT>
         </LIBRARY_DESCRIPTOR>
      </DESIGN>
      <PLATFORM>
         <platform>
            <INSTRUMENT_MODEL>instrument</INSTRUMENT_MODEL>
         </platform>
      </PLATFORM>
      <EXPERIMENT_ATTRIBUTES>
         <EXPERIMENT_ATTRIBUTE>
            <TAG>spam</TAG>
            <VALUE>eggs</VALUE>
         </EXPERIMENT_ATTRIBUTE>
      </EXPERIMENT_ATTRIBUTES>
   </EXPERIMENT>
</EXPERIMENT_SET>

```

As shown above, experiment attributes can also be added, in the same way as described for SAMPLE ATTRIBUTEs above. These are however not mandatory.

If using the PHE scripts, options such as read length etc can be set on the command line.


#### The run file

The run file is the one that actually describes the read files themselves. This is the file that will contain the filename and the checksum for each file. The fields that are needed here are:
- run alias - a name given specifically to this run
- experiment_ref - this is the accession number/alias given to the experiment which these read files are a result of
- center name - the name of the institution submitting the reads
- checksum - checksum for the file that is mentioned in the same FILE section
- filename - name of the read file

Note> the file name has to be exactly the same as it is in the ENA dropbox. I.e. no directory names.  


```
<?xml version='1.0' encoding='utf-8'?>
<RUN_SET>
  <RUN alias="run alias" center_name="center name">
    <EXPERIMENT_REF refname="experiment alias" />
    <DATA_BLOCK>
      <FILES>
        <FILE checksum="6e2e640ad49b063d54c145ecc33b34e3" checksum_method="MD5" filename="filename" />
        <FILE checksum="d281ac18e3769baf03b2d2139376422f" checksum_method="MD5" filename="filename" />
      </FILES>
    </DATA_BLOCK>
  </RUN>
</RUN_SET>
```

If using the PHE scripts, the script will itself find the checksums and put them into the file with the filenames. Note: if running this on a directory with the read files in them, the directory name is in the filename. These will then have to be removed before submittal.


#### The submit file

Last but not least, the submit file. Whenever an XML file is transferred to ENA, we have to tell them what to do with them. In case we are adding a new submission, with the file set created above, this file will consist of a list of references to the files we have made above. This file and the others can then be transferred to ENA, and submission is complete. Note: first test this against the test server to ensure that everything is correct before transferring to the production server.


```
<?xml version='1.0' encoding='utf-8'?>
<SUBMISSION_SET>
  <SUBMISSION alias="study alias" center_name="center name">
    <ACTIONS>
      <ACTION>
        <ADD schema="study" source="study.xml" />
      </ACTION>
      <ACTION>
        <ADD schema="sample" source="sample.xml" />
      </ACTION>
      <ACTION>
        <ADD schema="experiment" source="experiment.xml" />
      </ACTION>
      <ACTION>
        <ADD schema="run" source="run.xml" />
      </ACTION>
      <ACTION>
        <HOLD />
      </ACTION>
    </ACTIONS>
  </SUBMISSION>
</SUBMISSION_SET>
```

This website explains how to submit the XML files.

* [How to submit the XML files](https://ena-docs.readthedocs.io/en/latest/submit/analyses/programmatic.html#submit-the-xmls-using-curl)
