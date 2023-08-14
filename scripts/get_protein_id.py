import sys


protein_file = sys.argv[1:]

nine_strain = ['Burkholderia_cepacia','Burkholderia_multivorans','Burkholderia_cenocepacia','Burkholderia_stabilis','Burkholderia_vietnamiensis',\
'Burkholderia_dolosa','Burkholderia_ambifaria','Burkholderia_anthina','Burkholderia_pyrrocinia']




def get_protein_id(protein_file):
    for each_protein_file in protein_file:
        
         with open(protein_file,'r') as read_protein_file:
        




if __name__ == "__main":
    nine_strain_dict,other_strain_file = get_dict(nine_strain_file,other_strain_file)
    res = get_own_nine_cds(blastn_file,nine_strain_dict,other_strain_dict)
    print(res)