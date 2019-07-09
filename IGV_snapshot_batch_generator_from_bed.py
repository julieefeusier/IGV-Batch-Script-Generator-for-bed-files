import sys
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('-i', '--in',
                    metavar='INPUT BED',
                    dest="i",
                    help='path to BED to convert into IGV batch script')

parser.add_argument('-o', '--out',
                    metavar='OUTPUT IGV BATCH SCRIPT',
                    dest="o",
                    help='output IGV batch script name/path')

parser.add_argument('-b', '--bam_dir',
                    metavar='BAM DIRECTORY',
                    dest="b",
                    help='path to bam directory')

parser.add_argument('-d', '--picture_dir',
                    metavar='PICTURE DIRECTORY',
                    dest="d",
                    help='path to IGV picture directory')

parser.add_argument('-bp', '--buffer',
                    metavar='BP BUFFER',
                    dest="bp",
                    type=int,
                    help='bp buffer around locus in IGV')

parser.add_argument('-p', '--ped',
                    metavar='PED FILE',
                    dest="p",
                    help='PED FILE FOR TRIO PICTURES')

args = parser.parse_args()

if args.i is None:
        raise NameError('Must include name/path to BED file with option -i')
else:
        input_file1 = args.i

if args.o is None:
        raise NameError('Must include name/path to output file with option -o')
else:
        output_file = args.o

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
        output_file = args.bp

if args.p is None:
        ped = 0
else:
        ped = args.p
        Sample_key = {}
        ped_lines=open(ped, 'r')
        for bed_lines in ped_lines.xreadlines():
                bed_split=[l.strip() for l in bed_lines.split('\t')]
                Family_id=bed_split[0]
                sample=bed_split[1]
                father=bed_split[2]
                mother=bed_split[3]
                if sample not in Sample_key.keys():
                        Sample_key[sample] = father,mother

        ped_lines.close()


#except:
#        print "Usage: py input.txt (chr position1 position2 sample.bed) input.ped bam_file_directory snapshot_directory bp_buffer > output.txt"

try:
        f=open(input_file1,'r')
        f_line=f.readline()
        f.close()
except:
        print "Can't open bed file."

###This creates a dictionary of trios based on the ped file
#Sample_key = {}
#ped_lines=open(ped, 'r')
#for bed_lines in ped_lines.xreadlines():
#        bed_split=[l.strip() for l in bed_lines.split('\t')]
#        Family_id=bed_split[0]
#        sample=bed_split[1]
#        father=bed_split[2]
#        mother=bed_split[3]
#        if sample not in Sample_key.keys():
#		Sample_key[sample] = father,mother

#ped_lines.close()

lines=open(input_file1,'rt')
#bp_buffer=int(sys.argv[5])
pos_upstream = ""
pos_downstream = ""


s_d =  "snapshotDirectory " + snapshot_directory
print s_d
sample_prev = ""
for bed_lines in lines.xreadlines():
        bed_split=[l.strip() for l in bed_lines.split('\t')]
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
		print "new"
		join_load = "load " + file_directory + sample
		if ped != 0:
                        join_load1 = "load " + file_directory + father1 + ".bam"
                        join_load2 = "load " + file_directory + mother2 + ".bam"

		print join_load
		if ped != 0:
                        print join_load1
                        print join_load2
		
	join_goto = "goto " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream)
	print join_goto
	print "sort"
	print "collapse"
        if ped != 0:
                snapshot = "snapshot " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "_" + str(sample_name) + "_trio.png"
	else:
                snapshot = "snapshot " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "_" + str(sample_name) + ".png"
        print snapshot
	father1, mother2 = "",""
	sample_prev = sample
