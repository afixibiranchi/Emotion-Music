package com.example.lingez.firstapp;

/**
 * Created by LINGEZ on 11/8/2017.
 */

import android.util.Log;

import io.socket.client.IO;
import io.socket.client.Socket;


public class connection extends MainActivity {

    Socket mSocket;
    public Socket getSocket(){
        if(mSocket==null){
            try{
                mSocket= IO.socket("http://192.168.10.112:2222");
            }catch (Exception e){
                e.printStackTrace();
                Log.d("error connecting","to server");
            }
        }

        return mSocket;
    }
}
