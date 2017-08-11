package com.example.lingez.firstapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import io.socket.client.Socket;
import io.socket.emitter.Emitter;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        conn();
    }

    public void conn() {
        try {
            connection app = new connection();
            final Socket socket = app.getSocket();

            socket.on(Socket.EVENT_CONNECT, new Emitter.Listener() {

                @Override
                public void call(Object... args) {
                    socket.emit("foo", "hi");
                }

            });

            //socket.on("incoming", new Emitter.Listener() {

//                @Override
//                public void call(final Object... args) {
//                    Log.d(TAG, args.toString());
//                    JSONObject jsonObject = (JSONObject) args[0];
//                    String x = null;
//                    int y = 0;
//                    try {
//                        x = (String) jsonObject.get("test");
//                        y = (int) jsonObject.get("time");
//                    } catch (JSONException e) {
//                        e.printStackTrace();
//                    }
//                    System.out.println(jsonObject.toString());
//                    System.out.println(x);
//                    if(x.equals("forward")){
//                        send2Server("F", y);
//                    }else if(x.equals("backward")){
//                        send2Server("B", y);
//                    }else if(x.equals("right")){
//                        send2Server("R", y);
//                    }else if(x.equals("left")){
//                        send2Server("L", y);
//                    }
//                }

//            }).on(Socket.EVENT_DISCONNECT, new Emitter.Listener() {
//
//                @Override
//                public void call(Object... args) {
//                    //Log.d(TAG, "Disconnected");
//                }
//            });

            socket.connect();
        }catch (Exception e){

        }

    }


}
