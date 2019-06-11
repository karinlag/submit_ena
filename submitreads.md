# How to submit reads programmatically

Assumptions for this tutorial: a submitter has one or more readsets that they wish to submit. These files are on a linux system, and the user wants to submit them via the linux command line.


## Links and resources

Most of the information in this tutorial is found here:
* [The ENA tutorial](https://ena-docs.readthedocs.io/en/latest/)

To understand more about the relationships between files, see this page describing the data model:
 * [The ENA metadata model](https://ena-docs.readthedocs.io/en/latest/reads.html)

## Brief overview of the process

This process consists of three steps:

1. Transfer the read files to the ENA dropbox using FTP or Aspera.
1. Create XML files that describe the submission.
1. Transfer XML files. With that, the files are submitted.

The fastq files are transferred using FTP to a user specific location on the ENA server.  The XML are transferred using 'curl'. The XML files transferred describe the data being submitted. These files are interlinked by referring to each other in such a way that they, together with the read files, put together a read set submission.

To transfer read and XML files, the person submitting them must have [registered an account at ENA with a username and password](https://ena-docs.readthedocs.io/en/latest/general-guide/registration.html).

## Fastq read file transfer

Read files can be transferred to ENA using for instance FTP. Data is then put into a user specific area. Users should not expect the data to be there for more than two months. To figure out more about how to transfer, read the guide below.

* [Transfer fastq files to ENA](https://ena-docs.readthedocs.io/en/latest/fileprep/upload.html)

The files transferred will be referred to in the read pair Run file, mentioned below.

## XML Files
A read set submission consists of creating and transferring the following set of [XML](https://en.wikipedia.org/wiki/XML) files:

* Study (project): this is the file that will describe the study, and which will result in a ENA accession number for your reads.
* Sample: a study consists of one or more samples. This file contains sample information. One file can contain information regarding one to many samples.
* Experiment: each sample has been sequenced. This then constitutes an experiment, which is then described in this file One Experiment file can contain one to many experiments.
* Run: within each experiment, one or more sequencing runs have been done. In most cases, when there is only one pair of fastq files, there will be only one Run per Experiment. If there are more, more Runs  describing each run has to be created. One Run file can contain one to many Runs. This is the file that contains the filenames of the files transferred to the ENA dropbox above.
* Submission: whenever a file (any of the ones mentioned above) is to be transferred to ENA, a file has to accompany it that tells the system on the other side what is to be done with it. This is the role of the submission file.  

When submitting files, ENA recommends to do a test against the test server first. This will check that the files submitted have the right format etc. The web addresses for both can be [found on the ENA pages](https://ena-docs.readthedocs.io/en/latest/general-guide/programmatic.html).


### Creating the necessary files

Some concepts/terms are shared between these files

* Alias: this is a unique name for this particular file. This alias will be needed to be able to refer to this file from other files.

#### The study file

This is the file that describes what the study in question was. There are some essential pieces of information that is needed to create this one:

* Alias - see above.
* Description - a text description of the study. 


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
