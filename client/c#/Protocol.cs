using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Net;

namespace SocketClient
{
    enum HANDTYPE
    {
        PACK_TYPE = 0,
        PACK_TYPE_LOGIN,
        PACK_TYPE_ACTION,
        PACK_TYPE_QUIT,
        PACK_TYPE_DEFAULT,
        PACK_TYPE_PLAYERDATA
    }

    public class ProtocolBase
    {
        public int type;
        public int packlen;

        private int nowindex;
        private byte[] buf = new byte[2048];
        private List<byte> byteSource = new List<byte>();

        public ProtocolBase() 
        {
            this.type = (int)HANDTYPE.PACK_TYPE;
            this.packlen = 0;
            this.nowindex = 0;
        }

        //-------------------------------------------------------------------------------recv byte
        /// <summary>
        /// buf >> class
        /// 解析开始
        /// </summary>
        /// <param name="buf"></param>
        public void makeBegin(byte[] buf)
        {
            this.nowindex = 0;
            this.buf = buf;
            getHand();
        }

        /// <summary>
        /// buf >> class
        /// 解析协议头
        /// </summary>
        private void getHand()
        {
            if (this.buf.Length < nowindex + 8)
                throw new Exception("getHand len err");
            this.type = System.BitConverter.ToInt32(this.buf, 0);
            this.packlen = System.BitConverter.ToInt32(this.buf, 4);
            this.nowindex += 8;
        }

        /// <summary>
        /// buf >> class
        /// 解析Int
        /// </summary>
        /// <returns></returns>
        public int getInt()
        {
            if (this.buf.Length < this.nowindex + 4)
                throw new Exception("getInt len err");
            int num = System.BitConverter.ToInt32(this.buf, this.nowindex);
            this.nowindex += 4;
            return num;
        }

        /// <summary>
        /// buf >> class
        /// 解析string
        /// </summary>
        /// <returns></returns>
        public string getString()
        {
            int len = getInt();
            if (this.buf.Length < this.nowindex + len)
                throw new Exception("getString len err");
            this.nowindex += len;
            return System.BitConverter.ToString(this.buf, nowindex, len);
        }

        //-------------------------------------------------------------------------------create byte
        /// <summary>
        /// class >> buf
        /// 打包开始
        /// </summary>
        public void packBegin()
        {
            this.nowindex = 0;
            this.byteSource.Clear();
            Array.Clear(buf, 0, buf.Length);
            packHand();
        }

        /// <summary>
        /// class >> buf
        /// 打包协议头
        /// </summary>
        private void packHand()
        {
            byteSource.AddRange(getFromInt(this.type));
            byteSource.AddRange(getFromInt(this.packlen));
        }

        /// <summary>
        /// class >> buf
        /// 打包Int
        /// </summary>
        /// <param name="num"></param>
        public void packInt(int num)
        {
            byteSource.AddRange(getFromInt(num));
        }

        /// <summary>
        /// class >> buf
        /// 打包string
        /// </summary>
        /// <param name="str"></param>
        public void packString(string str)
        {
            byteSource.AddRange(getFromInt(str.Length));
            byteSource.AddRange(getFromString(str));
        }

        /// <summary>
        /// class >> buf
        /// 打包结束
        /// </summary>
        /// <returns></returns>
        public byte[] packEnd()
        {
            this.buf = this.byteSource.ToArray();
            replaceHandLen();
            return this.buf;
        }

        /// <summary>
        /// class >> buf
        /// 替换buf的包大小
        /// </summary>
        private void replaceHandLen()
        {
            byte[] lenBuf = getFromInt(this.nowindex);
            for (int i = 4; i < 8; i++)
            {
                this.buf[i] = lenBuf[i - 4];
            }
        }

        private byte[] getFromInt(int num)
        {
            this.nowindex += Marshal.SizeOf(num);
            return BitConverter.GetBytes(num);
        }

        private byte[] getFromString(string str)
        {
            this.nowindex += str.Length;
            return System.Text.Encoding.Default.GetBytes(str);
        }
    }

    public class pack_login : ProtocolBase
    {
        public int numid;
        public string password;

        public pack_login(int numid, string password)
        {
            this.type = (int)HANDTYPE.PACK_TYPE_LOGIN;
            this.numid = numid;
            this.password = password;
        }

        public void make(byte[] buf)
        {
            makeBegin(buf);

            this.numid = getInt();
            this.password = getString();
        }

        public byte[] pack()
        {
            packBegin();

            packInt(this.numid);
            packString(this.password);

            return packEnd();
        }
    }

    public class pack_playerdata : ProtocolBase
    {
        public int numid;

        public void make(byte[] buf)
        {
            makeBegin(buf);

            this.numid = getInt();
        }
    }
}