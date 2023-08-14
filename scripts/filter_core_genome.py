import sys
import re
import gzip


# usecommand python ../../../scripts/filter_core_genome.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table new_goodProteins.m6 ../*faa.gz > new_temp.temp
# usecommand python ../../../scripts/filter_core_genome.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table new_goodProteins.m6 ../*faa.gz > filter_nine_core_protein.fasta

nine_strain_abb = {'bcp':'Burkholderia_cepacia','bmt':'Burkholderia_multivorans','bcc':'Burkholderia_cenocepacia','bsb':'Burkholderia_stabilis',\
'bvt':'Burkholderia_vietnamiensis','bdo':'Burkholderia_dolosa','bab':'Burkholderia_ambifaria','bat':'Burkholderia_anthina',\
'bpc':'Burkholderia_pyrrocinia'}

nine_strain_file = sys.argv[1]
other_strain_file = sys.argv[2]
blastp_file = sys.argv[3]
protein_file = sys.argv[4:]

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

def get_protein_id(protein_file,nine_strain_dict,other_strain_dict):
    protein_id_dict = {}
    for each_protein_file in protein_file:
        # print(each_protein_file)
        assembly = re.search(r'GC[AF]_\d+\.\d_',each_protein_file).group().strip('_')
        # print(assembly)
        if assembly in nine_strain_dict.keys():
            strain_space = nine_strain_dict[assembly]
        else:
            strain_space = other_strain_dict[assembly]
        with gzip.open(each_protein_file,'rt') as read_protein_file:
            for line in read_protein_file:
                if '>' in line[0]:
                    line_split = line.strip().split('[')
                    protein_id = line_split[0].split(' ')[0].replace('>','')
                    # strain_space = line_split[-1].strip().strip(']').strip('1026b').strip().replace(' ','_')
                    protein_id_dict[protein_id] = [strain_space]
                else:
                    if len(protein_id_dict[protein_id]) < 2:
                        protein_id_dict[protein_id].append(line)
                    else:
                        protein_id_dict[protein_id][1] += line
    return protein_id_dict


def get_core_genome(blastp_file):
    res = {}
    with open(blastp_file,'r')as read_blastp_file:
        for line in read_blastp_file:
            col_list = line.strip().split('\t')
            strain_specie_col_1 = col_list[0].split('|')[0]
            strain_protein_id_1 = col_list[0].split('|')[1]
            strain_specie_col_2 = col_list[1].split('|')[0]
            strain_protein_id_2 = col_list[1].split('|')[1]
            if strain_specie_col_1 != strain_specie_col_2:
                if col_list[1] not in res.keys():
                    if col_list[0] not in res.keys():
                        res[col_list[0]] = {strain_specie_col_2:[strain_protein_id_2]}
                    elif strain_specie_col_2 not in res[col_list[0]].keys():
                        res[col_list[0]][strain_specie_col_2] = [strain_protein_id_2]
                    else:
                        res[col_list[0]][strain_specie_col_2].append(strain_protein_id_2)
    return res


if __name__ == '__main__':
    nine_strain_dict,other_strain_dict = get_dict(nine_strain_file,other_strain_file)
    protein_id_dict = get_protein_id(protein_file,nine_strain_dict,other_strain_dict)
    res = get_core_genome(blastp_file)
    fasta_file = open('nine_core_protein_95.fasta','w')
    table_file = open('nine_core_protein_95.table','w')
    for k,v in res.items():
        if len(v) == 8: 
            strain_specie = nine_strain_abb[k.split('|')[0]]
            protein_id = k.split('|')[1]
            print('{}|{}\t'.format(strain_specie,protein_id),'\t'.join([nine_strain_abb[i] + '|' + v[i][0] for i in v.keys()]),file = table_file) 
            print('>{}|{}\n{}'.format(protein_id,strain_specie,protein_id_dict[protein_id][1].strip()),file = fasta_file)
            for key,value in v.items():
                strain_specie = nine_strain_abb[key]
                # protein_id = value[0]
                for protein_id in value:
                    print('>{}|{}\n{}'.format(protein_id,strain_specie,protein_id_dict[protein_id][1].strip()),file = fasta_file)
    fasta_file.close()
    table_file.close()



