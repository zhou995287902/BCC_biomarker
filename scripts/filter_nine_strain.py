import sys


# user conmmand :  python ../../../scripts/filter_nine_strain.py ../../../strain_list/nine_stain.tale ../../../strain_list/other_strain.table all_protein_out.m6 ../all_protein.faa


nine_strain_file = sys.argv[1]
other_strain_file = sys.argv[2]
blastp_file = sys.argv[3]
protein_file = sys.argv[4]

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


def get_protein_id(protein_file):
    protein_id_dict = {}
    with open(protein_file,'r',encoding = 'utf-8') as read_protein_file:
        for line in read_protein_file:
            if '>' in line[0]:
                line_split = line.strip().split('[')
                protein_id = line_split[0].split(' ')[0].replace('>','')
                strain_space = line_split[-1].strip().strip(']').strip('1026b').strip().replace(' ','_')
                protein_id_dict[protein_id] = [strain_space]
            else:
                if len(protein_id_dict[protein_id]) < 2:
                    protein_id_dict[protein_id].append(line)
                else:
                    protein_id_dict[protein_id][1] += line
    return protein_id_dict


def get_blastp_own_nine_cds(blastp_file,nine_strain,protein_id_dict):
    res = set()
    with open(blastp_file) as read_blastp_file:
        for line in read_blastp_file:
            col_list = line.strip().split('\t')
            ref_id = col_list[1]
            alignment_id = col_list[0]
            if ref_id != alignment_id:
                ref_strain_space = protein_id_dict[ref_id][0]
                alignment_strain_space = protein_id_dict[alignment_id][0]
                if ref_strain_space in nine_strain and alignment_strain_space in nine_strain:
                    res.add(ref_id)
                    res.add(alignment_id)
                else:
                    if ref_id in res:
                        res.remove(ref_id)
                    if alignment_id in res:
                        res.remove(alignment_id)

    return res


def get_own_nine_cds(blastn_file,nine_strain_dict,other_strain_dict):
    res = set()
    with open(blastn_file) as read_blastn_file:
        for line in read_blastn_file:
            col_list = line.strip().split('\t')
            ref_id = col_list[0]
            alignment_id = col_list[0]
            ref_seq_name = col_list[0].split('_')[0].replace('lcl|','')
            alignment_seq_name = col_list[1].split('_')[0]
            if ref_seq_name != alignment_seq_name:
                if ref_seq_name in nine_strain_dict.keys() and alignment_seq_name in nine_strain_dict.keys():
                    res.add(ref_id)
                    res.add(alignment_id)
                else:
                    if ref_id in res:
                        res.remove(ref_id)
                    if alignment_id in res:
                        res.remove(alignment_id)
    return res


if __name__ == "__main__":
    nine_strain_dict,other_strain_file = get_dict(nine_strain_file,other_strain_file)
    # print(nine_strain_dict)
    protein_id_dict = get_protein_id(protein_file)
    # print(protein_id_dict)
    res = get_blastp_own_nine_cds(blastp_file,nine_strain,protein_id_dict)
    # print(res)
    for i in nine_strain_abb.values():
        print(i)
        globals()[i] = open(i+'.fasta',"w")
        for ii in res:
            if i == nine_strain_abb[protein_id_dict[ii][0]]:
                print('>{}|{}\n{}'.format(nine_strain_abb[protein_id_dict[ii][0]],ii,protein_id_dict[ii][1].strip()),file = eval(i))

        eval(i).close()