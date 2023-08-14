import sys 

diamond_db_cmd = open('diamond_mkdb_cmd.sh','w')
diamond_blastp_cmd = open('diamond_blastp_cmd2.sh','w')

cds_file_list = sys.argv[1:]
for index in range(len(cds_file_list)-1):
	new_name = cds_file_list[index].strip('../').split('.faa')[0]
	mkdb_cmd = 'zcat {}|diamond makedb --in - --db {}'.format(' '.join(cds_file_list[index+1:]),new_name)
	blastp_cmd = 'zcat {}|diamond blastp --db ../diamond_db/{} --query - --outfmt 6 --out {}_out.m6 --max-target-seqs 5000 --sensitive --evalue 1e-10 --index-chunks 1 --id 80 --tmpdir ./temp/'.format(cds_file_list[index],new_name,new_name)
	print(mkdb_cmd,file=diamond_db_cmd)
	print(blastp_cmd,file=diamond_blastp_cmd)
	print('gzip {}_out.m6'.format(new_name),file=diamond_blastp_cmd)

diamond_blastp_cmd.close()
diamond_db_cmd.close()
