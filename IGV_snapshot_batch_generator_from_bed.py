import sys

try:
        input_file1=sys.argv[1]
        file_directory=sys.argv[2]
	snapshot_directory=sys.argv[3]
	bp_buffer=int(sys.argv[4])
except:
        print "Usage: python2.7 IGV_generator.py input.bed (chr position1 position2 sample.bam) bam_file_directory snapshot_directory bp_buffer> output.txt"

try:
        f=open(input_file1,'r')
        f_line=f.readline()
        f.close()
except:
        print "Can't open bed file."

lines=open(input_file1,'rt')
bp_buffer=int(sys.argv[4])
pos_upstream = ""
pos_downstream = ""

s_d =  "snapshotDirectory " + snapshot_directory
print s_d
#print "genome hg19"
sample_prev = ""
for bed_lines in lines.xreadlines():
        bed_split=[l.strip() for l in bed_lines.split('\t')]
        chr = bed_split[0]
        pos = bed_split[1]
        pos2 = bed_split[2]
        sample = bed_split[3]
        sample_tmp=sample.split(".")
	sample_name=sample_tmp[0]
	pos_upstream = int(pos) - (bp_buffer)
	pos_downstream = int(pos2) + (bp_buffer)

	if sample_prev != sample:
		print "new"
		join_load = "load " + file_directory + sample
		print join_load
				
	join_goto = "goto " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream)
	print join_goto
	print "sort"
	print "collapse"
	snapshot = "snapshot " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "_" + str(sample_name) + ".png"
	print snapshot
	sample_prev = sample
