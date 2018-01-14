using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.Runtime.InteropServices;

namespace SocketClient
{
    class Program
    {
        private static byte[] result = new byte[1024];
        static void Main(string[] args)
        {
            //设定服务器IP地址
            IPAddress ip = IPAddress.Parse("106.14.144.43");
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                clientSocket.Connect(new IPEndPoint(ip, 8300)); //配置服务器IP与端口
                Console.WriteLine("连接服务器成功");
            }
            catch
            {
                Console.WriteLine("连接服务器失败，请按回车键退出！");
                return;
            }

            pack_login pack = new pack_login(123,"123");
            //Console.WriteLine("send pack len={0}" + Marshal.SizeOf(pack));
            //Console.WriteLine("send hand len={0}" + Marshal.SizeOf(pack.hand));
            //Console.WriteLine("send numid len={0}" + Marshal.SizeOf(pack.numid));
            byte[] buf = pack.pack();
            //string hex = BitConverter.ToString(buf, 0).Replace("-", string.Empty).ToLower();
            //Console.WriteLine("向服务器发送消息：{0}" + hex);
            clientSocket.Send(buf);
            //Console.WriteLine("发送完毕，按回车键退出");

            int receiveLength = clientSocket.Receive(result);
            pack_playerdata playerdata = new pack_playerdata();
            playerdata.make(result);
            Console.WriteLine("收到消息:type=" + playerdata.hand.type + ",len=" + playerdata.hand.packlen + ",numid=" + playerdata.numid);

            Console.ReadLine();
        }

    }
}
