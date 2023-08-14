# BCC特异性蛋白标志物筛选

本项目旨在从341株细菌的蛋白组数据中筛选出可作为BCC(布氏杆菌复合群)特异性蛋白标志物的候选蛋白。

## 依赖

- Python 3.6+
- DIAMOND 0.9.26

## 数据准备

1. 从NCBI Genebank数据库获取78株BCC菌株和263株非BCC菌株的信息,保存到nine_strain_info.csv和other_strain_info.csv文件中。

2. 使用download_ref_seq.py脚本生成下载的download_cmd.sh文件，并从NCBI GenBank数据库下载341株细菌的参考基因组序列数据。

```bash
python3 download_ref_seq.py nine_strain_info.csv >> download_cmd.sh
python3 download_ref_seq.py other_strain_info.csv >> download_cmd.sh
bash download_cmd.sh
```

3. 使用diamond_blastp_cmd.py脚本生成diamond构建数据库的命令文件diamond_mkdb_cmd.sh和diamond蛋白序列比对的命令文件diamond_blastp_cmd2.sh。

```bash
python diamond_blastp_cmd.py *.faa
bash diamond_mkdb_cmd.sh
bash diamond_blastp_cmd2.sh
```

## 筛选流程

1. 运行diamond构建数据库命令和diamond比对命令,获得所有蛋白序列两两比对的结果文件。

2. 使用filter_nine_strain.py脚本对两两比对的结果文件进行过滤,保留匹配9种BCC基因组型中的任意一种的蛋白序列，得到9种BCC蛋白序列文件。

3. 使用filter_core_genome.py脚本对9种BCC蛋白序列文件进行进一步筛选，获得出现在所有9种BCC基因组型中的核心蛋白序列文件nine_core_protein_95.table和nine_core_protein_95.fasta。

4. 提取特异性蛋白及其编码基因作为BCC特异性蛋白标志物。

## 使用方式

```bash
# 获取菌株信息 
# 从NCBI Genebank获取78株BCC菌株和263株非BCC菌株信息,保存到nine_strain_info.csv，other_strain_info.csv

# 下载参考基因组序列
python3 download_ref_seq.py nine_strain_info.csv >> download_cmd.sh
python3 download_ref_seq.py other_strain_info.csv >> download_cmd.sh
bash download_cmd.sh

# 生成diamond比对命令文件
python diamond_blastp_cmd.py *.faa

# 运行diamond命令
bash diamond_mkdb_cmd.sh
bash diamond_blastp_cmd2.sh

# 第一步筛选
python ../../../scripts/filter_nine_strain.py ../../../strain_list/nine_stain.tale ../../../strain_list/other_strain.table all_protein_out.m6 ../all_protein.faa 

# 第二步筛选
python ../../../scripts/filter_core_genome.py ../../../strain_list/nine_stain.table ../../../strain_list/other_strain.table new_goodProteins.m6 ../*faa.gz > filter_nine_core_protein.fasta

```
