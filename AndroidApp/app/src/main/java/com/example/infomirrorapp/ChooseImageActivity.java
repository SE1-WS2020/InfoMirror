package com.example.infomirrorapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ChooseImageActivity extends AppCompatActivity {
    private TextView debugText;
    private ImageView imageView;
    private Button chooseFileButton;
    private Button uploadFileButton;
    private final int IMG_REQUEST = 1;
    private Bitmap bitmap;
    private Uri imagePath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choose_image);
        debugText = findViewById(R.id.debugText);
        imageView = findViewById(R.id.imageView);
        chooseFileButton = findViewById(R.id.chooseFileButton);
        uploadFileButton = findViewById(R.id.uploadButton);
    }

    public void onChooseFileButtonClick(View view) {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent, IMG_REQUEST);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == IMG_REQUEST && resultCode == RESULT_OK && data != null) {
            this.imagePath = Uri.parse(data.getData().getPath());
            try {
                bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), data.getData());
                this.imageView.setImageBitmap(bitmap);
                this.imageView.setVisibility(View.VISIBLE);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void onUploadFileButtonClick(View view) {
        String apiUrl = "http://192.168.178.66:8000/api/upload_image/";

        OkHttpClient client = new OkHttpClient().newBuilder().build();

        MediaType mediaType = MediaType.parse("text/plain");

        RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart("user_image", this.imagePath.getPath(),
                        RequestBody.create(MediaType.parse("application/octet-stream"),
                                imageToString(bitmap)))
                .addFormDataPart("user_account", getIntent().getStringExtra(MainActivity.EXTRA_USER_EMAIL))
                .build();

        Request request = new Request.Builder()
                .url(apiUrl)
                .method("POST", body)
                .addHeader("Authorization", "Token " + getIntent().getStringExtra(MainActivity.EXTRA_TOKEN))
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.println("asdfas");
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                System.out.println(response.message());

            }
        });
    }

    private byte[] imageToString(Bitmap bitmap) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);

        return byteArrayOutputStream.toByteArray();
    }
}

