import sys
import requests
import re

## 当输入的参数个数不等于2时，就打印本脚本的提示文本，以及参考输入文本，并且退出脚本
if len(sys.argv) != 2:
    print('\nuseage:\npython3 get_assembly_name.py <input_txt> \nexample:\npython3 get_assembly_name.py bacillus_amyloiquefaciens_strain_list \n')
    exit()

# 获取网页内容
def get_web_content(url):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}                        
    response = requests.get(url,headers = header)    
    return response

# 打开bacillus_amyloiquefaciens_strain_list文件，取其中的Assembly和固定的网址组成组成新的网址，使用Requests包获取网页内容，然后使用正则获取我们想要的菌株编号
with open(sys.argv[1],'r') as read_file:
    lines = read_file.readlines()
    for line in lines[1:]:
        col_list = line.strip().split(',')
        assembly_num = col_list[1].strip('"')
        print(assembly_num)
        url = 'https://www.ncbi.nlm.nih.gov/assembly/' + assembly_num
        # print(url)
        web_content = get_web_content(url).text
        # print(web_content)
        assembly_name = re.search(r'<title>(.*)</title>',web_content).group(1)
        assembly_name = assembly_name.split('-')[0].strip()
        col_list.append(assembly_name)
        print('\t'.join(col_list))
        
