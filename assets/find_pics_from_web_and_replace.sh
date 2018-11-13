more *.tex | grep -o 'http://.*.peg' *.tex > ../url.txt
more *.tex | grep -o 'http://.*.png' *.tex >> ../url.txt
grep -o 'http://.*.peg' ../url.txt > ../urls.txt
grep -o 'http://.*.png' ../url.txt >> ../urls.txt
rm ../url.txt
# 捕获组的概念
# .表示任意一个字符
# *表示*前面出现的那个字符重复0或任意次
# grep -o 'http://(/[\w-]+\.)+[\w-]+(/[\w- ./?%&=]*)?' *.tex  
# # grep -o 'http://' *.tex | wc -l
# # # 出现次数
# # more *.tex |grep 'http://' -n
# # 把来着网络的图片要下载并替换路径
# #https://bbs.csdn.net/topics/380032747
# #https://blog.csdn.net/a1102086061/article/details/54616877 
