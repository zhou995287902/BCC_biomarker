import sys
import gzip
import re 
import pickle


# user conmmand :  python ../../../scripts/get_strain_specie.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table obj_protein_id.pkl *_protein_out.m6.gz

nine_strain_file = sys.argv[1]
other_strain_file = sys.argv[2]
blastp_file = sys.argv[4:]
protein_pkl_file = sys.argv[3]

nine_strain = ['Burkholderia_cepacia','Burkholderia_multivorans','Burkholderia_cenocepacia','Burkholderia_stabilis','Burkholderia_vietnamiensis',\
'Burkholderia_dolosa','Burkholderia_ambifaria','Burkholderia_anthina','Burkholderia_pyrrocinia']
nine_strain_abb = {'Burkholderia_cepacia':'bcp','Burkholderia_multivorans':'bmt','Burkholderia_cenocepacia':'bcc','Burkholderia_stabilis':'bsb',\
'Burkholderia_vietnamiensis':'bvt','Burkholderia_dolosa':'bdo','Burkholderia_ambifaria':'bab','Burkholderia_anthina':'bat',\
'Burkholderia_pyrrocinia':'bpc'}


def save_obj(obj, name):
    with open('obj_'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

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


def get_blastp_own_nine_cds(blastp_file,nine_strain_abb,protein_id_dict):
    res = set()
    filter_list = {}
    count = 0
    for each_blastp_file in blastp_file:
        count +=1
        print(count,each_blastp_file)
        with gzip.open(each_blastp_file,'rt') as read_blastp_file:
            # lines = read_blastp_file.readlines()
            for line in read_blastp_file:
                col_list = line.strip().split('\t')
                ref_id = col_list[1]
                alignment_id = col_list[0]
                if ref_id != alignment_id:
                    ref_strain_space = protein_id_dict[ref_id][0]
                    alignment_strain_space = protein_id_dict[alignment_id][0]
                # print(ref_strain_space,alignment_strain_space)
                # if ref_strain_space != alignment_strain_space:
                    if ref_strain_space in nine_strain_abb and alignment_strain_space in nine_strain_abb: 
                        if ref_id not in filter_list and alignment_id not in filter_list:
                            res.add(ref_id)
                            res.add(alignment_id)
                    else:
                        if ref_id in res:
                            filter_list[ref_id] = False
                            res.remove(ref_id)
                        if alignment_id in res:
                            filter_list[alignment_id] = False
                            res.remove(alignment_id)

    return res


def get_own_nine_cds(blastn_file,nine_strain_dict,other_strain_dict):
    res = set()
    count = 0
    with open(blastn_file) as read_blastn_file:
        count += 1
        print(count)
        for line in read_blastn_file:
            col_list = line.strip().split('\t')
            ref_id = col_list[0]
            alignment_id = col_list[0]
            ref_seq_name = col_list[0].split('_')[0].replace('lcl|','')
            alignment_seq_name = col_list[1].split('_')[0]
            if ref_seq_name != alignment_seq_name:
                if nine_strain_dict.get(ref_seq_name) and nine_strain_dict.get(alignment_seq_name):
                    res.add(ref_id)
                    res.add(alignment_id)
                else:
                    if ref_id in res:
                        res.remove(ref_id)
                    if alignment_id in res:
                        res.remove(alignment_id)
    return res


if __name__ == "__main__":
    # nine_strain_dict,other_strain_dict = get_dict(nine_strain_file,other_strain_file)
    # print(nine_strain_dict)
    protein_id_dict = load_obj(protein_pkl_file)
    # print(protein_id_dict)
    res = get_blastp_own_nine_cds(blastp_file,nine_strain_abb,protein_id_dict)
    print('get nine own protein ok!')
    # print(res)
    for i in nine_strain_abb.values():
        print(i)
        globals()[i] = open(i+'.fasta',"w")
        for ii in res:
            if i == nine_strain_abb[protein_id_dict[ii][0]]:
                print('>{}|{}\n{}'.format(nine_strain_abb[protein_id_dict[ii][0]],ii,protein_id_dict[ii][1].strip()),file = eval(i))

        eval(i).close()