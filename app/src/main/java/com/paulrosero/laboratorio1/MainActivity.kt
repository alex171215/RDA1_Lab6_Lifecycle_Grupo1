package com.paulrosero.laboratorio1

import android.app.ActivityManager
import android.app.ApplicationStartInfo
import android.content.Context
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.paulrosero.laboratorio1.ui.theme.Laboratorio1Theme

class MainActivity : ComponentActivity() {

    private val TAG = "LIFECYCLE_DEBUG"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate: La Activity se está creando")

        // Reto Android 16: Trazabilidad de Inicio con ApplicationStartInfo
        detectApplicationStartType(savedInstanceState)

        setContent {
            Laboratorio1Theme {
                val viewModel: CounterViewModel = viewModel()
                val count by viewModel.count.collectAsState()
                var localCounter by remember { mutableStateOf(0) }

                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Text(
                            text = "Laboratorio 2.1: Ciclo de Vida",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )

                        Spacer(modifier = Modifier.height(24.dp))

                        // Tarjeta Contador Seguro (Fase 3 & Fase 4 - ViewModel + SavedStateHandle)
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.primaryContainer
                            ),
                            shape = RoundedCornerShape(16.dp),
                            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
                        ) {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(20.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = "Contador Seguro: $count",
                                    style = MaterialTheme.typography.headlineLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onPrimaryContainer
                                )
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = "Persiste a Rotación y Process Death",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                                )
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(
                                    onClick = { viewModel.increment() }
                                ) {
                                    Text("Incrementar", fontSize = 16.sp)
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(20.dp))

                        // Tarjeta Contador Local (Fase 2 - Demostración de Pérdida en Rotación)
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant
                            ),
                            shape = RoundedCornerShape(16.dp)
                        ) {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = "Contador Local: $localCounter",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    text = "(Variable efímera en remember - Se reinicia al rotar)",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.error
                                )
                                Spacer(modifier = Modifier.height(8.dp))
                                Button(
                                    onClick = { localCounter++ },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = MaterialTheme.colorScheme.secondary
                                    )
                                ) {
                                    Text("Incrementar Local")
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    private fun detectApplicationStartType(savedInstanceState: Bundle?) {
        try {
            if (Build.VERSION.SDK_INT >= 35) { // Android 15 (API 35) & Android 16 (API 36)
                val am = getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
                val startInfoList = am?.getHistoricalProcessStartReasons(1)
                if (!startInfoList.isNullOrEmpty()) {
                    val info = startInfoList[0]
                    val startTypeStr = when (info.startType) {
                        ApplicationStartInfo.START_TYPE_COLD -> "Fría (Cold Start)"
                        ApplicationStartInfo.START_TYPE_WARM -> "Cálida (Warm Start)"
                        ApplicationStartInfo.START_TYPE_HOT -> "Caliente (Hot Start)"
                        else -> "Tipo desconocido (${info.startType})"
                    }
                    Log.d(TAG, "ApplicationStartInfo (Android 16): Inicio de forma $startTypeStr [Reason: ${info.reason}]")
                    return
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "Error obteniendo ApplicationStartInfo: ${e.message}")
        }

        // Respaldo heurístico estándar
        val fallbackType = if (savedInstanceState == null) "Fría (Cold Start)" else "Cálida (Warm Start)"
        Log.d(TAG, "Trazabilidad de Inicio: Inicio de forma $fallbackType")
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, "onStart: La Activity es visible")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, "onResume: La Activity tiene el foco (interactuable)")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, "onPause: La Activity pierde el foco")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, "onStop: La Activity ya no es visible")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "onDestroy: La Activity va a ser destruida")
    }
}