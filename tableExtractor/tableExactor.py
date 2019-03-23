import os
from pprint import pprint

from docx import Document

def convert2list(table, name):
    table_temp = {}
    tmp_list = []
    for row in table.rows:
        for cell in row.cells:
            tmp_list.append(cell.text)
    list = sorted(set(tmp_list), key=tmp_list.index)
    table_temp[name] = dict(zip(list[0::2], list[1::2]))
    return table_temp

def read_doc(file):
    name = os.path.basename(file)[:-4]
    doc = Document(file)
    for table in doc.tables:
        table_dict = convert2list(table, name)
    return table_dict

def read_directory():
    rootdir = os.getcwd() + '/docs' # 获取当前目录
    list = os.listdir(rootdir )  # 列出文件夹下所有的目录与文件
    paths = []
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        paths.append(path)
    return paths


def write_xls(files):
    import xlwt
    header = ['文件名','主讲单位','主讲','讲座题目','职称职务', '拟安排\n日期', '内容提要']

    tmp_dicts = []
    for f in files:
        tmp_dict = {}
        print('#'*200)
        for key in f:
            print(key)
            tmp_dict['文件名'] = key
            for k,v in f[key].items():
                if k.strip() in header:
                    tmp_dict[k] = v
                    print(k,v)
                elif '内容提要' in k:
                    try:
                        tmp_dict['内容提要'] = str(k)
                        print('&'*200)
                        print(str(k))
                    except UnicodeDecodeError as e:
                        continue
                elif '内容提要' in v:
                    try:
                        tmp_dict['内容提要'] = str(v)
                        print('&'*200)
                        print(str(v))
                    except UnicodeDecodeError as e:
                        continue
                elif '拟安排' in k:
                    tmp_dict['拟安排'] = v
                    print(k,v)
        tmp_dicts.append(tmp_dict)

    book = xlwt.Workbook(encoding='utf-8',
                         style_compression=0)  # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    sheet = book.add_sheet('test',
                           cell_overwrite_ok=True)  # # 其中的test是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False

    # 设置表头
    i = 0
    for k in header:
        sheet.write(0, i, k)
        i = i + 1

    # 数据写入excel
    row = 1
    for tmp_dict in tmp_dicts:
        try:
            sheet.write(row, 0, tmp_dict['文件名'])  # 第二行开始
            sheet.write(row, 1, tmp_dict['主讲单位'])  # 第二行开始
            sheet.write(row, 2, tmp_dict['主讲'])  # 第二行开始
            sheet.write(row, 3, tmp_dict['讲座题目'])  # 第二行开始
            sheet.write(row, 4, tmp_dict['职称职务'])  # 第二行开始
            sheet.write(row, 5, tmp_dict['拟安排'])  # 第二行开始
            sheet.write(row, 6, tmp_dict['内容提要'])  # 第二行开始
        except KeyError:
            pass

        row = row + 1

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(os.getcwd() + '/docs/test.xls')


if __name__ == '__main__':
    paths = read_directory()
    files = []
    for p in paths:
        files.append(read_doc(p))
    write_xls(files)