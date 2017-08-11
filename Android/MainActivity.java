package com.example.lingez.firstapp;

import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;

import io.socket.client.Socket;
import io.socket.emitter.Emitter;

public class MainActivity extends AppCompatActivity {

    private Button btn_sad;
    private Button btn_hpy;
    private Button btn_ang;
    private TextView mTVUsername;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        conn();

        mTVUsername = (TextView) findViewById(R.id.user_name);

//        btn_sad = (Button) findViewById(R.id.btn_sad);
//        btn_hpy = (Button) findViewById(R.id.btn_hpy);
//        btn_ang = (Button) findViewById(R.id.btn_ang);
//
//        btn_sad.setOnClickListener(
//                new View.OnClickListener() {
//                    @Override
//                    public void onClick(View v) {
//                        playMusic("/When I Was Your Man.mp3");
//                    }
//                }
//        );
//
//        btn_hpy.setOnClickListener(
//                new View.OnClickListener() {
//                    @Override
//                    public void onClick(View v) {
//                        playMusic("/Happy.mp3");
//                    }
//                }
//        );
//
//       btn_ang.setOnClickListener(
//               new View.OnClickListener() {
//                   @Override
//                   public void onClick(View v) {
//                       playMusic("/Scream.mp3");
//                   }
//               }
//       );
    }

    public void playMusic(String filename){
        Intent intent = new Intent();
        intent.setAction(android.content.Intent.ACTION_VIEW);
        String filepath = Environment.getExternalStoragePublicDirectory((Environment.DIRECTORY_MUSIC)).toString();
        System.out.println(filepath);
        filepath = filepath.concat(filename);
        File file = new File(filepath);
        Log.d("Error", filepath);
        intent.setDataAndType(Uri.fromFile(file), "audio/*");
        startActivity(intent);
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

            socket.on("data4android", new Emitter.Listener() {

                @Override
                public void call(final Object... args) {
                    Log.d("Error", args.toString());
                    JSONObject jsonObject = (JSONObject) args[0];

                    String emo  = "";
                    String usr_Name = "";

                    try {
                        emo = (String)  jsonObject.get("emotion");
                        usr_Name = (String) jsonObject.get("name");
                        Log.d("Error", emo);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    final String finalUsr_Name = usr_Name;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mTVUsername.setText(finalUsr_Name);
                        }
                    });

                    if(emo.equals("Happy")){
                        playMusic("/Happy.mp3");
                    }
                    else if(emo.equals("Sad")){
                        playMusic("/When I Was Your Man.mp3");
                    }
                    else if(emo.equals("Angry")){
                        playMusic("/Scream.mp3");
                    }
                }



            }).on(Socket.EVENT_DISCONNECT, new Emitter.Listener() {

                @Override
                public void call(Object... args) {
                    //Log.d(TAG, "Disconnected");
                }
            });

            socket.connect();
        }catch (Exception e){

        }

    }


}
