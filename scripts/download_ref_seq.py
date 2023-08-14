import sys

## 当输入的参数个数不等于3时，就打印本脚本的提示文本，以及参考输入文本，并且退出脚本
if len(sys.argv) != 2:
    print('\nuseage:\npython3 download_ref_seq.py <input_txt> \nexample:\npython3 download_ref_seq.py strain_list_add_assembly_name.txt \n')
    exit()

with open(sys.argv[1],'r') as read_file:
    lines = read_file.readlines()
    for line in lines:
        line = line.strip().split(',')
        ID = line[2].strip('"').split('/')[-1]
        ftp_link = line[2].strip('"')
        # file_name = ['_cds_from_genomic.fna.gz','_genomic.fna.gz','_genomic.gff.gz','_protein.faa.gz','_genomic.gbff.gz','_feature_table.txt.gz']
        file_name = ['_protein.faa.gz']
        for i in file_name:
            cmd_str = 'wget {0}/{1}'.format(ftp_link,ID+i)
            cmd_change_name = 'mv {0} {1}'.format(ID+i,line[0].strip('"').replace(' ','_')+'_'+ID+i)
            print(cmd_str) 
            print(cmd_change_name)
