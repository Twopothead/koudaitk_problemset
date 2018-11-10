from w3lib.html import remove_tags
a = '<em><em>ai</em></em>工程师'
print(remove_tags(a))
b="<p>在坚持唯物论的同时，没有把唯物论和辩证法相结合</p>"
#ai工程师
print(remove_tags(a))
#在坚持唯物论的同时，没有把唯物论和辩证法相结合
# python爬虫时删除多余标签内的内容remove、remove_tags
# https://blog.csdn.net/xiongzaiabc/article/details/81008432