#ifndef __PACKAGE_H__
#define __PACKAGE_H__

enum
{
	PACK_TYPE_LOGIN = 1,
	PACK_TYPE_ACTION,
	PACK_TYPE_QUIT,
	PACK_TYPE_DEFAULT,
	PACK_TYPE_PLAYERDATA,
};

struct packhand
{
	int type;
	int packlen;
	packhand(){ type = 0; packlen = 0; }
};

struct pack_login
{
	packhand hand;
	int numid;
	int pas_len;
	char password[20];
	pack_login(){ hand.type = PACK_TYPE_LOGIN; }
};

struct pack_action
{
	packhand hand;
	int actType;
	int len_buf;
	char buf[10];
	pack_action(){ hand.type = PACK_TYPE_ACTION; }
};

struct pack_quit
{
	packhand hand;
	int len_msg;
	char msg[64];
	pack_quit(){ hand.type = PACK_TYPE_QUIT; }
};

struct pack_default
{
	packhand hand;
	int num;
	pack_default(){ hand.type = PACK_TYPE_DEFAULT; }
};

struct pack_playerdata
{
	packhand hand;
	int numid;
	pack_playerdata(){ hand.type = PACK_TYPE_PLAYERDATA; }
};

#endif