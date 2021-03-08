package com.example.infomirrorapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    public static final String EXTRA_TOKEN = "com.example.infomirrorapp.TOKEN";
    public static final String EXTRA_USER_EMAIL = "com.example.infomirrorapp.USER_EMAIL";
    private Button signInButton;
    private Button registerButton;
    private EditText emailText;
    private EditText passwordText;
    private TextView debugInfo;

    private String authToken;
    private JSONObject loginData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        signInButton = findViewById(R.id.singInButton);
        emailText = findViewById(R.id.emailAddressText);
        passwordText = findViewById(R.id.passwordText);
        debugInfo = findViewById(R.id.responseView);

    }

    public void startRegisterActivity(View view) {
        Intent intent = new Intent(this, RegisterActivity.class);

        startActivity(intent);
    }

    public void login(View view) {
        RequestQueue queue = Volley.newRequestQueue(this);
        this.loginData = new JSONObject();

        try {
            this.loginData.put("username", this.emailText.getText().toString());
            this.loginData.put("password", this.passwordText.getText().toString());
        }
        catch (JSONException e) {
            e.printStackTrace();
        }

        String apiUrl = "http://192.168.178.66:8000/api/login/";

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, apiUrl, this.loginData,
                response -> this.processLogInResponse(response),
                error -> error.printStackTrace());

        queue.add(request);
    }

    public void processLogInResponse(JSONObject response) {
        try {
            System.out.println(response.getString("token"));
            this.authToken = response.getString("token");
            this.startConfigView();
        } catch (JSONException e) {
            e.printStackTrace();
            this.authToken = "";
        }

        if (this.authToken.equals("")) {
            this.debugInfo.setText("Authentication failed.");
        }
        else {
            this.debugInfo.setText("Authentication successful.");
            this.getUserConfig();
        }
    }

    private void startConfigView() {
        Intent intent = new Intent(this, UserConfigActivity.class);
        intent.putExtra(MainActivity.EXTRA_TOKEN, this.authToken);
        intent.putExtra(MainActivity.EXTRA_USER_EMAIL, this.emailText.getText().toString());
        startActivity(intent);
    }

    public void getUserConfig() {
        RequestQueue queue = Volley.newRequestQueue(this);
        String username = "";

        try {
            username = this.loginData.getString("username");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String apiUrl = "http://192.168.178.66:8000/api/user-config/" + username;

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, apiUrl, new JSONObject(),
                response -> System.out.println(response),
                error -> error.printStackTrace())
        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {

                Map<String, String> params = new HashMap<String, String>();
                params.put("Content-Type", "application/json; charset=UTF-8");
                params.put("Authorization", "Token " + authToken);
                return params;
            }
        };

        queue.add(request);
    }

    public void getAPIInfo(View view) {
        RequestQueue queue = Volley.newRequestQueue(this);

        String apiUrl = "http://192.168.178.66:8000/api/";
        StringRequest stringRequest = new StringRequest(Request.Method.GET, apiUrl,
                response -> debugInfo.setText(response),
                error -> printConnError(error));
        queue.add(stringRequest);
    }

    private void printConnError(VolleyError error) {
        System.out.println("Error: " + error
                + "\nStatus Code " + error.networkResponse.statusCode
                + "\nCause " + error.getCause()
                + "\nnetworkResponse " + error.networkResponse.data.toString()
                + "\nmessage" + error.getMessage());
    }
}