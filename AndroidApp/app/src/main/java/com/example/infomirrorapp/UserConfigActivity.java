package com.example.infomirrorapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class UserConfigActivity extends AppCompatActivity {
    private CheckBox newsAppCheck;
    private CheckBox covidTrackerCheck;
    private CheckBox trafficStatusCheck;
    private CheckBox weatherAppCheck;
    private TextView debugView;

    private String token;
    private String userEmail;

    private JSONObject configJson;


    // TODO set initial values for checkboxes
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_config);

        this.newsAppCheck = findViewById(R.id.newsAppCheck);
        this.covidTrackerCheck = findViewById(R.id.covidTrackerCheck);
        this.trafficStatusCheck = findViewById(R.id.trafficStatusCheck);
        this.weatherAppCheck = findViewById(R.id.weatherAppCheck);
        this.debugView = findViewById(R.id.debug1View);

        Intent intent = getIntent();
        this.token = intent.getStringExtra(MainActivity.EXTRA_TOKEN);
        this.userEmail = intent.getStringExtra(MainActivity.EXTRA_USER_EMAIL);
    }

    public void saveConfig(View view) {
        String apiUrl = "http://192.168.178.66:8000/api/user-config/create/";
        RequestQueue queue = Volley.newRequestQueue(this);
        this.configJson = new JSONObject();

        try {
            this.configJson.put("user_account", getIntent().getStringExtra(MainActivity.EXTRA_USER_EMAIL));
            this.configJson.put("news_app", Boolean.toString(this.newsAppCheck.isChecked()).toLowerCase());
            this.configJson.put("covid_tracker", Boolean.toString(this.covidTrackerCheck.isChecked()).toLowerCase());
            this.configJson.put("traffic_status", Boolean.toString(this.trafficStatusCheck.isChecked()).toLowerCase());
            this.configJson.put("weather_app", Boolean.toString(this.weatherAppCheck.isChecked()).toLowerCase());

        } catch (JSONException e) {
            e.printStackTrace();
        }

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.POST, apiUrl, this.configJson, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                debugView.setText(response.toString());
                System.out.println(response);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        })       {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {

                Map<String, String> params = new HashMap<String, String>();
                params.put("Content-Type", "application/json; charset=UTF-8");
                params.put("Authorization", "Token " + getIntent().getStringExtra(MainActivity.EXTRA_TOKEN));
                return params;
            }};

        queue.add(request);
    }

    public void pushChooseImageActivity(View view) {
        Intent intent = new Intent(this, ChooseImageActivity.class);
        intent.putExtra(MainActivity.EXTRA_USER_EMAIL,  this.userEmail);
        intent.putExtra(MainActivity.EXTRA_TOKEN,  this.token);
        startActivity(intent);
    }
}