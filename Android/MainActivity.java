package com.example.lingez.firstapp;

import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.json.JSONObject;

import java.io.File;

import io.socket.client.Socket;
import io.socket.emitter.Emitter;

public class MainActivity extends AppCompatActivity {

    private Button btn_sad;
    private Button btn_hpy;
    private Button btn_ang;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        conn();

        btn_sad = (Button) findViewById(R.id.btn_sad);
        btn_hpy = (Button) findViewById(R.id.btn_hpy);
        btn_ang = (Button) findViewById(R.id.btn_ang);

       btn_ang.setOnClickListener(
               new View.OnClickListener() {
                   @Override
                   public void onClick(View v) {
                       Intent intent = new Intent();
                       intent.setAction(android.content.Intent.ACTION_VIEW);
                       String filepath = Environment.getExternalStoragePublicDirectory((Environment.DIRECTORY_MUSIC)).toString();
                       System.out.println(filepath);
                       filepath = filepath.concat("/Scream.mp3");
                       File file = new File(filepath);
                       Log.d("Error", filepath);
                       intent.setDataAndType(Uri.fromFile(file), "audio/*");
                       startActivity(intent);
                   }
               }
       );
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

            socket.on("incoming", new Emitter.Listener() {

                @Override
                public void call(final Object... args) {
                    Log.d("Error", args.toString());
                    JSONObject jsonObject = (JSONObject) args[0];
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
