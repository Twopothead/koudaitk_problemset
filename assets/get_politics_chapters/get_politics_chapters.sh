# 把含有tex的problems_detail.zip解压,把politics文件夹拷贝到当前目录运行此脚本,得到合并后的章节总tex
workdir=`pwd`; echo "Current working dir : $workdir";
# 创建章节所在目录
chapters="politics_chapters/"
echo ${workdir}/${chapters}
if [ ! -d "${workdir}/${chapters}" ]; then mkdir "${workdir}/${chapters}"; echo "chapters directory created : ${workdir}/${chapters}"; fi;
sourcedir="${workdir}/politics/"; echo "Source dir is : $sourcedir";
for dir in `ls -F $sourcedir | grep "/$"`; do
    echo "Sub-dir : ${dir}";
    # echo ${dir%/*} # 删除目录末尾的／
    # cd ${sourcedir}${dir} && cd ../../${chapters} && echo `pwd`
    cd ${sourcedir}${dir} && rm ./*.txt && rm ./*.htm && cat ./*.tex> ./sum.latex && mv ./sum.latex ../../${chapters}${dir%/*}.tex
    # cd ${sourcedir}${dir} && echo ../../${chapters}${dir%/*}.tex
done;
