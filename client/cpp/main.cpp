// client.cpp

#include <iostream>
#include <thread>
#include <cstdio>
#include <Winsock2.h>
#include <string>
#include "package.h"
#pragma comment( lib, "ws2_32.lib" ) 

using namespace std;

bool nContinue = true;
SOCKET sockClient;

void recvv(const char* buf)
{
	cout << "buf=" << buf << endl;
}

void thread_send()
{
	char send_buf[2048] = { 0 };
	memset(send_buf, 0, 1024);

	//login
	while (1)
	{
		int numid = -1;
		cout << "please input numid:";
		cin >> numid;

		char password[20];
		cout << "please input password:";
		cin >> password;

		if (strlen(password)<6 && strlen(password)>20)
		{
			cout << "password error, please try again";
			continue;
		}

		struct pack_login pa;
		sprintf_s(pa.password, password);
		pa.numid = numid;
		pa.pas_len = strlen(pa.password);
		pa.hand.packlen = sizeof(pa);
		memcpy(send_buf, &pa, sizeof(pa));
		send(sockClient, send_buf, pa.hand.packlen, 0);
		cout << "send login" << endl;
		break;
	}

	while (1)
	{
	loopbegin:
		int itype = -1;
		cout << "please input package type:";
		cin >> itype;
		
		switch (itype)
		{
		case PACK_TYPE_ACTION:
		{
								 int actType = -1;
								 cout << "please input actType:";
								 cin >> actType;

								 char talk[100];
								 cout << "please input package data:";
								 cin >> talk;

								 struct pack_action pa;
								 sprintf_s(pa.buf, talk);
								 pa.actType = actType;
								 pa.len_buf = strlen(pa.buf);
								 pa.hand.packlen = sizeof(pa);
								 memcpy(send_buf, &pa, sizeof(pa));
								 send(sockClient, send_buf, pa.hand.packlen, 0);
								 break;
		}
		default:
		{
				   cout << "type error,please try again!" << endl;
				   break;
		}
		}

		//exit(0);
	}
loopend:
	//nContinue = false;
	cout << "communication end because client use quit" << endl;
	return;
}

void recv_package(char* buf)
{
	char b_buf[10] = { 0 };
	struct packhand ps;
	memset(&ps, 0, sizeof(ps));
	memcpy(&ps, buf, sizeof(ps));

	switch (ps.type)
	{
	case PACK_TYPE_ACTION:
	{
							 cout << endl;
							 cout << "recv a action package" << endl;
							 struct pack_action pa;
							 memcpy(&pa, buf, sizeof(pa));
							 cout << "actType=" << pa.actType << endl;
							 pa.buf[pa.len_buf] = '\0';
							 cout << "buf=" << pa.buf << endl;
							 sprintf_s(b_buf, pa.buf);
							 break;
	}
	case PACK_TYPE_QUIT:
	{
						   cout << endl;
						   struct pack_quit pa;
						   memcpy(&pa, buf, sizeof(pa));
						   pa.msg[pa.len_msg] = '\0';
						   cout << "recv a quit package,case=" << pa.msg << endl;
						   getchar();
						   exit(0);
						   return;
	}
	case PACK_TYPE_PLAYERDATA:
	{
								 struct pack_playerdata pa;
								 memcpy(&pa, buf, sizeof(pa));
								 cout << endl;
								 cout << "player data:numid=" << pa.numid << endl;
								 break;
	}
	default:
		break;
	}

	return;
}

int main()
{
	WORD wVersionRequested;
	WSADATA wsaData;
	int err;

	wVersionRequested = MAKEWORD(1, 1);

	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) {
		return -1;
	}

	if (LOBYTE(wsaData.wVersion) != 1 || HIBYTE(wsaData.wVersion) != 1) {
		WSACleanup();
		return -1;
	}

	sockClient = socket(AF_INET, SOCK_STREAM, 0);	

	SOCKADDR_IN addrSrv;
	addrSrv.sin_addr.S_un.S_addr = inet_addr("106.14.144.43");
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(8300);
	connect(sockClient, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));

	thread t1(thread_send);

	while (nContinue){

		char recvBuf[1024];
		recv(sockClient, recvBuf, 1024, 0);
		recv_package(recvBuf);

	}

	t1.join();
	closesocket(sockClient);
	WSACleanup();

	return 0;
}







