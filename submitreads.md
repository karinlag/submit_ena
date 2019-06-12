# How to submit reads programmatically

Assumptions for this tutorial: a submitter has one or more readsets that they wish to submit. These files are on a linux system, and the user wants to submit them via the linux command line.


## Links and resources

Most of the information in this tutorial is found here:
* [The ENA tutorial](https://ena-docs.readthedocs.io/en/latest/)

To understand more about the relationships between files, see this page describing the data model:
 * [The ENA metadata model](https://ena-docs.readthedocs.io/en/latest/reads.html)

## Brief overview of the process

This process consists of three steps:

1. Transfer the read files to the ENA dropbox.
1. Create XML files that describe the submission.
1. Transfer XML files. With that, the files are submitted.

The fastq files are transferred using FTP to a user specific location on the ENA server.  The XML are transferred using 'curl'. The XML files transferred describe the data being submitted. These files are interlinked by referring to each other in such a way that they, together with the read files, put together a read set submission.

To transfer read and XML files, the person submitting them must have [registered an account at ENA with a username and password](https://ena-docs.readthedocs.io/en/latest/general-guide/registration.html).

## Fastq read file transfer

Read files can be transferred to ENA using for instance FTP. Data is then put into a user specific area. Users should not expect the data to be there for more than two months.

Before transferring, make sure that the file is zipped and that a checksum file for each file has been made. A checksum file contains a "number" calculated on the basis of the file content. If the file changes, for instance by not being completely transferred, a checksum can reveal that. A checksum file is a file named fastq.gz.md5, i.e. the full sample filename followed by ".md5". To make a set of md5 checksum files for all files in a directory, do the following:

```bash
for f in *.gz; do md5sum $f > $f.md5; done
```

* [On how to prep the files](https://ena-docs.readthedocs.io/en/latest/fileprep/preparation.html)

* [On how to transfer fastq files to ENA](https://ena-docs.readthedocs.io/en/latest/fileprep/upload.html)

The file names of the files transferred will be referred to in the read pair Run file, mentioned below.

## XML Files
A read set submission consists of creating and transferring the following set of [XML](https://en.wikipedia.org/wiki/XML) files:

* Study (project): this is the file that will describe the study, and which will result in a ENA accession number for your reads.
* Sample: a study consists of one or more samples. This file contains sample information. One file can contain information regarding one to many samples.
* Experiment: each sample has been sequenced. This then constitutes an experiment, which is then described in this file. One Experiment file can contain one to many experiments.
* Run: within each experiment, one or more sequencing runs have been done. In most cases, when there is only one pair of fastq files, there will be only one Run per Experiment. If there are more, more Runs  describing each run has to be created. One Run file can contain one to many Runs. This is the file that contains the filenames of the files transferred to the ENA dropbox above.
* Submission: whenever a file (any of the ones mentioned above) is to be transferred to ENA, a file has to accompany it that tells the system on the other side what is to be done with it. This is the role of the submission file.  

When submitting files, ENA recommends to do a test against the test server first. This will check that the files submitted have the right format etc. The web addresses for both can be [found on the ENA pages](https://ena-docs.readthedocs.io/en/latest/general-guide/programmatic.html).


### Creating the necessary files

In this section, the necessary files and their formats are described. Note, these files can contain significantly more information than described here - see the ENA webpages for more information. The minimum versions given here were generously contributed by [@martinghunt](https://github.com/martinghunt) and the [Iqbal lab](https://github.com/iqbal-lab-org).

#### The study file

This is the file that describes what the study in question was. There are some essential pieces of information that is needed to create this one:

* Project alias - a specific tag for this study. Will be used by other entries.
* Title - a name for the project/study.
* Description - a text description of the project/study. This should contain information
regarding how many samples are included and a bit about library prep and how they were sequenced.

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

#### The sample file

This file describes the samples in your read set. This file can contain many sample entries in one file. This is done by having multiple SAMPLE sections in the file. One SAMPLE section begins with the "<SAMPLE...>" tag, and ends with the "</SAMPLE...>" tag.

Some values need to be detailed here (per sample):
- Sample alias - a specific tag for this sample. Will be used by other entries.
- Center name - the name of the institution sequencing/submitting the reads
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
In this XML snippet, other information can also be added. Some things that should be considered is to add the isolation year (collection_date) and what it was isolated from (isolation_source). That would then look like this:

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

#### The experiment file


#### The submit file

All file

```
<SUBMISSION>
    <ACTIONS>
         <ACTION>
              <RELEASE target="TODO: study accession number"/>
         </ACTION>
    </ACTIONS>
</SUBMISSION>
```

As is notable from the file above, there is a 'TODO' noted. Any such fields in this tutorial has to be filled with some information. The information above comes from the Study file that we will create next.
