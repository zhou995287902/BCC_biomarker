# Screening for Burkholderia cepacia species-specific protein markers

This project aims to screen for candidate proteins that can serve as species-specific protein markers for the Burkholderia cepacia (BCC) from the proteomic data of 341 bacterial strains.

## Dependencies

- Python 3.6+
- DIAMOND 0.9.26

## Data preparation 

1. Obtain information for 78 BCC strains and 263 non-BCC strains from the NCBI Genebank database, and save to files nine_strain_info.csv and other_strain_info.csv.

2. Use the download_ref_seq.py script to generate the download_cmd.sh file, and download the reference genome sequences of 341 bacterial strains from the NCBI GenBank database.

```bash
python3 download_ref_seq.py nine_strain_info.csv >> download_cmd.sh
python3 download_ref_seq.py other_strain_info.csv >> download_cmd.sh
bash download_cmd.sh
```

3. Use the diamond_blastp_cmd.py script to generate the diamond database construction command file diamond_mkdb_cmd.sh and the diamond protein sequence alignment command file diamond_blastp_cmd2.sh.

```bash 
python diamond_blastp_cmd.py *.faa
bash diamond_mkdb_cmd.sh
bash diamond_blastp_cmd2.sh
```

## Screening process

1. Run the diamond database construction and alignment commands to obtain alignment results for all protein sequences. 

2. Use the filter_nine_strain.py script to filter the alignment results, keeping proteins matching any of the 9 BCC genomic types, generating 9 BCC protein files.

3. Use the filter_core_genome.py script to further filter the 9 BCC protein files, obtaining core proteins present in all 9 BCC genomic types in files nine_core_protein.table and nine_core_protein.fasta.

4. Extract specific proteins and their encoding genes as candidate BCC species-specific protein markers.

## Usage

```bash
# Get strain information
# Obtain 78 BCC and 263 non-BCC strains from NCBI Genebank, save to nine_strain_info.csv and other_strain_info.csv

# Download reference genomes
python3 download_ref_seq.py nine_strain_info.csv >> download_cmd.sh  
python3 download_ref_seq.py other_strain_info.csv >> download_cmd.sh
bash download_cmd.sh

# Generate diamond alignment commands 
python diamond_blastp_cmd.py *.faa

# Run diamond commands
bash diamond_mkdb_cmd.sh
bash diamond_blastp_cmd2.sh

# First round filtering
python ../../../scripts/filter_nine_strain.py ../../../strain_list/nine_stain.tale ../../../strain_list/other_strain.table all_protein_out.m6 ../all_protein.faa

# Second round filtering
python ../../../scripts/filter_core_genome.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table new_goodProteins.m6 ../*faa.gz > filter_nine_core_protein.fasta
```
