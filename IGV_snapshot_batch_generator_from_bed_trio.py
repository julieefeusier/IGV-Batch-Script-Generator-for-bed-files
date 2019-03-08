import sys

try:
        input_file1=sys.argv[1]
	ped=sys.argv[2]
        file_directory=sys.argv[3]
        snapshot_directory=sys.argv[4]
        bp_buffer=int(sys.argv[5])
except:
        print "Usage: py input.txt (chr position1 position2 sample.bed) input.ped bam_file_directory snapshot_directory bp_buffer > output.txt"

try:
        f=open(input_file1,'r')
        f_line=f.readline()
        f.close()
except:
        print "Can't open bed file."

###This creates a dictionary of trios based on the ped file
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

lines=open(input_file1,'rt')
bp_buffer=int(sys.argv[5])
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

	father1, mother2 = Sample_key[sample_name]
	
        ###This checks to make sure to not reload the same sample.
	if sample_prev != sample:
		print "new"
		join_load = "load /vbod2/CEPH_BAMs/" + sample
		join_load1 = "load /vbod2/CEPH_BAMs/" + father1 + ".bam"
		join_load2 = "load /vbod2/CEPH_BAMs/" + mother2 + ".bam"

		print join_load
		print join_load1
		print join_load2
		
	join_goto = "goto " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream)
	print join_goto
	print "sort"
	print "collapse"
	snapshot = "snapshot " + str(chr) + ":" + str(pos_upstream) + "-" + str(pos_downstream) + "_" + str(sample_name) + "_trio.png"
	print snapshot
	father1, mother2 = "",""
	sample_prev = sample
