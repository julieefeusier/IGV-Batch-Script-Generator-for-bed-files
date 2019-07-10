# IGV-Batch-Script-Generator-for-bed-files
This script generates IGV batch scripts from bed files. The script can be loaded into IGV for automatic generation of images on the command line.

**usage**:<br/>
```
usage: IGV_snapshot_batch_generator_from_bed.py [-h] -i INPUT BED
                                                [-o OUTPUT IGV BATCH SCRIPT]
                                                -b BAM DIRECTORY -s SNAPSHOT
                                                DIRECTORY [-bp BP BUFFER]
                                                [-p PED FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT IGV BATCH SCRIPT, --out OUTPUT IGV BATCH SCRIPT
                        output IGV batch script name/path
  -bp BP BUFFER, --buffer BP BUFFER
                        bp buffer around locus in IGV
  -p PED FILE, --ped PED FILE
                        name/path to PED file for trio pictures

required named arguments:
  -i INPUT BED, --in INPUT BED
                        name/path to BED to convert into IGV batch script
  -b BAM DIRECTORY, --bam_dir BAM DIRECTORY
                        path to bam directory
  -s SNAPSHOT DIRECTORY, --snapshot_dir SNAPSHOT DIRECTORY
                        path to final IGV snapshot directory
```
The script requires column 4 of the bed file to be the name of the bam file (see example.bed). It is best to pre-sort the bed file by the bam names, because IGV runs faster when it doesn't have to reload the bam for each image.


**locations.bed**:<br/>
  chr1    1000000 1000001 sample1.bam<br/>
  chr5    800000  800001  sample2.bam<br/>
  chr5    800000  800001  sample1.bam<br/>

```
sort -k4,1 locations.bed > locations_sorted.bed
```

**locations_sorted.bed**:<br/>
  chr1    1000000 1000001 sample1.bam<br/>
  chr5    800000  800001  sample1.bam<br/>
  chr5    800000  800001  sample2.bam<br/>


**IGV_snapshot_batch_generator_from_bed.py**
Example using a 500bp buffer around the bed region (recommended for looking at 1bp region): 
```
python IGV_snapshot_batch_generator_from_bed.py -i /path/to/locations_sorted.bed -b /path/to/bam_directory/ -s /path/to/snapshot_directory/ -bp 500 -o locations_IGV_batch.txt
```
snapshotDirectory /snapshot_directory/<br/>
new<br/>
load /file/to/bams/sample1.bam<br/>
goto chr1:999500-1000501<br/>
sort<br/>
collapse<br/>
snapshot chr1:999500-1000501_sample1.png<br/>
goto chr5:799500-800501<br/>
sort<br/>
collapse<br/>
snapshot chr5:799500-800501_sample1.png<br/>
new<br/>
load /file/to/bams/sample2.bam<br/>
goto chr5:799500-800501<br/>
sort<br/>
collapse<br/>
snapshot chr5:799500-800501_sample2.png<br/>


**Trio option** -p takes in a ped file and generates an IGV image of a trio (child, dad, mom)

**example.ped**<br/>
pedigree1       sample1 sample1_father  sample1_mother  1       0<br/>
pedigree2       sample2 sample2_father  sample2_mother  2       0<br/>

```
python IGV_snapshot_batch_generator_from_bed.py -i /path/to/locations_sorted.bed -b /path/to/bam_directory/ -s /path/to/snapshot_directory/ -bp 500 -o locations_IGV_batch.txt -p /path/to/example.ped
```

snapshotDirectory /snapshot_directory/<br/>
new<br/>
load /vbod2/CEPH_BAMs/sample1.bam<br/>
load /vbod2/CEPH_BAMs/sample1_father.bam<br/>
load /vbod2/CEPH_BAMs/sample1_mother.bam<br/>
goto chr1:999500-1000501<br/>
sort<br/>
collapse<br/>
snapshot chr1:999500-1000501_sample1_trio.png<br/>
goto chr5:799500-800501<br/>
sort<br/>
collapse<br/>
snapshot chr5:799500-800501_sample1_trio.png<br/>
new<br/>
load /file/to/bams/sample2.bam<br/>
load /file/to/bams/sample2_father.bam<br/>
load /file/to/bams/sample2_mother.bam<br/>
goto chr5:799500-800501<br/>
sort<br/>
collapse<br/>
snapshot chr5:799500-800501_sample2_trio.png<br/>
