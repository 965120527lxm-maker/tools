# 中文学术写作校准语料

本目录只收正规公开来源。材料用于本地阅读和写作规律校准，不作为可拼贴的句库，也不因下载到本地而改变原作品的版权状态。文件校验值见 `SHA256SUMS`。

| 本地文件 | 来源 | 使用边界 |
| --- | --- | --- |
| `pdfs/zhou-zhihua-machine-learning-sample.pdf` | 周志华《机器学习》，清华大学出版社官方样章：<https://www.tup.tsinghua.edu.cn/upload/books/yz/064027-01.pdf> | 商业图书样章；仅本地校准，不再分发 |
| `pdfs/zhou-zhihua-machine-learning-preface-toc.pdf` | 周志华作者主页公开的前言与目录：<https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/Book2016toc.pdf> | 作者公开材料；仅本地校准 |
| `pdfs/fudan-probability-introduction.pdf` | 谢践生《概率论引论》，复旦大学教务处公开教学支持材料：<https://jwc.fudan.edu.cn/_upload/article/files/4b/39/489071da4c2a9f56492ae9ecfc59/4cff14a9-818d-4f38-8e14-3cd7ab94ea11.pdf> | 校方公开教学材料；仅本地校准，不再分发 |
| `open-textbooks/openmlsys/preface.md` | OpenMLSys v1 中文前言，固定 revision `9c289782ccbb165ac8ad7c960ecffc12942a5560` | 项目采用 CC BY-NC-SA 4.0；保留来源与许可 |
| `open-textbooks/openmlsys/classic-machine-learning.md` | OpenMLSys v1 经典机器学习章节，同上 revision | 项目采用 CC BY-NC-SA 4.0；保留来源与许可 |

下载脚本：`tools/writing/scripts/fetch-zh-academic-corpus.sh`。脚本只访问以上批准来源，并生成文本抽取和 SHA256 清单。

潘承彪、潘承洞《初等数论》目前未找到作者或出版社提供的公开电子全文/样章，因此未下载。若作者本人持有合法 PDF，可另行导入本地私有语料；不要改用第三方“电子书下载”站补齐。
