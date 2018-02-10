using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class testScoket : MonoBehaviour {

    public string ip = "";
    public int port = 0;
    public GameObject mCube;
    public bool IsConnected = false;

    private static Socket clientSocket;
    private int interval = 0;
    private int times = 0;

    void Start () {
        clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        connectSocket(ip,port);
        interval = 0;
        times = 0;
    }
	
	void Update () {
		if(IsConnected)
        {
            if (Input.GetKeyUp(KeyCode.W))
            {
                pack_action act = new pack_action("W");
                byte[] buf = act.pack();
                clientSocket.Send(buf);

                pack_position pos = new pack_position(0.001f,1.11f,9.99f);
                byte[] buf2 = pos.pack();
                clientSocket.Send(buf2);
                Debug.Log("send all success");
            }
        }
	}

    void connectSocket(string ip, int port)
    {
        IPAddress mIp = IPAddress.Parse(ip);
        IPEndPoint ip_end_point = new IPEndPoint(mIp, port);

        try
        {
            clientSocket.Connect(ip_end_point);
            IsConnected = true;
            Debug.Log("连接服务器成功,ip=" + ip + ",port=" + port);
        }
        catch
        {
            IsConnected = false;
            Debug.Log("连接服务器失败,ip=" + ip + ",port=" + port);
            return;
        }

        pack_login pack = new pack_login(123, "123");
        byte[] buf = pack.pack();
        clientSocket.Send(buf);
    }
    
}
