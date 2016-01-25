# coding:utf-8
import posi_predict
import degree_predict
import salary_predict
import size_predict
import codecs

file_out = codecs.open('result.csv', 'w', 'utf-8')


def get_result():
    print '将进行职位预测，需要1小时以上，请耐心等待'
    posi_result = posi_predict.train()
    print '职位预测结束\n将进行degree预测：'
    degree_result = degree_predict.train()
    print 'degree预测结束\n将进行salary预测：'
    salary_result = salary_predict.train()
    print 'salary预测结束\n将进行size预测：'
    size_result = size_predict.train()
    first_line = 'id,degree,size,salary,position_name\n'
    file_out.write(first_line)
    for key in posi_result.keys():
        posi = posi_result[key]
        degree = str(degree_result[key])
        salary = str(salary_result[key])
        size = str(size_result[key])
        file_out.write(key + ',' + degree + ',' + size + ',' + salary + ',' + posi + '\n')
    print '程序结束'
    file_out.close()


if __name__ == '__main__':
    get_result()
