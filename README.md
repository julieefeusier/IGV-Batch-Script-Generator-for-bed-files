# IGV-Batch-Script-Generator-for-bed-files
These scripts generate IGV batch scripts from bed files. The script can be loaded into IGV for automatic generation of images on the command line.


These scripts take a bed file and generate an IGV batch file that can be uploaded through IGV. The script requires column 4 of the bed file to be the name of the bam file (see example.bed). It is best to sort the bed file by the bam names, because IGV runs faster when it doesn't have to reload the bam for each image.


Example using a 500bp buffer around the bed region (recommended for looking at 1bp region): 

**example.bed**:<br/>
  chr1    1000000 1000001 sample1.bam<br/>
  chr5    800000  800001  sample1.bam<br/>
  chr5    800000  800001  sample2.bam<br/>

```
python2.7 IGV_snapshot_batch_generator_from_bed.py example.bed /file/to/bams/ /snapshot_directory/ 500
```
snapshotDirectory /snapshot_directory/
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


IGV_snapshot_batch_generator_from_bed_trio.py takes in a ped file and generates an IGV image of a trio (child, dad, mom)

**example.ped**<br/>
pedigree1       sample1 sample1_father  sample1_mother  1       0<br/>
pedigree2       sample2 sample2_father  sample2_mother  2       0<br/>

```
python2.7 IGV_snapshot_batch_generator_from_bed_trio.py example.bed example.ped /file/to/bams/ /snapshot_directory/ 500
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
load /vbod2/CEPH_BAMs/sample2.bam<br/>
load /vbod2/CEPH_BAMs/sample2_father.bam<br/>
load /vbod2/CEPH_BAMs/sample2_mother.bam<br/>
goto chr5:799500-800501<br/>
sort<br/><br/>
collapse<br/>
snapshot chr5:799500-800501_sample2_trio.png<br/>

