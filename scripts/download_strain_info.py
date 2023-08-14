import sys
import re
import gzip


# usecommand :python scripts/download_strain_info.py strain_list/nine_stain.table strain_list/other_strain.table all_strain.csv strain_seq/protein_seq/*faa.gz

strain_csv_file = sys.argv[3]
nine_strain_file = sys.argv[1]
other_strain_file = sys.argv[2]
# blastp_file = sys.argv[3]
protein_file = sys.argv[4:]


def get_strain_info(strain_csv_file):
    all_strain_info_dict = {}
    with open(strain_csv_file,'r') as read_csv_file:
        for line in read_csv_file:
            if line[0] != '#':
                col_list = line.strip().split(',')
                all_strain_info_dict[col_list[5].strip('"')] = ','.join(col_list[:-2])
            else:
                headline = ','.join(line.strip().split(',')[:-2])
    return all_strain_info_dict,headline


def get_dict(nine_strain_file,other_strain_file):
    read_nine_strain= open(nine_strain_file,'r')
    read_other_strain= open(other_strain_file,'r')
    # all_csv_file_list = sys.argv[1:]
    nine_strain_dict = {}
    other_strain_dict = {}
    for line in read_nine_strain:
        col_list = line.strip().split('\t')
        nine_strain_dict[col_list[-1]] = col_list[0]

    for line in read_other_strain:
        col_list = line.strip().split('\t')
        other_strain_dict[col_list[-1]] = col_list[0]

    read_other_strain.close()
    read_nine_strain.close()
    return nine_strain_dict,other_strain_dict


def get_protein_id(protein_file,all_strain_info_dict,nine_strain_dict,other_strain_dict,headline):
    protein_id_dict = {}
    nine_strain_file_info = open('nine_strain_info.csv','w')
    print(headline,file = nine_strain_file_info)
    other_strain_file_info = open('other_strain_info.csv','w')
    print(headline,file = other_strain_file_info)
    for each_protein_file in protein_file:
        # print(each_protein_file)
        assembly = re.search(r'GC[AF]_\d+\.\d_',each_protein_file).group().strip('_')
        # print(assembly)
        
        if assembly in nine_strain_dict:
            print(all_strain_info_dict[assembly],file=nine_strain_file_info)
        else:
            print(all_strain_info_dict[assembly],file=other_strain_file_info)
    nine_strain_file_info.close()
    other_strain_file_info.close()


if __name__ == "__main__":
    all_strain_info_dict,headline = get_strain_info(strain_csv_file)
    nine_strain_dict,other_strain_dict = get_dict(nine_strain_file,other_strain_file)
    # print(all_strain_info_dict)
    get_protein_id(protein_file,all_strain_info_dict,nine_strain_dict,other_strain_dict,headline)    
    
