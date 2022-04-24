# BBS_defender  
未名BBS守护者交互式爬虫  
## 前言  
作者为什么要写这样的一个函数？  
那是因为我看了这个帖子：https://bbs.pku.edu.cn/v2/post-read.php?bid=138&threadid=18263492
![Image load fail](./image/watern_witness0.png)  
![Image load fail](./image/watern_witness1.png)  
![Image load fail](./image/watern_witness2.png)  
![Image load fail](./image/watern_witness3.png)  
HSC领导和rmyy领导对于水n的大无畏送鹿精神作出了高度评价，对于水n在此次舆情防控攻坚战上的卓越贡献给予了充分肯定，为表彰水n的所作所为，HSC领导和rmyy领导在心里偷偷地号召BBS全站站友向水n同志学习。（以上内容均为瞎编的（doge））  
作者本人也非常“认可”水n的送鹿精神，但是想了想光表彰有啥用，来点儿实在的东西不行吗，作者突然想起来这学期选了一个Python爬虫选修课，学了一点爬虫知识，于是花了三天时间写了这个四五百行代码的交互式爬虫程序作为锦旗送给水n，有了这个交互式爬虫，水n日后的工作将会有更大的进步空间，一定继续被领导高度表扬的，加油💪🏻💪🏻💪🏻，我看好你哦。  
## 功能介绍  
1. 爬取帖子内容（包括发帖人、发帖内容、引用部分、附件内容、发帖时间、签名档）  
2. 检测被删帖子  
3. 用户交互（包括查看被删帖子、自删免爬、版务删帖免爬）  
![Image load fail](./image/reply.png)
![Image load fail](./image/white.png)
4. 生成日志文件（备份）  
![Image load fail](./image/log.png)
5. 动态操作（加时、减时、手动停止）  
6. 操作通知  
![Image load fail](./image/add_poster.png)
![Image load fail](./image/sub_poster.png)
7. 五杀荣耀播报   
![Image load fail](./image/Glory_broadcast.png)
8. 守护通知自动复活
![Image load fail](./image/reborn.png)
9. 炸楼全局广播（需要手动确认） 
![Image load fail](./image/bomb.png) 
## 食用指南  
打开```BBS_defender.py```文件，将配置区的内容补全，然后运行，根据提示输入url、守护时间即可，后续动态操作也有提示 
### 关于配置区参数的获取  
1. ```t```。谷歌浏览器（有开发者工具的浏览器都行）进入BBS https://bbs.pku.edu.cn/v2/home.php 打开开发者工具（快捷键：F12），然后登陆，在开发者工具Network选项下面找到login.php这个数据包，里面就有t值，如图：  
![Image load fail](https://github.com/Doublefire-Chen/BDWM_BBS_reminder/blob/main/picture/get_t.png)  
## 鸣谢  
非常感谢下列所有站友帮助测试：（排名不分先后）  
['KakaHiguain', 'Sirius', 'Splindow', 'Seter', 'kkzhiyu', 'cylpku', 'ddvdv', 'jacksonfu', 'Kuroko', 'lxgzg', 'nokay', 'dysyyds', 'jzljlj', 'sugar', 'Raypotter', 'hgj', 'Lorry', 'krgkkkk', 'GWZZ', 'durr', 'kangkangcmr', 'shzmcxk', 'bbsatpku', 'vkzotto', 'tengjingshu', 'UDK']  