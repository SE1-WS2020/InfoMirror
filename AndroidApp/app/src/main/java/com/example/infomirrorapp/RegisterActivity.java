package com.example.infomirrorapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class RegisterActivity extends AppCompatActivity {
    private Button registerButton;
    private EditText usernameText;
    private EditText emailText;
    private EditText passwordText;
    private EditText password2Text;
    private TextView debugView;

    private TextView emailHint;
    private TextView usernameHint;
    private TextView passwordHint;


    private JSONObject newUserData;

    private String token;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        this.usernameText = findViewById(R.id.editTextUsername);
        this.emailText = findViewById(R.id.editTextTextEmailAddress);
        this.passwordText = findViewById(R.id.editTextTextPassword);
        this.password2Text = findViewById(R.id.editTextTextPassword2);
        this.debugView = findViewById(R.id.responseView);

        this.emailHint = findViewById(R.id.emailHint);
        this.usernameHint = findViewById(R.id.usernameHint);
        this.passwordHint = findViewById(R.id.passwordHint);

    }

    public void registerButtonOnClick(View view) {
        RequestQueue queue = Volley.newRequestQueue(this);
        this.newUserData = new JSONObject();

        try {
            this.newUserData.put("email", this.emailText.getText().toString());
            this.newUserData.put("username", this.usernameText.getText().toString());
            this.newUserData.put("password", this.passwordText.getText().toString());
            this.newUserData.put("password2", this.password2Text.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String apiUrl = "http://192.168.178.66:8000/api/register/";

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, apiUrl, this.newUserData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                debugView.setText(response.toString());
                processRegisterResponse(response);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        });

        queue.add(request);
    }

    public void processRegisterResponse(JSONObject response) {
        this.clearHints();

        try {
            this.usernameHint.setText(response.getString("username"));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        try {
            this.emailHint.setText(response.getString("email"));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        try {
            this.passwordHint.setText(response.getString("password"));
        } catch (JSONException e) {
            e.printStackTrace();
        }


        try {
            this.token = response.getString("token");
            this.pushSettingsView();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void pushSettingsView() {
        Intent intent = new Intent(this, UserConfigActivity.class);
        intent.putExtra(MainActivity.EXTRA_TOKEN, this.token);
        intent.putExtra(MainActivity.EXTRA_USER_EMAIL, this.emailText.getText().toString());
        startActivity(intent);
    }

    private void clearHints() {
        this.usernameHint.setText("");
        this.emailHint.setText("");
        this.passwordHint.setText("");
    }
}