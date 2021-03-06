﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;

enum HANDTYPE
{
    PACK_TYPE_LOGIN = 1,
    PACK_TYPE_ACTION,
    PACK_TYPE_QUIT,
    PACK_TYPE_DEFAULT,
    PACK_TYPE_PLAYERDATA,
    PACK_TYPE_POSITION,
}
public class ProtocolBase
{
    public static byte[] StructToBytes<T>(T structType)
    {
        int size = Marshal.SizeOf(structType);
        byte[] bytes = new byte[size];
        IntPtr structPtr = Marshal.AllocHGlobal(size);
        Marshal.StructureToPtr(structType, structPtr, false);
        Marshal.Copy(structPtr, bytes, 0, size);
        Marshal.FreeHGlobal(structPtr);
        return bytes;
    }

    //-------------------------------------------------------------------------------recv byte
    public static packhand getHand(byte[] buf, ref int nowindex)
    {
        if (buf.Length < nowindex + 8)
            throw new Exception("getHand len err");
        int type = System.BitConverter.ToInt32(buf, 0);
        //type = IPAddress.NetworkToHostOrder(type);
        int packlen = System.BitConverter.ToInt32(buf, 4);
        //packlen = IPAddress.NetworkToHostOrder(packlen);
        packhand hand = new packhand(type, packlen);
        nowindex += 8;
        return hand;
    }

    public static int getInt(byte[] buf, ref int nowindex)
    {
        if (buf.Length < nowindex + 4)
            throw new Exception("getInt len err");
        int num = System.BitConverter.ToInt32(buf, nowindex);
        nowindex += 4;
        return num;
    }

    public static float getFloat(byte[] buf, ref int nowindex)
    {
        if (buf.Length < nowindex + 4)
            throw new Exception("getInt len err");
        float num = System.BitConverter.ToSingle(buf, nowindex);
        nowindex += 4;
        return num;
    }

    public static string getString(byte[] buf, ref int nowindex, int srclen)
    {
        if (buf.Length < nowindex + srclen)
            throw new Exception("getString len err");
        nowindex += srclen;
        return System.BitConverter.ToString(buf, nowindex, srclen);
    }

    //-------------------------------------------------------------------------------create byte
    public static void replaceHandLen(ref byte[] buf, int nowsize)
    {
        byte[] lenBuf = getFromInt(nowsize, ref nowsize);
        for (int i = 4; i < 8; i++)
        {
            buf[i] = lenBuf[i - 4];
        }
    }

    public static byte[] getFromInt(int num, ref int nowsize)
    {
        nowsize += Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    public static byte[] getFromFloat(float num, ref int nowsize)
    {
        nowsize += Marshal.SizeOf(num);
        return BitConverter.GetBytes(num);
    }

    public static byte[] getFromString(string str, ref int nowsize)
    {
        nowsize += str.Length;
        return System.Text.Encoding.Default.GetBytes(str);
    }
}

public struct packhand
{
    public int type;
    public int packlen;

    public packhand(int type, int packlen)
    {
        this.type = type;
        this.packlen = packlen;
    }

    public byte[] pack(ref int nowsize)
    {
        ProtocolBase b = new ProtocolBase();
        List<byte> byteSource = new List<byte>();
        byteSource.AddRange(ProtocolBase.getFromInt(this.type, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromInt(this.packlen, ref nowsize));
        return byteSource.ToArray();
    }
}

public struct pack_login
{
    public packhand hand;
    public int numid;
    public int len_pwd;
    public string password;

    public pack_login(int numid, string password)
    {
        this.hand = new packhand((int)HANDTYPE.PACK_TYPE_LOGIN, 0);
        this.numid = numid;
        this.len_pwd = password.Length;
        this.password = password;
    }

    public void make(byte[] buf)
    {
        int nowindex = 0;

        this.hand = ProtocolBase.getHand(buf, ref nowindex);
        this.numid = ProtocolBase.getInt(buf, ref nowindex);
        this.len_pwd = ProtocolBase.getInt(buf, ref nowindex);
        this.password = ProtocolBase.getString(buf, ref nowindex, this.len_pwd);
    }

    public byte[] pack()
    {
        int nowsize = 0;
        List<byte> byteSource = new List<byte>();

        byteSource.AddRange(this.hand.pack(ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromInt(this.numid, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromInt(this.password.Length, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromString(this.password, ref nowsize));

        byte[] buf = byteSource.ToArray();
        ProtocolBase.replaceHandLen(ref buf, nowsize);
        return buf;
    }
}

public struct pack_action
{
    public packhand hand;
    public int len_buf;
    public string buf;

    public pack_action(string buf)
    {
        this.hand = new packhand((int)HANDTYPE.PACK_TYPE_ACTION, 0);
        this.len_buf = buf.Length;
        this.buf = buf;
    }

    public void make(byte[] buf)
    {
        int nowindex = 0;

        this.hand = ProtocolBase.getHand(buf, ref nowindex);
        this.len_buf = ProtocolBase.getInt(buf, ref nowindex);
        this.buf = ProtocolBase.getString(buf, ref nowindex, this.len_buf);
    }

    public byte[] pack()
    {
        int nowsize = 0;
        List<byte> byteSource = new List<byte>();

        byteSource.AddRange(this.hand.pack(ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromInt(this.len_buf, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromString(this.buf, ref nowsize));

        byte[] buf = byteSource.ToArray();
        ProtocolBase.replaceHandLen(ref buf, nowsize);
        return buf;
    }
}

public struct pack_playerdata
{
    public packhand hand;
    public int numid;

    public void make(byte[] buf)
    {
        int nowindex = 0;

        this.hand = ProtocolBase.getHand(buf, ref nowindex);
        this.numid = ProtocolBase.getInt(buf, ref nowindex);
    }
}

public struct pack_position
{
    public packhand hand;
    public float x;
    public float y;
    public float z;
    public pack_position(float x, float y, float z)
    {
        this.hand = new packhand((int)HANDTYPE.PACK_TYPE_POSITION, 0);
        this.x = x;
        this.y = y;
        this.z = z;
    }
    public void make(byte[] buf)
    {
        int nowindex = 0;

        this.hand = ProtocolBase.getHand(buf, ref nowindex);
        this.x = ProtocolBase.getFloat(buf, ref nowindex);
        this.y = ProtocolBase.getFloat(buf, ref nowindex);
        this.z = ProtocolBase.getFloat(buf, ref nowindex);
    }

    public byte[] pack()
    {
        int nowsize = 0;
        List<byte> byteSource = new List<byte>();

        byteSource.AddRange(this.hand.pack(ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromFloat(this.x, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromFloat(this.y, ref nowsize));
        byteSource.AddRange(ProtocolBase.getFromFloat(this.z, ref nowsize));

        byte[] buf = byteSource.ToArray();
        ProtocolBase.replaceHandLen(ref buf, nowsize);
        return buf;
    }
}
