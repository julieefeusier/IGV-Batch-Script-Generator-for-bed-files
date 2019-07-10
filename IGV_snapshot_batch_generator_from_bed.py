#!/usr/bin/python
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--in',
                    metavar='INPUT BED',
                    dest="i",
                    required=True,
                    help='name/path to BED to convert into IGV batch script')

parser.add_argument('-o', '--out',
                    metavar='OUTPUT IGV BATCH SCRIPT',
                    dest="o",
                    help='output IGV batch script. Will default to stdout')

requiredNamed.add_argument('-b', '--bam_dir',
                    metavar='BAM DIRECTORY',
                    required=True,
                    dest="b",
                    help='path to bam directory')

requiredNamed.add_argument('-s', '--snapshot_dir',
                    metavar='SNAPSHOT DIRECTORY',
                    required=True,
                    dest="d",
                    help='path to final IGV snapshot directory')

parser.add_argument('-bp', '--buffer',
                    metavar='BP BUFFER',
                    dest="bp",
                    type=int,
                    help='bp buffer around locus in IGV')

parser.add_argument('-p', '--ped',
                    metavar='PED FILE',
                    dest="p",
                    help='name/path to PED file for trio pictures')

args = parser.parse_args()

if args.i is None:
        raise NameError('Must include name/path to BED file with option -i')
else:
        input_file1 = args.i

if args.o is None:
        f = sys.stdout
else:
        output_file = args.o
        f=open(output_file, 'w+')

if args.b is None:
        raise NameError('Must include path to BAM directories with option -b')
else:
        file_directory = args.b

if args.d is None:
        raise NameError('Must include path to final snapshot directory with option -d')
else:
        snapshot_directory = args.d

if args.bp is None:
        bp_buffer = 50
else:
        bp_buffer = args.bp

#This incorporates trio information
if args.p is None:
        ped = 0
else:
        ped = args.p
        Sample_key = {}
        ped_lines=open(ped, 'r')
        for ped_line in ped_lines:
                bed_split=[l.strip() for l in ped_line.split('\t')]
                Family_id=bed_split[0]
                sample=bed_split[1]
                father=bed_split[2]
                mother=bed_split[3]
                if sample not in Sample_key.keys():
                        Sample_key[sample] = father,mother

        ped_lines.close()

lines=open(input_file1,'rt')
pos_upstream = ""
pos_downstream = ""

f.write(str("snapshotDirectory " + snapshot_directory + '\n'))
sample_prev = ""
for bed_line in lines:
        bed_split=[l.strip() for l in bed_line.split('\t')]
        chr = bed_split[0]
        pos = bed_split[1]
        pos2 = bed_split[2]
        sample=bed_split[3]
        sample_tmp=sample.split(".")
	sample_name=sample_tmp[0]
	pos_upstream = int(pos) - (bp_buffer)
	pos_downstream = int(pos2) + (bp_buffer)
        
        if ped != 0: #checking ped
                father1, mother2 = Sample_key[sample_name]
	
        ###This checks to make sure to not reload the same sample.
	if sample_prev != sample:
		f.write("new\n")
		f.write(str("load " + file_directory + sample + "\n"))
                if ped != 0:
                        f.write(str("load " + file_directory + father1 + ".bam\n"))
                        f.write(str("load " + file_directory + mother2 + ".bam\n"))
	f.write(str("goto " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "\n"))
	f.write(str("sort\ncollapse\n"))
        snapshot = "snapshot " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "_" + str(sample_name)
        if ped != 0:
                f.write(str(snapshot + "_trio.png\n"))
	else:
                f.write(str(snapshot + ".png\n"))
	father1, mother2 = "",""
	sample_prev = sample
lines.close()
f.close()
