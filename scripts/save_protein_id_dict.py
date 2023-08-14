import sys
import gzip
import re 


# user conmmand :  python ../../../scripts/filter_nine_strain.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table all_protein_out.m6 ../*.faa.gz


nine_strain_file = sys.argv[1]
other_strain_file = sys.argv[2]
# blastp_file = sys.argv[3]
protein_file = sys.argv[3:]

nine_strain = ['Burkholderia_cepacia','Burkholderia_multivorans','Burkholderia_cenocepacia','Burkholderia_stabilis','Burkholderia_vietnamiensis',\
'Burkholderia_dolosa','Burkholderia_ambifaria','Burkholderia_anthina','Burkholderia_pyrrocinia']
nine_strain_abb = {'Burkholderia_cepacia':'bcp','Burkholderia_multivorans':'bmt','Burkholderia_cenocepacia':'bcc','Burkholderia_stabilis':'bsb',\
'Burkholderia_vietnamiensis':'bvt','Burkholderia_dolosa':'bdo','Burkholderia_ambifaria':'bab','Burkholderia_anthina':'bat',\
'Burkholderia_pyrrocinia':'bpc'}


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


import pickle

def save_obj(obj, name ):
    with open('obj_'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj_' + name + '.pkl', 'rb') as f:
        return pickle.load(f)



if __name__ == "__main__":
    nine_strain_dict,other_strain_dict = get_dict(nine_strain_file,other_strain_file)
    # print(nine_strain_dict)
    protein_id_dict = get_protein_id(protein_file,nine_strain_dict,other_strain_dict)
    # print(protein_id_dict)
    save_obj(protein_id_dict,'protein_id')