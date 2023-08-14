import sys

nine_strain = ['Burkholderia_cepacia','Burkholderia_multivorans','Burkholderia_cenocepacia','Burkholderia_stabilis','Burkholderia_vietnamiensis',\
'Burkholderia_dolosa','Burkholderia_ambifaria','Burkholderia_anthina','Burkholderia_pyrrocinia']
nine_strain_file = open('nine_stain.tale','w')
other_strain_file = open('other_strain.table','w')
all_csv_file_list = sys.argv[1:]
for each_csv_file in all_csv_file_list:
    space_name = each_csv_file.strip('./').split('.')[0]
    with open(each_csv_file,'r') as read_file:
        lines = read_file.readlines()
        for line in lines[1:]:
            col_list = line.strip().split(',')
            strain_name = col_list[0].strip('"')
            strain_id = col_list[2].strip('"')
            strain_sam = col_list[3].strip('"')
            strain_pro = col_list[4].strip('"')
            strain_assembly = col_list[5].strip('"')
            if space_name in nine_strain:
                print('{}\t{}\t{}\t{}\t{}'.format(space_name,strain_id,strain_sam,strain_pro,strain_assembly),file=nine_strain_file)
            else:
                print('{}\t{}\t{}\t{}\t{}'.format(space_name,strain_id,strain_sam,strain_pro,strain_assembly),file=other_strain_file)
nine_strain_file.close()
other_strain_file.close()
