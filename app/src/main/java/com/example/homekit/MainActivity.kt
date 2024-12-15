package com.example.homekit

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.example.homekit.databinding.ActivityMainBinding
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var database: DatabaseReference
    private var isLightOn = false // Track the state of the light

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.buttonRead.setOnClickListener {
            // Toggle the light when the button is clicked
            toggleLight()
        }
    }

    private fun toggleLight() {
        // Toggle the state of the light
        isLightOn = !isLightOn

        val analogValue = if (isLightOn) 255 else 0 // Set analog value based on light state
        val digitalValue = isLightOn // Set digital value based on light state

        controlLED(analogValue, digitalValue)
    }

    private fun controlLED(analogValue: Int, digitalValue: Boolean) {
        database = FirebaseDatabase.getInstance().reference
        val analogRef = database.child("LED").child("analog")
        analogRef.setValue(analogValue)
            .addOnSuccessListener {
                Toast.makeText(this, "Analog value set successfully", Toast.LENGTH_SHORT).show()
            }
            .addOnFailureListener {
                Toast.makeText(this, "Failed to set analog value", Toast.LENGTH_SHORT).show()
            }

        val digitalRef = database.child("LED").child("digital")
        digitalRef.setValue(digitalValue)
            .addOnSuccessListener {
                Toast.makeText(this, "Digital value set successfully", Toast.LENGTH_SHORT).show()
            }
            .addOnFailureListener {
                Toast.makeText(this, "Failed to set digital value", Toast.LENGTH_SHORT).show()
            }
    }
}
