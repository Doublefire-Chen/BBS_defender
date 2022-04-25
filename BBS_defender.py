# coding:utf-8
#申明编码的注释必须放在最上面
#Author:Doublefire.Chen
#Author_BBS_id:Bigscience
#last_modified_time:2022年04月25日19:28:06
#version:3.0
#location:HSC of PKU or BJMU(dawu,23333)
import requests
import re
import time
import threading
import random
import datetime
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode,quote
################配置区####################
ur_username="" #填入你的用户名
password="" #填入你的密码
t='' #填入你的data form里面的t
signature= #填入你发站内信想用的的签名档，按顺序，从上往下数，个数减一，比如你想用第4个，这里就填3，不要加引号
play_with_watern_flag=1 #是否调戏水n（调戏：在守护通知帖成功复活后跟水n讲家乡话），是填1，否填0
#下面的是家乡话，可自行修改
holly_shit=["你能主动来送（ ）真是太好了","赵家的（ ）又来删帖了","你删你（ ）呢","你删你（ ）了个（ ）","你就不怕被（ ）（ ）（ ）创（ ）吗","你（ ）什么时候（ ）啊？","本机器人为您兢兢业业的工作精神所感动，特意为您献唱一首歌：听我说👂👂👂谢谢你🙏🙏🙏因为有你👉👉👉温暖了四季🌈🌈🌈谢谢你🙏🙏🙏感谢有你👉👉👉世界更美丽🌏🌏🌏我要谢谢你🙏🙏🙏因为有你👉👉👉爱常在心底💃💃💃谢谢你 🙏🙏🙏感谢有你🙇‍♂🙇‍♂🙇‍♂把幸福传递","非常佩服你的大无畏送鹿精神","领导们对于水n的大无畏送鹿精神作出了高度评价，对于水n在此次舆情防控攻坚战上的卓越贡献给予了充分肯定，为表彰水n的所作所为，领导在心里偷偷地号召BBS全站站友向水n同志学习。","您尽管抽楼，我这个机器人好好陪您玩","天天这么抽，不怕手抽筋吗？"]
#########################################
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' #随机字符串的生成，参考：https://blog.csdn.net/qq_32599479/article/details/91042234 本来想用secret的，但是心想：能让大家少装一个包是一个
serial_number = "".join(random.sample(alphabet,24)) #生成序列号作为程序运行唯一标识符
black_id_list=["watern"] #这里我就不需要多说吧（doge）
white_id_list=[] #白名单（id）初始赋值
white_postid_list=[] #白名单（postid）初始赋值
white_postid_list_for_admin=[] #白名单（专为版务删帖设置的）初始赋值
crawled_date_postid=[] #已爬帖子（postid为标识）列表初始赋值
all_userid=[] #已爬用户列表初始赋值
crawl_flag=0 #完成第一遍完整爬取所有页面的flag
complete_flag=0 #完成输入url和守护时间的flag
defender_flag=0 #发布守护通知flag
disapeared_data_postid=[] #被删帖子列表初始赋值
all_poster={} #用于存储所有被爬取帖子内容的字典初始赋值
reborn_num=0 #守护通知复活次数初始赋值
five_kill=[] #五杀荣耀播报用的列表初始赋值
crawl_complete_flag=0 #完成爬取单个页面的flag初始赋值
stop_flag=0 #停止flag初始赋值
defender_postid="tmp" #守护通知postid初始赋值
admin="" #版务列表初始赋值
first_postid={} #存储每一页第一层楼的postid的字典初始赋值
detector_flag=0 #是否进入detector的flag，避免两个detector同时运行
header={
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
'Connection': 'keep-alive',
'Content-Length': '84',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'bbs.pku.edu.cn',
'Origin': 'https://bbs.pku.edu.cn',
'Referer': 'https://bbs.pku.edu.cn/v2/home.php',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"macOS"',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
} #登陆时发送请求包的header初始赋值
data = {
'username': ur_username,
'password': password,
'keepalive': '0',
't': t
} #登陆时发送请求包的data初始赋值
def bomb(soup): #炸楼函数，检测整栋楼是否还在
	global stop_flag #申明全局变量
	bdwm_title=soup.find('div',id="page-content").find('div',id="bdwm-title") #爬bdwm-title
	if str(bdwm_title)=='<div id="bdwm-title">出错啦 - 北大未名BBS</div>': #判断整栋楼是否被拆迁
		print("检测到整栋楼拆迁，是否通知每一位站友，1：是；0：否") #提示性输出
		bomb_flag=input() #必须手动确认，毕竟现实情况很复杂，有些东西不适合全局广播
		if bomb_flag=="1":
			bomb_content="检测到整栋楼拆迁，经"+ur_username+"手动确认，机器自动给每一位参与过讨论的id发送备份"+"\n"+"******************************************************"+"\n" #发信内容初始赋值
			for postid in crawled_date_postid: #遍历，将每一个帖子都合在一起组成发信内容
				bomb_content=bomb_content+all_poster[postid]+"******************************************************"+"\n"
			for id in all_userid: #遍历，给每一个参与过讨论的id发站内信，进行全局广播
				mail(id,"未名BBS守护者自动回复",bomb_content,signature)
				time.sleep(6)
			print("已通知每一位id，程序结束") #提示性输出
			stop_flag=1 #停止程序flag触发
			log_creator() #生成日志
			os._exit(0) #停止
		elif bomb_flag=="0": #输入0就不通知
			print("不进行炸楼通知，程序结束")
			stop_flag=1 #停止程序flag触发
			log_creator() #生成日志
			os._exit(0) #停止
def log_creator(): #生成日志的函数
	filename=serial_number+".txt" #生成文件名
	file=open(filename,'w',encoding='utf-8') #创建文件
	i=0 #循环控制变量
	while i < len(crawled_date_postid): #遍历
		crawled_date_postid[i]=int(crawled_date_postid[i]) #将字符串转化为int，为后面排序做准备
		i=i+1 #循环控制变量
	crawled_date_postid.sort() #按照从小到大的顺序排序，这样生成的日志就是按照时间顺序排列的了
	i=0 #循环控制变量
	while i < len(crawled_date_postid): #遍历
		crawled_date_postid[i]=str(crawled_date_postid[i]) #再将int变成str
		i=i+1 #循环控制变量
	for postid in crawled_date_postid: #变量每一个被爬到的帖子
		file.write(all_poster[postid]+"\n"+"******************************************************"+'\n') #写入内容
	file.close #关闭文件
	print("日志文件生成完毕") #提示性输出
def get_admin(url): #爬取版务的函数
	url=url.replace('post-read.php?',"thread.php?") #将输入的帖子链接替换为版块链接
	url= re.sub(r'threadid=\d+', "mode=topic", url) #同上
	r=requests.get(url) #获取页面内容
	soup=BeautifulSoup(r.text,"html.parser") #解析
	bomb(soup) #炸楼函数
	page_content=soup.find('div',id="page-content") #爬到page_content
	board_head=page_content.find('div',id="board-head") #爬到board-head
	content=board_head.find('div',id="content") #爬到content
	admin=content.find('div',id="admin").get_text().replace("版务:","").strip().replace("\n",",") #获取版务信息
	return admin
def update_cookies(): #更新cookie函数
	global header #申明全局变量
	session = requests.session() #使用session发送请求
	print("尝试连接BBS主页") #提示性输出
	login = session.post('https://bbs.pku.edu.cn/v2/ajax/login.php',data=data,headers=header) #发送登陆请求
	if str(login)=='<Response [200]>': #判断是否登陆成功
		print("登录成功") #提示性输出
	else:
		print("网络错误") #提示性输出
	r = session.get('https://bbs.pku.edu.cn/v2/home.php') #登录后回到主页
	soup=BeautifulSoup(r.text,"html.parser") #解析
	print("解析成功") #提示性输出
	BBS_id = re.search(r'<span data-role="login-username">.+</span>',str(soup)).group(0).replace('<span data-role="login-username">','').replace('</span>','') #正则表达式匹配得到id并删去匹配用的多余字符串
	if BBS_id!="guest": #判断是否登陆成功
		print("登录用户："+BBS_id) #提示性输出
	skey=re.search(r'skey=.+for .bbs.pku.edu.cn/>,',str(login.cookies)).group(0).replace(" for .bbs.pku.edu.cn/>,","") #获取skey
	uid=re.search(r'uid=\d+',str(login.cookies)).group(0) #获取uid
	header["Cookie"]=skey+";"+uid #更新cookie
def get_page_number(url): #获取总页数函数
	r=requests.get(url) #获取页面内容
	soup=BeautifulSoup(r.text,"html.parser") #解析
	bomb(soup) #炸楼函数
	total_page_number=int(re.search(r"<div>/ \d+</div>",str(soup)).group(0).replace("<div>/ ","").replace("</div>","")) #获取总页数
	print("已获取总页数") #提示性输出
	return total_page_number
def get_post_landlord(url): #获取第一层楼postid函数
	r=requests.get(url) #获取页面内容
	soup=BeautifulSoup(r.text,"html.parser") #解析
	bomb(soup) #炸楼函数
	card_list=soup.find('div',class_='card-list') #爬到card_list
	first_div=card_list.find('div',class_='post-card') #爬到past-card
	landlord_postid=re.search(r'data-postid="\d+"',str(first_div)).group(0).replace("data-postid=","").replace('"',"") #获取第一层楼postid
	return landlord_postid
def detector(url): #检测被删帖函数
	global exist_data_postid,reborn_num,five_kill,landlord_postid,defender_postid,first_postid,disapeared_data_postid,detector_flag #申明全局变量
	detector_flag=1
	print("detector（）激活") #提示性输出
	exist_data_postid=[] #现存帖子postid列表初始赋值
	i=len(first_postid) #临时变量i用来控制循环，防止有人发的新帖子刚好是新的一页的第一个帖子，此时first_postid还没有更新
	safe_flag=0 #前面页面是否安全flag
	while i>0: #遍历爬取所有现存帖子的postid
		if safe_flag==1: #前面的页面如果安全就直接break
			break
		url_with_page=url+"&page="+str(i) #将url变成第i页的url
		r=requests.get(url_with_page) #获取页面内容
		soup=BeautifulSoup(r.text,"html.parser") #解析
		bomb(soup) #炸楼函数
		first_post_flag=0
		card_list=soup.find('div',class_='card-list') #爬到card-list
		for post_card in card_list.find_all('div',class_='post-card'): #爬到postcard
			data_postid=re.search(r'data-postid="\d+"',str(post_card)).group(0).replace("data-postid=","").replace('"',"") #获取datapostid
			if data_postid==first_postid[i] and first_post_flag==0: #判断第一个帖子是否变化
				first_postid[i]=data_postid #更新第一个帖子的postid
				print("已更新第"+str(i)+"页第一个帖子的postid")
				print("前面"+str(i-1)+"页都是安全的") #提示性输出
				unsafe_page=i #记录不安全的页面
				safe_flag=1 #改变safe_flag
				first_post_flag=1 #改变first_post_flag
			elif data_postid!=first_postid[i] and first_post_flag==0:
				first_postid[i]=data_postid #更新第一个帖子的postid
				first_post_flag=1 #改变first_post_flag
				print("已更新第"+str(i)+"页第一个帖子的postid")
			if data_postid not in exist_data_postid: #判断这个帖子是否被爬过，防止重复存入
				exist_data_postid.append(data_postid) #如果没被爬就加进去
		i=i-1 #循环控制
	#disapeared_data_postid=set(crawled_date_postid)^set(exist_data_postid) #使用异或运算符找到被删的帖子 #参考：https://blog.csdn.net/qq_40808154/article/details/94591431
	for postid in crawled_date_postid:
		if postid >= first_postid[unsafe_page]:
			if postid not in exist_data_postid and postid not in disapeared_data_postid: #加后面这个判断防止重复爬取
				disapeared_data_postid.append(postid)
				print("发现被删帖子")
	if str(defender_postid) in disapeared_data_postid: #判断守护通知帖是否被删
		reborn_num=reborn_num+1 #被删了重生次数就加一
		now_time=datetime.datetime.now() #获取当前时间
		now_time = now_time.strftime("%Y-%m-%d %H:%M:%S") #格式化时间
		reborn_content="本帖于"+str(now_time)+"自动复活，这是本帖第"+str(reborn_num)+"次复活"+"\n"+"本程序目前设定的运行时间为"+str(running_time)+"小时"+"\n"+defender_content #复活帖内容
		reply(landlord_postid,reborn_content) #发布复活贴
		print("第"+str(reborn_num)+"次复活成功") #提示性输出
		if play_with_watern_flag==1:
			play_content="（本回帖留给我们最最亲爱的水n同志）\n机器都被水n同志的敬业精神所打动，从语料库中自动生成了家乡话\n水n同志，"+random.choice(holly_shit)
			reply(landlord_postid,play_content)
	if len(disapeared_data_postid)!=0: #如果有帖子被删了
		if len(disapeared_data_postid)%5==0: #判断是否为5的整数倍
			five_number=len(disapeared_data_postid)/5 #是的话求出5杀的个数
			five_number=int(five_number) #将浮点数转化为整数
			if five_number not in five_kill: #判断这个五杀是不是之前拿过的
				dead_id="" #被删id字符串初始赋值
				for postid in disapeared_data_postid: #循环爬取被删帖子的id
					poster_id=re.search(r'回帖人:.+\n',all_poster[postid]).group(0).replace("回帖人:","").replace("\n","") #获取id
					dead_id=dead_id+poster_id+"," #组合内容
				dead_id=dead_id.strip(",") #删去最后多余的逗号
				Glory_broadcast_content="*************荣耀播报*************"+"\n"+"让我们恭喜水n在本主题帖拿下第"+str(five_number)+"个五连绝世，让我们来看看有哪些送人头的站友（doge）"+"\n"+"被删帖id（出现n次表示被删帖n次）："+dead_id+"\n"+"最后，让我们回到主旋律上吧："+"\n"+"听我说👂👂👂谢谢你🙏🙏🙏因为有你👉👉👉温暖了四季🌈🌈🌈谢谢你🙏🙏🙏感谢有你👉👉👉世界更美丽🌏🌏🌏我要谢谢你🙏🙏🙏因为有你👉👉👉爱常在心底💃💃💃谢谢你 🙏🙏🙏感谢有你🙇‍♂🙇‍♂🙇‍♂把幸福传递" #生成荣耀播报内容
				reply(landlord_postid,Glory_broadcast_content) #发送荣耀播报
				five_kill.append(five_number) #记录这个五杀
				print("荣耀播报发送成功") #提示性输出
	detector_flag=0
	return disapeared_data_postid 
def mail(username,title,content,signature): #发站内信函数
	update_cookies() #更新cookie
	username='["'+username+'"]' #格式化被发信人
	data_user={"names":username} #同上
	session = requests.session() #使用session发信
	mail_getid=session.post('https://bbs.pku.edu.cn/v2/ajax/get_userinfo_by_names.php',headers=header,data=data_user) #发送站内信预请求，以获取uid
	mail_id=re.search(r'"id":\d+',mail_getid.text).group(0).replace('"id":',"") #获取uid
	mail_data={
	'rcvuids': '['+mail_id+']',
	'title': title,
	'attachpath':"",
	'postinfo': '{}',
	'signature': signature
	} #生成发送请求包所需的data
	now_time=datetime.datetime.now() #获取当前时间
	now_time = now_time.strftime("%Y-%m-%d %H:%M:%S") #格式化时间
	content=content+"\n"+"序列号："+serial_number+"\n"+"本站内信由机器于"+str(now_time)+"自动发送" #生成发信内容
	content='[{"type":"ansi","bold":false,"underline":false,"fore_color":9,"back_color":9,"content":"'+content+'"}]' #格式化发信内容
	mail_data=urlencode(mail_data)+'&content='+quote(content).replace('%0A','%5Cn') #想换行就要这么写，涉及url编码问题
	session = requests.session() #使用session
	mail=session.post('https://bbs.pku.edu.cn/v2/ajax/create_mail.php',headers=header,data=mail_data) #发送站内信
	if '"success":true' in mail.text: #判断是否发送成功
		print("给"+username+"发送站内信成功") #提示性输出
def crawler(page,all_page_number): #爬页面帖子函数
	global crawled_date_postid,crawl_flag,black_id_list,white_id_list,white_postid_list,ur_username,defender_flag,disapeared_data_postid,all_poster,defender_content,crawl_complete_flag,defender_postid,white_postid_list_for_admin,stop_flag,first_postid #申明全局变量
	url_with_page=url+"&page="+str(page) #生成指定页数的url
	r=requests.get(url_with_page) #获取页面内容
	soup=BeautifulSoup(r.text,"html.parser") #解析
	bomb(soup) #炸楼函数
	card_list=soup.find('div',class_='card-list') #爬到card-list
	first_post_flag=0 #爬取第一个帖子的控制flag
	for post_card in card_list.find_all('div',class_='post-card'): #遍历每一个post-card
		data_postid=re.search(r'data-postid="\d+"',str(post_card)).group(0).replace("data-postid=","").replace('"',"") #获取postid
		if first_post_flag==0 and len(first_postid)!=all_page_number: #判断是否为第一个帖子并且没有把每一页都存进去
			first_postid[page]=data_postid #是的话就存下来
			first_post_flag=1 #改变控制flag
			print("已存储当前页面的第一个帖子的postid") #提示性输出
		if data_postid not in crawled_date_postid: #判断这个帖子是否爬过
			print("发现新楼层") #提示性输出
			post_owner=post_card.find('div',class_="post-owner") #爬到poster-owner
			username_rough=post_owner.find('p',class_="username") #粗爬username
			username=username_rough.find('a').get_text() #爬取username
			nickname=post_owner.find('p',class_="nickname text-line-limit").get_text() #爬取昵称
			post_main=post_card.find('div',class_="post-main") #爬到post-main
			content_rough=post_main.find('div',class_="body file-read image-click-view") #爬到内容框
			content="" #回帖内容初始赋值
			for content_element in content_rough.find_all('p',class_=""): #遍历内容的每一个p
				content=content+str(content_element.get_text())+"\n" #组合内容
			content=content[:-1] #用切片的方法删除最后多余的一个换行符
			quote="没有引用，可能是楼主或者机器人\n" #引用内容默认值
			if content_rough.find('p',class_="quotehead")!=None: #判断是否有引用内容
				quote=content_rough.find('p',class_="quotehead").get_text()+'\n' #获取引用的头部信息
			for quote_element in post_main.find_all('p',class_="blockquote"): #获取引用部分的后面内容
				if quote_element!=None: #判断是否存在
					quote=quote+quote_element.get_text()+"\n" #组合内容
			quote=quote[:-1] #用切片的方法删除最后多余的一个换行符
			attachment=post_main.find('div',class_="attachment") #爬到attachment
			attachment_temple="无" #attachment初始赋值
			if attachment!=None: #判断是否为空
				attachment_temple="" #当不是空时重新赋值attachment
				ul=attachment.find('ul') #爬取到列表ul
				li=ul.find_all('li') #找到所有的列表项目
				i=1 #循环控制变量
				for each_attachment in li: #遍历获取附件
					size=each_attachment.find('span',class_="size") #获取文件大小
					if size!=None: #如果size为空，说明该li为缩略图，不是我们想要的
						attachment_name="附件"+str(i)+":"+each_attachment.get_text() #爬取附件文件名称
						attachment_href=each_attachment.find("a").get("href") #爬取附件文件链接
						attachment_temple=attachment_temple+attachment_name+"\n"+"链接："+attachment_href+"\n" #组合内容
						i=i+1 #控制循环
				attachment_temple=attachment_temple[:-1] #用切片的方法删除最后多余的一个换行符
			signature_file_read=post_main.find('div',class_="signature file-read") #爬到signature
			signature="" #signa初始赋值，默认为空
			if signature_file_read != None: #判断是否为空
				for each in signature_file_read: #遍历签名档每一行
					if each != None: #判断是否为空
						signature=signature+each.get_text()+"\n" #组合内容
				signature=signature[:-1] #用切片的方法删除最后多余的一个换行符
			else:
				signature="无" #没有就是无
			operations=post_main.find('div',class_="operations") #爬到操作区
			right=operations.find('div',class_="right") #爬到右边区域
			sl_triangle_container=right.find('div',class_="sl-triangle-container") #爬到下一层
			time_title=sl_triangle_container.find('span',class_="title") #爬到title
			time=time_title.find('span',class_="").get_text() #获取回复时间
			temple="回帖人:"+username+"("+nickname+")"+"\n"+"回复内容:"+content+"\n"+"引用内容:"+"\n"+quote+"\n"+"附件:"+attachment_temple+"\n"+signature+"\n"+"回复时间:"+time+"\n"+"data_postid="+data_postid #组合内容
			'''
			loc = locals() #至于这里为什么这么写，这里涉及局部范围变量问题，是个大坑，太恶心了，debug了几个小时 #参考：https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html
			exec("reply_"+data_postid+"=temple") #动态生成变量  参考：https://blog.csdn.net/weixin_30750335/article/details/99335069
			tmp="reply_"+data_postid
			all_poster[tmp]=loc[tmp]
			发现大可不必这样复杂，我为啥不直接把temple存进字典里面呢，23333
			'''
			all_poster[data_postid]=temple #将爬到的帖子存到字典里去
			print(temple) #提示性输出
			print("*"*50) #分割线
			crawled_date_postid.append(data_postid) #将postid放入爬过的postid列表里面
			if serial_number in content and username==ur_username: #判断序列号是否在内容里面并且判断这是不是程序运行者发的帖子
				defender_postid=data_postid #如果是，就表明该postid为守护回复帖的postid，存起来，后面复活时需要
				print("已定位defender_post") #提示性输出
			if username not in all_userid and username!=ur_username: #判断这个发帖人之前是否被爬过
				all_userid.append(username) #没有被爬过的话就将其存入参与讨论的id列表里，最后炸楼的时候通知需要
			if (content in ["#思想自由，兼容并包","#思想自由,兼容并包","＃思想自由，兼容并包","＃思想自由,兼容并包"]) and (username not in black_id_list) and (data_postid not in white_postid_list) and (crawl_flag!=0): #由于中英文的井号有2种，逗号有2种，为了站友们方便，所以把4种情况都列出来了，黑白名单的请求不会生效，黑名单我就不多说了，白名单的是之前发送的请求，已经处理过，这里判断一下避免二次回复。crawl_flag的作用是确保整栋楼完整的被爬了一边，这样程序运行之前的请求也是无效的。
				print("收到站友"+username+"的请求") #提示性输出
				if detector_flag==0: #判断detector函数是否空闲
					disapeared_data_postid=detector(url) #获取被删帖子的postid
				print("disapeared_data_postid",disapeared_data_postid)
				mail_content="目前无帖子被删除" #站内信内容初始赋值
				if disapeared_data_postid==[]: #判断有无帖子被删
					print("目前无帖子被删除") #提示性输出
					mail(username,"未名BBS守护者自动回复",mail_content,signature) #发送站内信
					white_postid_list.append(data_postid) #将该请求帖子postid加入白名单
					print("请求处理完毕") #提示性输出
				else:
					white_flag=0 #id白名单flag
					mail_content="被删除帖子："+"\n" #初始赋值
					print("进入内容组合")
					for data_postid in disapeared_data_postid: #遍历每一个被删的帖子
						if data_postid not in crawled_date_postid: #如果该帖子没有被爬。有这种情况，就是当程序detector函数正在爬取现有的帖子时正好有一个人发新帖子，那么异或运算就会把这个新帖子当做被删除的帖子。我这里这么写就是为了避免出现这种情况。
							continue #下一个
						if white_id_list==[] and white_postid_list_for_admin==[]: #如果id白名单和postid白名单都是空的
							mail_content=mail_content+all_poster[data_postid]+"\n"+"******************************************************"+"\n" #直接组合内容
						elif white_id_list!=[]: #如果id白名单不为空
							for id in white_id_list: #遍历id白名单的每一个id
								poster_id=re.search(r'回帖人:.+\n',all_poster[data_postid]).group(0) #获取被删除帖子的发帖人id
								if id in poster_id: #如果二者相等
									white_flag=1 #白名单控制flag，后面就不会将这个帖子当成被删除帖子
							if (white_flag==0) and (data_postid not in white_postid_list_for_admin): #入股白名单控制flag没被改动（说明这个帖子不是id白名单里的人发的）并且postid不在postid白名单里面
								mail_content=mail_content+all_poster[data_postid]+"\n"+"******************************************************"+"\n" #组合内容
						elif white_postid_list_for_admin!=[]: #如果版务postid白名单不是空的
							if data_postid not in white_postid_list_for_admin: #如果被删帖子postid不在版务postid白名单里面
								mail_content=mail_content+all_poster[data_postid]+"\n"+"******************************************************"+"\n" #组合内容
					if mail_content=="被删除帖子：\n": #如果发件内容没被更改
						mail_content="目前无帖子被删除" #说明目前没有帖子被删除
					#if username!=ur_username: #还要判断这个请求是不是自己发起的
					mail(username,"未名BBS守护者自动回复",mail_content,signature) #不是的话就发送站内信
					#else: #如果这个请求是自己发的
						#print("判定为自己给自己发送请求，目的是激活detector()，不会给自己发送站内信的，内容直接输出到终端") #提示性输出
						#print(mail_content) #在终端直接输出被删除帖子内容，因为自己不能给自己发站内信#2022年04月25日06:00:55，今天发现原来自己可以给自己发站内信，哈哈哈，那还挺好的
					white_postid_list.append(data_postid) #将该请求加入白名单，因为已经回复过了
					print("请求处理完毕") #提示性输出
			if (content in ["#自删","＃自删"]) and (crawl_flag!=0): #判断是否为自删请求
				print("收到站友"+username+"的请求") #提示性输出
				white_id_list.append(username) #将该站友的id加入id白名单
				reply_content="已添加进入白名单，可自行删帖" #回复内容赋值
				mail(username,"未名BBS守护者自动回复",reply_content,signature) #发送站内信
				print("请求处理完毕") #提示性输出
			if ("#删帖原因" in content or "＃删帖原因" in content) and (username in admin) and (crawl_flag!=0): #判断是否为版务删帖请求
				print("检测到版务"+username+"的删帖请求") #提示性输出
				postid=re.search(r'postid=\d+',content).group(0).replace("postid=","") #获取版务想要删帖的postid
				white_postid_list_for_admin.append(postid) #将该postid加入白名单
				reply_content="已添加进入白名单，可自行删帖" #回复内容赋值
				mail(username,"未名BBS守护者自动回复",reply_content,signature) #发送站内信
				print("请求处理完毕") #提示性输出
		else:
			crawl_complete_flag=1 #表明该页面已经爬完了
		if stop_flag==1: #终止flag判断
			print("进入终止") #提示性输出
			log_creator() #生成日志
			now_time=datetime.datetime.now() #获取当前时间
			now_time = now_time.strftime("%Y-%m-%d %H:%M:%S") #格式化时间
			quit_content="本程序于"+str(now_time)+"停止运行（有可能是时间到了，也有可能是"+ur_username+"手动停了）" #回帖内容赋值
			reply(landlord_postid,quit_content) #回帖
			os._exit(0) #结束程序
	print("第"+str(page)+"页爬取完毕") #提示性输出
def main(): #主函数
	global crawled_date_postid,crawl_flag,start_time,bid,complete_flag,url,defender_flag,running_time,defender_content,landlord_postid,stop_flag,admin #申明全局变量
	start_time=datetime.datetime.now() #获取程序开始运行的时间
	url=input("请输入您想要守护的主题帖的链接:") #输入想要守护的主题帖的链接
	running_time=input("请输入运行时间（请输入整数，单位：小时）:") #输入想要守护的时间
	running_time=int(running_time) #将字符串变量转化为整数
	url=re.sub(r'&page=\d+',"",url) #格式化url，无论用户输入第几页的链接，这里都会使之变为第一页的链接
	complete_flag=1 #输入完成flag #是complete，不是compelete!!!
	bid=re.search(r'bid=\d+',url).group(0).replace("bid=","") #获取url中的bid
	total_page_number=get_page_number(url) #获取总页数
	tmp_page=total_page_number #临时变量存储总页数
	admin=get_admin(url) #获取版务
	if defender_flag==0: #判断守护通知是否发出
		landlord_postid=get_post_landlord(url) #获取一楼的postid
		defender_content=ur_username+"于"+str(start_time)+"为本主题帖运行未名BBS守护者程序"+"\n"+"守护时间："+str(running_time)+"小时"+"\n"+"版本号：公测v3.0"+"\n"+"项目地址：https://github.com/Doublefire-Chen/BBS_defender"+"\n"+"本版块版务："+admin+"\n"+"###以下所有回复内容均不要引号，不要中间的加号，不要句号，不要加多余的字符###"+"\n"+"回复“#+思想自由，兼容并包”查看被删除帖子（站内信形式）"+"\n"+"回复“#+自删”即可将自己的id加入白名单（请在收到站内信提示后再删帖）"+"\n"+"版务回复：“#+删帖postid=#+删帖原因：”即可将该postid加入白名单（未写明删帖原因视为无效回复）（请在收到站内信提示后删帖）" #回复内容赋值
		reply(landlord_postid,defender_content) #回帖
		print("已发布守护通知") #提示性输出
	while True:
		r=requests.get(url) #获取内容
		soup=BeautifulSoup(r.text,"html.parser") #解析
		bomb(soup) #炸楼函数
		if tmp_page<=get_page_number(url): #如果当前页数比总页数小
			crawler(tmp_page,total_page_number) #爬
		else: #如果当前页数比总页数还大
			tmp_page=get_page_number(url) #重新获取总页数
			print("页数减少") #说明删帖导致楼层数减少
		if tmp_page==1 or crawl_complete_flag!=0: #如果爬到了第一页或者爬取一页的flag改变了
			tmp_page=get_page_number(url) #更新总页数
			crawl_flag=1 #说明完整的爬完了一次整栋楼
			defender_flag=1	#守护通知flag改变
			time.sleep(6) #禁止擅自修改这个数值！！！违者后果自负！！！这是贵站允许的最大爬取频率了，再高就有可能被视为网络攻击
			continue #继续
		else:
			tmp_page=tmp_page-1 #页数减一
			time.sleep(6) #禁止擅自修改这个数值！！！违者后果自负！！！这是贵站允许的最大爬取频率了，再高就有可能被视为网络攻击
def controller(): #控制器函数
	global stop_flag,complete_flag,running_time #申明全局变量
	stop_flag=0 #停止flag初始赋值
	while True:
		if complete_flag==1: #如果用户的输入完成了
			while True:
				time.sleep(10) #等10秒
				print("输入指令，结束程序请输入q，延长运行时间请输入+n，缩短运行时间请输入-n,（n为整数，单位：小时）") #提示性输出
				command=input() #输入指令
				if command=="q": #判断指令类型
					stop_flag=1 #停止flag改变
					print("结束程序") #提示性输出
					quit() #没用os._quit(0)，因为日志还没有生成
				elif "+" in command: #判断指令类型
					command=command.replace("+","") #删去加号
					add_time=int(command) #字符串变量转整数变量
					running_time=running_time+add_time #加时
					now_time=datetime.datetime.now() #获取现在时间
					landlord_postid=get_post_landlord(url) #获取一楼postid
					inform_content=ur_username+"于"+str(now_time)+"为本守护程序延长运行时间"+str(add_time)+"小时"+"\n"+ur_username+"于"+str(start_time)+"开始为本主题帖运行未名BBS守护者程序"+"\n"+"目前设定的运行时间为"+str(running_time)+"小时" #回帖内容赋值
					reply(landlord_postid,inform_content) #回帖
					print("加时成功") #提示性输出
					command="" #更新命令
					del add_time #释放add_time内存
				elif "-" in command: #判断指令类型
					command=command.replace("-","") #删去减号
					sub_time=int(command) #字符串变量转整数变量
					running_time=running_time-sub_time #减时
					now_time=datetime.datetime.now() #获取当前时间
					landlord_postid=get_post_landlord(url) #获取一楼的postid
					inform_content=ur_username+"于"+str(now_time)+"为本守护程序减少运行时间"+str(sub_time)+"小时"+"\n"+ur_username+"于"+str(start_time)+"开始为本主题帖运行未名BBS守护者程序"+"\n"+"目前设定的运行时间为"+str(running_time)+"小时" #回帖内容赋值
					reply(landlord_postid,inform_content) #回帖
					print("减时成功") #提示性输出
					command="" #更新命令
					del sub_time #释放sub_time内存
				else:
					print("输入命令有误，或者是两个输入发生了冲突，请重新输入") #提示性输出
def reply(parentid,reply_content): #回帖函数
	global bid,signature #申明全局变量
	actionid=random.randint(1,1000000) #随机数生成
	reply_data={
	'title': '未名BBS守护者',
	'attachpath': '',
	'actionid':actionid,
	'bid':bid,
	'signature':signature,
	'postinfo': '{"parentid":'+parentid+',"mail_re":true}',
	} #发送请求所需的data赋值
	now_time=datetime.datetime.now() #获取当前时间
	now_time = now_time.strftime("%Y-%m-%d %H:%M:%S") #格式化时间
	reply_content=reply_content+"\n"+"序列号："+serial_number+"\n"+"本帖由机器于"+str(now_time)+"自动发送" #回帖内容赋值
	content='[{"type":"ansi","bold":false,"underline":false,"fore_color":9,"back_color":9,"content":"'+reply_content+'"}]' #回帖内容格式化，堆代码的时候后面多粘了个逗号，debug了半天，气死我了😤，加了逗号老是认为这是数组变量而不是字符串变量
	reply_data=urlencode(reply_data)+'&content='+quote(content).replace('%0A','%5Cn') #想换行就要这么写，涉及url编码问题
	update_cookies() #更新cookie
	session = requests.session() #使用session
	reply=session.post("https://bbs.pku.edu.cn/v2/ajax/create_post.php",headers=header,data=reply_data) #发送回帖请求
	if '"success":true' in reply.text: #判断是否回帖成功
		print("给parentid="+parentid+"回帖成功") #提示性输出
def time_controler(): #计时器函数
	global start_time,running_time,stop_flag #申明全局变量
	running_time=1 #运行时间初始赋值
	while True:
		if complete_flag==1: #判断用户是否完成了输入
			while True: #完成输入后才能运行计时器函数
				if stop_flag==1: #如果停止flag被改变
					quit() #就停止，不能用os_quit(0)，因为还没有生成日志
				running_time_seconds=running_time*3600 #把小时变成秒
				now_time=datetime.datetime.now() #获取当前时间
				time_interval=now_time-start_time #获取时间间隔
				print("time_interval",time_interval) #提示性输出
				print("设定运行时间为"+str(running_time_seconds)+"秒") #提示性输出
				if time_interval>=datetime.timedelta(seconds=running_time_seconds): #判断时间到了没有
					print("时间到") #提示性输出
					stop_flag=1 #改变停止flag，赋值时再写2个等号我就是梁志超他奶奶
					quit() #停止本线程，不能用os_quit(0)，因为还没有生成日志
				else:
					time.sleep(1800) #睡他半个小时
def auto_detector(): #自动监测函数
	global disapeared_data_postid
	while True:
		if crawl_flag!=0: #当第一遍完整爬取后	
			time.sleep(12) #睡12秒
			if detector_flag==0: #判断detector函数是否空闲
				disapeared_data_postid=detector(url) #监测
			print("定时自动爬取，同时看看守护通知帖子还在不在") #提示性输出
			if stop_flag==1: #如果停止flag被改变
				quit() #就停止

t1=threading.Thread(target=controller) #申明第一个线程
t2=threading.Thread(target=main) #申明第二个线程
t3=threading.Thread(target=time_controler) #申明第三个线程
t4=threading.Thread(target=auto_detector) #申明第四个线程
t1.start() #运行第一个线程
t2.start() #运行第二个线程
t3.start() #运行第三个线程
t4.start() #运行第四个线程
