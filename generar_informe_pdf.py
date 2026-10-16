import os
import base64
from playwright.sync_api import sync_playwright

def img_to_base64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img1_b64 = img_to_base64("capturas/01_contador_antes_de_rotar.png")
img2_b64 = img_to_base64("capturas/02_emulador_contador_15_tras_rotar.png")
img3_b64 = img_to_base64("capturas/03_logcat_rotacion.png")
img4_b64 = img_to_base64("capturas/04_dont_keep_activities.png")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Informe Laboratorio 2.1: Dominio del Ciclo de Vida y Persistencia de Estado</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1f2937;
    line-height: 1.6;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}

  /* Page break utilities */
  .page-break {{
    page-break-before: always;
  }}

  .avoid-break {{
    page-break-inside: avoid;
  }}

  /* Cover Page */
  .cover-page {{
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px 0 40px 0;
    border-bottom: 3px solid #2563eb;
  }}

  .cover-header {{
    border-left: 6px solid #2563eb;
    padding-left: 20px;
  }}

  .institution {{
    font-size: 13pt;
    font-weight: 700;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 4px 0;
  }}

  .faculty {{
    font-size: 11pt;
    font-weight: 500;
    color: #6b7280;
    margin: 0;
  }}

  .cover-title-box {{
    margin: 60px 0;
  }}

  .badge-lab {{
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 9.5pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
  }}

  .cover-title {{
    font-size: 26pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
    margin: 0 0 16px 0;
  }}

  .cover-subtitle {{
    font-size: 14pt;
    color: #475569;
    font-weight: 400;
    line-height: 1.4;
    margin: 0;
  }}

  .cover-meta-grid {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 40px;
  }}

  .meta-item-label {{
    font-size: 8.5pt;
    font-weight: 600;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 2px;
  }}

  .meta-item-value {{
    font-size: 11pt;
    font-weight: 600;
    color: #1e293b;
  }}

  /* Headings */
  h1 {{
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 14px;
  }}

  h2 {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 22px;
    margin-bottom: 10px;
  }}

  h3 {{
    font-size: 11.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 8px;
  }}

  p {{
    margin: 0 0 12px 0;
    text-align: justify;
  }}

  ul, ol {{
    margin: 0 0 14px 0;
    padding-left: 24px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  /* Highlight boxes */
  .callout {{
    border-radius: 8px;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 10pt;
  }}

  .callout-info {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    color: #1e40af;
  }}

  .callout-warning {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #92400e;
  }}

  .callout-success {{
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    color: #166534;
  }}

  /* Images & Figures */
  .figure-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
    margin: 18px 0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    text-align: center;
  }}

  .figure-img {{
    max-width: 100%;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
  }}

  .figure-caption {{
    font-size: 9pt;
    color: #64748b;
    margin-top: 8px;
    font-weight: 500;
  }}

  .figure-caption b {{
    color: #334155;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 9.5pt;
  }}

  th {{
    background: #1e3a8a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    border: 1px solid #1e3a8a;
  }}

  td {{
    padding: 9px 12px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* Code blocks */
  pre {{
    background: #0f172a;
    color: #f8fafc;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.5pt;
    padding: 14px 16px;
    border-radius: 8px;
    overflow-x: auto;
    line-height: 1.45;
    margin: 14px 0;
  }}

  code {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* Questions & Answers */
  .qa-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #2563eb;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 14px;
  }}

  .qa-question {{
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 8px;
    font-size: 10.5pt;
  }}

  .qa-answer {{
    color: #334155;
    font-size: 10pt;
    margin: 0;
  }}

  /* Footer */
  .report-footer {{
    margin-top: 30px;
    border-top: 1px solid #e2e8f0;
    padding-top: 12px;
    display: flex;
    justify-content: space-between;
    font-size: 8pt;
    color: #94a3b8;
  }}
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover-page">
  <div class="cover-header">
    <div class="institution">Pontificia Universidad Católica del Ecuador / FISE</div>
    <div class="faculty">Redes y Dispositivos Móviles • Programación de Dispositivos Móviles</div>
  </div>

  <div class="cover-title-box">
    <div class="badge-lab">Laboratorio 2.1 — Informe Técnico Oficial</div>
    <h1 class="cover-title">Dominio del Ciclo de Vida y Persistencia de Estado en Android</h1>
    <p class="cover-subtitle">
      Instrumentación en Logcat, mitigación de cambios de configuración con Jetpack ViewModel,
      supervivencia a Process Death mediante SavedStateHandle y Trazabilidad de Inicio con ApplicationStartInfo (Android 16 API 36).
    </p>
  </div>

  <div class="cover-meta-grid">
    <div>
      <div class="meta-item-label">Proyecto / Repositorio</div>
      <div class="meta-item-value"><a href="https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1" style="color: #1d4ed8; text-decoration: none;">GitHub / RDA1_Lab6_Lifecycle_Grupo1</a></div>
    </div>
    <div>
      <div class="meta-item-label">Nombre del Proyecto Gradle</div>
      <div class="meta-item-value">LifecycleMaster</div>
    </div>
    <div>
      <div class="meta-item-label">Plataforma & Entorno</div>
      <div class="meta-item-value">Google Pixel 8 • Android 16 (API 36 Baklava)</div>
    </div>
    <div>
      <div class="meta-item-label">Grupo / Autores</div>
      <div class="meta-item-value">Grupo 1 (Alexander Carrión, Paul Rosero)</div>
    </div>
    <div>
      <div class="meta-item-label">Fecha de Ejecución</div>
      <div class="meta-item-value">Octubre 2026</div>
    </div>
    <div>
      <div class="meta-item-label">Commit Final</div>
      <div class="meta-item-value">Lab 2.1: Persistencia total con ViewModel y SavedStateHandle</div>
    </div>
  </div>
</div>

<!-- PÁGINA 2: OBJETIVOS Y MARCO TEÓRICO -->
<div class="page-break"></div>
<h1>1. Contexto y Objetivos del Laboratorio</h1>
<p>
  En el ecosistema móvil contemporáneo, particularmente con la introducción de <b>Android 16 (API 36 Baklava)</b>,
  el sistema operativo aplica políticas de gestión de recursos altamente agresivas con el objetivo primordial de
  maximizar la eficiencia energética y la disponibilidad de memoria RAM.
</p>
<p>
  En este contexto, un <code>Activity</code> en Android es por definición un componente <b>efímero</b> que el sistema
  puede destruir y recrear en cualquier momento, bien sea por motivos previsibles (como los cambios de configuración
  al rotar la pantalla entre orientaciones vertical y horizontal) o por situaciones imprevistas de presión de memoria
  (como la muerte del proceso o <i>Process Death</i> cuando la aplicación se encuentra en segundo plano).
</p>

<h3>Objetivos Principales:</h3>
<ul>
  <li><b>Experimentar y mapear los callbacks del ciclo de vida</b> de un <code>ComponentActivity</code> en Android mediante trazabilidad en tiempo real en Logcat utilizando el tag estandarizado <code>LIFECYCLE_DEBUG</code>.</li>
  <li><b>Demostrar empíricamente la vulnerabilidad del estado efímero</b> en Jetpack Compose cuando se utiliza únicamente la función <code>remember {{ mutableStateOf(...) }}</code> frente a una rotación de pantalla.</li>
  <li><b>Implementar la arquitectura de Jetpack ViewModel</b> para garantizar que los datos sobrevivan de manera transparente a las recreaciones del Activity provocadas por cambios de configuración.</li>
  <li><b>Dominar la técnica de persistencia de estado con <code>SavedStateHandle</code></b> integrada en el ViewModel para garantizar que el estado del usuario sobreviva incluso tras la muerte del proceso del sistema (<i>Process Death</i>) simulada con la opción de desarrollador <i>"Don't keep activities"</i>.</li>
  <li><b>Superar el Desafío de Innovación:</b> Implementar trazabilidad de inicio avanzada en <code>onCreate</code> empleando la nueva API de Android 16 <code>ApplicationStartInfo</code> para diagnosticar de forma programática inicios fríos (<i>Cold Start</i>) y cálidos (<i>Warm Start</i>).</li>
</ul>

<div class="callout callout-info">
  <b>Requisitos Técnicos Cumplidos:</b>
  El proyecto fue configurado y ejecutado en el emulador oficial <b>Pixel 8 - API 36 (Android 16)</b>,
  con las Opciones de Desarrollador habilitadas, compilado con JDK 21 y Android Gradle Plugin 8.7.0.
</div>

<h1>2. Marco Teórico y Fundamentos Arquitecturales</h1>
<p>
  Para comprender a profundidad las soluciones implementadas, es fundamental discernir los distintos niveles de
  persistencia y el ciclo de vida de los componentes en Android:
</p>

<table>
  <thead>
    <tr>
      <th>Mecanismo</th>
      <th>Ámbito de Memoria</th>
      <th>Sobrevive a Rotación</th>
      <th>Sobrevive a Process Death</th>
      <th>Sobrevive a Cierre por Usuario</th>
      <th>Caso de Uso Recomendado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>remember</b></td>
      <td>Composición local (RAM)</td>
      <td>❌ No</td>
      <td>❌ No</td>
      <td>❌ No</td>
      <td>Animaciones UI, estados visuales efímeros mientras la pantalla esté activa.</td>
    </tr>
    <tr>
      <td><b>rememberSaveable</b></td>
      <td>SavedStateRegistry (Bundle)</td>
      <td>✅ Sí</td>
      <td>✅ Sí</td>
      <td>❌ No</td>
      <td>Estados UI simples dentro de composables individuales (e.g. scroll position, texto temporal).</td>
    </tr>
    <tr>
      <td><b>ViewModel (solo)</b></td>
      <td>ViewModelStore en Heap RAM</td>
      <td>✅ Sí</td>
      <td>❌ No</td>
      <td>❌ No</td>
      <td>Lógica de negocio, consumo de APIs, flujos de datos en memoria activa.</td>
    </tr>
    <tr>
      <td><b>SavedStateHandle (en ViewModel)</b></td>
      <td>Bundle del SO + Heap</td>
      <td>✅ Sí</td>
      <td>✅ Sí</td>
      <td>❌ No</td>
      <td>Identificadores de sesión, contadores clave, inputs de formularios críticos.</td>
    </tr>
    <tr>
      <td><b>Room / DataStore</b></td>
      <td>Almacenamiento Flash (Disco)</td>
      <td>✅ Sí</td>
      <td>✅ Sí</td>
      <td>✅ Sí</td>
      <td>Bases de datos relacionales, preferencias de usuario, cachés offline persistentes.</td>
    </tr>
  </tbody>
</table>

<!-- PÁGINA 3: DESARROLLO PASO A PASO -->
<div class="page-break"></div>
<h1>3. Desarrollo Detallado Fase a Fase</h1>

<h2>Fase 0: Preparación y Estandarización Técnica del Proyecto</h2>
<p>
  Se estableció la base técnica a partir del proyecto base. Conforme a las directrices de la guía docente:
</p>
<ol>
  <li>Se limpiaron las carpetas de caché y artefactos generados (<code>.gradle</code> y <code>build</code>).</li>
  <li>Se configuró <code>settings.gradle.kts</code> asignando el nombre estandarizado:
    <code>rootProject.name = "LifecycleMaster"</code>.</li>
  <li>En <code>gradle.properties</code> se añadió <code>android.suppressUnsupportedCompileSdk=36</code> para garantizar compatibilidad nativa con el SDK 36 (Android 16 Baklava).</li>
  <li>En <code>gradle/libs.versions.toml</code> y <code>app/build.gradle.kts</code> se integró la biblioteca <code>androidx.lifecycle:lifecycle-viewmodel-compose</code>.</li>
</ol>

<h2>Fase 1: Rastreo del Ciclo de Vida (Logging Instrumentado)</h2>
<p>
  En <code>MainActivity.kt</code> se sobreescribieron todos los callbacks del ciclo de vida del <code>ComponentActivity</code>
  asociándolos al identificador de depuración <code>TAG = "LIFECYCLE_DEBUG"</code>:
</p>
<ul>
  <li><code>onCreate()</code>: Se invoca al instanciar la Activity en memoria. Se inicializan vistas y componentes.</li>
  <li><code>onStart()</code>: La Activity se vuelve visible para el usuario.</li>
  <li><code>onResume()</code>: La Activity adquiere el foco del sistema y se vuelve completamente interactuable.</li>
  <li><code>onPause()</code>: La Activity pierde el foco (por ejemplo, al iniciar la rotación o abrir otra ventana).</li>
  <li><code>onStop()</code>: La Activity deja de ser visible para el usuario.</li>
  <li><code>onDestroy()</code>: La Activity se destruye por completo y se liberan sus referencias inmediatas de memoria.</li>
</ul>

<h2>Fase 2: Demostración Empírica del Problema (Pérdida en Rotación)</h2>
<p>
  Se implementó un contador local utilizando la instrucción de Compose:
  <code>var localCounter by remember {{ mutableStateOf(0) }}</code>.
  Al interactuar con la aplicación y elevar el contador a un valor positivo (e.g. 10) y posteriormente rotar la pantalla
  hacia orientación horizontal (Landscape), el sistema operativo destruye la instancia original de la Activity
  y genera una nueva. Como consecuencia directa, <b>el contador local se reinicia a cero (0)</b>, demostrando
  la incapacidad de <code>remember</code> para preservar estado ante cambios de configuración.
</p>

<h2>Fase 3: La Solución de Arquitectura Jetpack (ViewModel)</h2>
<p>
  Para resolver la pérdida por rotación, se creó la clase <code>CounterViewModel.kt</code> heredando de <code>ViewModel()</code>.
  A diferencia de la Activity, el <code>ViewModel</code> sobrevive a los cambios de configuración porque su ciclo de vida
  está ligado al <code>ViewModelStoreOwner</code> y no a la instancia física del componente visual.
</p>

<h2>Fase 4: Resistencia ante la Muerte del Proceso (SavedStateHandle)</h2>
<p>
  Aunque el ViewModel sobrevive a la rotación, sus variables en memoria RAM son destruidas si el sistema operativo
  termina el proceso por falta de memoria (<i>Process Death</i>). Para alcanzar la persistencia total, se inyectó
  <code>SavedStateHandle</code> en el constructor del ViewModel. Se empleó la clave <code>"counter_key"</code> con un
  flujo mutable reactivo sincronizado con el Bundle del sistema operativo:
</p>
<pre><code>class CounterViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {{
    // Sincronización bidireccional con el Bundle del SO para resistir Process Death
    private val _count = savedStateHandle.getMutableStateFlow("counter_key", 0)
    val count = _count.asStateFlow()

    fun increment() {{
        _count.value++
    }}
}}</code></pre>

<!-- PÁGINA 4: RETO ANDROID 16 -->
<div class="page-break"></div>
<h1>4. Desafío de Innovación: Trazabilidad con ApplicationStartInfo</h1>
<p>
  El reto de la guía docente solicita diagnosticar de forma programática el tipo de inicio de la aplicación
  aprovechando las capacidades introducidas en las APIs más recientes de Android (API 35/36): <b>ApplicationStartInfo</b>.
</p>

<h3>Fundamento Técnico de ApplicationStartInfo:</h3>
<p>
  Históricamente, los desarrolladores debían inferir los arranques fríos mediante banderas estáticas o inspeccionando
  si <code>savedInstanceState == null</code>. Android 15 y Android 16 introducen el método
  <code>activityManager.getHistoricalProcessStartReasons(maxNum)</code> que retorna registros de nivel de kernel
  con las razones físicas y marcas de tiempo del proceso.
</p>

<table>
  <thead>
    <tr>
      <th>Tipo de Inicio</th>
      <th>Constante API 36</th>
      <th>Comportamiento en Memoria / Kernel</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Cold Start (Inicio Frío)</b></td>
      <td><code>START_TYPE_COLD</code> (1)</td>
      <td>El proceso no existe en la tabla de procesos. El kernel de Linux debe hacer <i>fork</i> de Zygote, cargar el runtime ART, inicializar la clase <code>Application</code> y finalmente inflar el <code>Activity</code>. Es el inicio más costoso.</td>
    </tr>
    <tr>
      <td><b>Warm Start (Inicio Cálido)</b></td>
      <td><code>START_TYPE_WARM</code> (2)</td>
      <td>El proceso de la aplicación ya se encuentra en memoria o la Activity debe ser recreada tras cambios de configuración o restauración de tarea sin recrear el proceso completo.</td>
    </tr>
    <tr>
      <td><b>Hot Start (Inicio Caliente)</b></td>
      <td><code>START_TYPE_HOT</code> (3)</td>
      <td>Tanto el proceso como la Activity residen ya en memoria RAM; el sistema únicamente trae la Activity al primer plano invocando <code>onStart</code> y <code>onResume</code> sin pasar por <code>onCreate</code>.</td>
    </tr>
  </tbody>
</table>

<h3>Implementación en <code>MainActivity.kt</code>:</h3>
<pre><code>private fun detectApplicationStartType(savedInstanceState: Bundle?) {{
    try {{
        if (Build.VERSION.SDK_INT >= 35) {{ // Android 15 & Android 16 (API 36 Baklava)
            val am = getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
            val startInfoList = am?.getHistoricalProcessStartReasons(1)
            if (!startInfoList.isNullOrEmpty()) {{
                val info = startInfoList[0]
                val startTypeStr = when (info.startType) {{
                    ApplicationStartInfo.START_TYPE_COLD -> "Fría (Cold Start)"
                    ApplicationStartInfo.START_TYPE_WARM -> "Cálida (Warm Start)"
                    ApplicationStartInfo.START_TYPE_HOT -> "Caliente (Hot Start)"
                    else -> "Tipo desconocido (${{info.startType}})"
                }}
                Log.d(TAG, "ApplicationStartInfo (Android 16): Inicio de forma $startTypeStr [Reason: ${{info.reason}}]")
                return
            }}
        }}
    }} catch (e: Exception) {{
        Log.w(TAG, "Error obteniendo ApplicationStartInfo: ${{e.message}}")
    }}

    val fallbackType = if (savedInstanceState == null) "Fría (Cold Start)" else "Cálida (Warm Start)"
    Log.d(TAG, "Trazabilidad de Inicio: Inicio de forma $fallbackType")
}}</code></pre>

<!-- PÁGINA 5: EVIDENCIAS EXPERIMENTALES (CAPTURAS) -->
<div class="page-break"></div>
<h1>5. Evidencias Experimentales y Capturas de Pantalla</h1>
<p>
  A continuación se presentan las capturas de pantalla obtenidas directamente del entorno de ejecución
  en el emulador Pixel 8 con Android 16 (API 36), las cuales demuestran el cumplimiento riguroso de cada
  fase y resultado esperado.
</p>

<div class="figure-card avoid-break">
  <img src="{img1_b64}" class="figure-img" style="max-height: 140mm;" alt="Contador antes de rotar">
  <div class="figure-caption">
    <b>Figura 1:</b> Aplicación ejecutándose en el emulador Pixel 8 (Android 16) en orientación vertical previa a la rotación.
    Se observa el <b>Contador Seguro en 15</b> (gestionado por ViewModel y SavedStateHandle) y el <b>Contador Local en 10</b> (efímero).
  </div>
</div>

<!-- PÁGINA 6: CAPTURAS DE ROTACIÓN Y LOGCAT -->
<div class="page-break"></div>

<div class="figure-card avoid-break">
  <img src="{img2_b64}" class="figure-img" style="max-height: 90mm;" alt="Contador en 15 tras rotar">
  <div class="figure-caption">
    <b>Figura 2 (Entregable Requerido):</b> Emulador Pixel 8 con el <b>Contador Seguro en 15 tras haber rotado la pantalla a modo horizontal (Landscape)</b>.
    Nótese cómo el Contador Local se reinició automáticamente a 0 debido a la destrucción de la Activity, mientras que el Contador Seguro preservó íntegramente su valor.
  </div>
</div>

<div class="figure-card avoid-break">
  <img src="{img3_b64}" class="figure-img" style="max-width: 98%;" alt="Logcat del ciclo de vida durante la rotación">
  <div class="figure-caption">
    <b>Figura 3 (Entregable Requerido):</b> Registro completo de Logcat filtrado por el tag <code>LIFECYCLE_DEBUG</code> durante el evento de rotación.
    Se evidencia la secuencia exacta requerida: <code>onPause &rarr; onStop &rarr; onDestroy &rarr; onCreate &rarr; onStart &rarr; onResume</code>,
    junto con la detección automática de <code>ApplicationStartInfo</code>.
  </div>
</div>

<!-- PÁGINA 7: CAPTURA DON'T KEEP ACTIVITIES Y PROCESS DEATH -->
<div class="page-break"></div>

<div class="figure-card avoid-break">
  <img src="{img4_b64}" class="figure-img" style="max-height: 155mm;" alt="Don't keep activities switch activado">
  <div class="figure-caption">
    <b>Figura 4 (Entregable Requerido):</b> Captura de pantalla de las <b>Opciones de Desarrollador</b> en el emulador Pixel 8 API 36,
    mostrando el interruptor <b>"Don't keep activities" (No conservar actividades) activado</b>.
    Esta configuración fuerza al sistema a destruir inmediatamente la Activity tan pronto como el usuario sale de ella,
    simulando las condiciones exactas de Process Death.
  </div>
</div>

<!-- PÁGINA 8: CUESTIONARIO Y PREGUNTAS TÉCNICAS -->
<div class="page-break"></div>
<h1>6. Respuestas a Preguntas de Evaluación y Reflexión</h1>

<div class="qa-card avoid-break">
  <div class="qa-question">
    Pregunta 1: ¿Por qué una variable gestionada únicamente con <code>remember {{ mutableStateOf(0) }}</code> pierde su valor cuando el usuario rota la pantalla?
  </div>
  <div class="qa-answer">
    <b>Respuesta Técnica:</b> La función <code>remember</code> almacena el estado dentro de la estructura interna del árbol de composición (Composition Slot Table), la cual se encuentra estrechamente acoplada a la instancia viva del <code>ComponentActivity</code>. Cuando ocurre una rotación de pantalla, Android clasifica este evento como un cambio de configuración (<code>Configuration Change</code>) y por diseño destruye la instancia actual del Activity llamando a <code>onPause()</code>, <code>onStop()</code> y <code>onDestroy()</code>, desechando su memoria heap asociada. Al crearse una nueva Activity mediante <code>onCreate()</code>, el árbol de composición se infla desde cero, reinicializando la variable a su valor inicial por defecto (0).
  </div>
</div>

<div class="qa-card avoid-break">
  <div class="qa-question">
    Pregunta 2: ¿Cuál es el mecanismo interno mediante el cual un <code>ViewModel</code> sobrevive a la rotación de pantalla si la Activity es destruida?
  </div>
  <div class="qa-answer">
    <b>Respuesta Técnica:</b> La instancia del <code>ViewModel</code> no pertenece a la Activity, sino a un <code>ViewModelStore</code> gestionado por el sistema a nivel de proceso. Durante el cambio de configuración, el framework retiene el <code>ViewModelStore</code> pasándolo de la Activity antigua a la nueva a través del mecanismo interno de <code>NonConfigurationInstances</code>. Cuando la nueva Activity invoca <code>viewModel()</code> dentro de su nuevo <code>onCreate()</code>, el <code>ViewModelProvider</code> busca en el almacén retenido y retorna la misma instancia en memoria RAM existente previamente, preservando intactos sus flujos reactivos (<code>StateFlow</code>) y propiedades.
  </div>
</div>

<div class="qa-card avoid-break">
  <div class="qa-question">
    Pregunta 3: Si <code>ViewModel</code> sobrevive a la rotación, ¿por qué es indispensable utilizar <code>SavedStateHandle</code> para lograr persistencia ante la muerte del proceso (Process Death)?
  </div>
  <div class="qa-answer">
    <b>Respuesta Técnica:</b> El <code>ViewModel</code> únicamente sobrevive a la rotación de pantalla porque el proceso de la aplicación permanece vivo en la memoria RAM del sistema operativo. Sin embargo, cuando el usuario envía la app a segundo plano y el sistema operativo sufre de escasez de recursos o la opción <i>"Don't keep activities"</i> está habilitada, el kernel puede terminar (<i>kill</i>) el proceso completo de la aplicación. Al morir el proceso, todo el Heap de memoria RAM se destruye, incluyendo el <code>ViewModelStore</code>. <code>SavedStateHandle</code> resuelve esto al conectarse con el <code>SavedStateRegistry</code> del sistema operativo, serializando las claves y valores en un <code>Bundle</code> que es custodiado por el proceso central del sistema (<code>system_server</code> / <code>ActivityManagerService</code>). Al relanzar la app, el SO pasa este Bundle al nuevo proceso, permitiendo al ViewModel restaurar su estado original de forma completamente transparente.
  </div>
</div>

<div class="qa-card avoid-break">
  <div class="qa-question">
    Pregunta 4: ¿Qué ventajas aporta la API <code>ApplicationStartInfo</code> de Android 16 frente a las técnicas tradicionales de medición de rendimiento?
  </div>
  <div class="qa-answer">
    <b>Respuesta Técnica:</b> Tradicionalmente, la detección de arranques fríos, cálidos y calientes dependía de banderas estáticas artesanales en la clase <code>Application</code> o en heurísticas basadas en <code>savedInstanceState</code>, las cuales carecían de precisión temporal a nivel de kernel y no podían identificar las razones específicas del inicio (e.g. lanzamiento por broadcast, servicio en background, o interacción de usuario). <code>ApplicationStartInfo</code> provee telemetría directa del sistema operativo, timestamps precisos de cada fase de arranque (tiempo de fork de proceso, tiempo de onCreate, tiempo de primer frame dibujado) y clasificación oficial de <code>START_TYPE_COLD</code>, <code>START_TYPE_WARM</code> y <code>START_TYPE_HOT</code>, permitiendo a los equipos de ingeniería diagnosticar y optimizar con exactitud milimétrica la latencia de arranque percibida por el usuario.
  </div>
</div>

<!-- PÁGINA 9: CONCLUSIONES Y RECOMENDACIONES -->
<div class="page-break"></div>
<h1>7. Conclusiones y Recomendaciones</h1>

<h3>Conclusiones:</h3>
<ul>
  <li><b>Comprobación empírica del ciclo de vida efímero:</b> Se verificó a través de la instrumentación en Logcat que la rotación de pantalla provoca inexorablemente la secuencia <code>onPause &rarr; onStop &rarr; onDestroy &rarr; onCreate</code>, lo que invalida cualquier intento de mantener datos persistentes utilizando únicamente estructuras efímeras en memoria local de composición (<code>remember</code>).</li>
  <li><b>Arquitectura desacoplada y robusta con Jetpack:</b> La implementación del patrón MVVM mediante <code>CounterViewModel</code> demostró que separar la lógica y retención del estado respecto a la capa de presentación visual no solo previene la pérdida de datos ante cambios de configuración, sino que garantiza código modular, escalable y fácilmente testeable.</li>
  <li><b>Resiliencia ante Process Death con SavedStateHandle:</b> La prueba de estrés realizada con la opción de desarrollador <i>"Don't keep activities"</i> validó que <code>SavedStateHandle</code> es la pieza fundamental que cierra la brecha entre la supervivencia en memoria RAM (ViewModel) y la persistencia estructurada a nivel de sistema operativo (Bundle), protegiendo la experiencia del usuario contra destrucciones imprevistas del proceso por gestión de energía en Android 16.</li>
  <li><b>Éxito del reto de innovación con ApplicationStartInfo:</b> Se integró de manera exitosa la API nativa de Android 16 para diagnosticar de forma programática el tipo de inicio del proceso, elevando la calidad técnica de la solución hacia los estándares de observabilidad y rendimiento de vanguardia.</li>
</ul>

<h3>Recomendaciones Técnicas:</h3>
<ul>
  <li><b>Regla de Oro en Compose:</b> Utilizar <code>remember</code> exclusivamente para estados visuales efímeros que no tengan impacto si se reinician (e.g., color transitorio de un botón o estado de expansión de un menú desplegable). Cualquier dato con significado para el usuario debe residir en un <code>ViewModel</code> o utilizar <code>rememberSaveable</code>.</li>
  <li><b>Uso disciplinado de SavedStateHandle:</b> Limitar los datos almacenados en <code>SavedStateHandle</code> a identificadores, tokens de sesión y estados clave de interfaz (generalmente menos de 50 KB). Nunca deben almacenarse objetos masivos, listas de imágenes o colecciones complejas en el Bundle del sistema para evitar excepciones de tipo <code>TransactionTooLargeException</code>. Para datos pesados debe combinarse el ViewModel con una base de datos local como <b>Room</b>.</li>
  <li><b>Pruebas continuas de ciclo de vida en CI/CD:</b> Mantener activada la opción <i>"Don't keep activities"</i> durante las fases de desarrollo y pruebas QA para detectar fugas de estado tempranas antes de que la aplicación sea desplegada a producción.</li>
</ul>

<!-- PÁGINA 10: REPOSITORIO Y ANEXO DE CÓDIGO -->
<div class="page-break"></div>
<h1>8. Enlace al Repositorio de GitHub y Commits</h1>
<div class="callout callout-success avoid-break">
  <b>Entrega Oficial en Control de Versiones (GitHub):</b><br><br>
  <ul>
    <li><b>Enlace al Repositorio GitHub:</b> <a href="https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1" style="color: #1d4ed8; font-weight: 600;">https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1</a></li>
    <li><b>Mensaje del Commit Final Requerido:</b> <code>Lab 2.1: Persistencia total con ViewModel y SavedStateHandle</code></li>
    <li><b>Explorador de Código en GitHub:</b> <a href="https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1/tree/main" style="color: #1d4ed8; font-weight: 600;">https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1/tree/main</a></li>
    <li><b>Historial Completo de Commits:</b> <a href="https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1/commits/main" style="color: #1d4ed8; font-weight: 600;">https://github.com/alex171215/RDA1_Lab6_Lifecycle_Grupo1/commits/main</a></li>
    <li><b>Ramas Sincronizadas:</b> <code>main</code> (rama predeterminada de producción) y <code>master</code></li>
  </ul>
</div>

<h1>9. Anexo: Código Fuente Completo de la Solución</h1>

<h3>9.1. <code>CounterViewModel.kt</code></h3>
<pre><code>package com.paulrosero.laboratorio1

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

// Extensión para SavedStateHandle que proporciona un MutableStateFlow sincronizado
// con el Bundle interno de SavedStateHandle para resistir Process Death
fun &lt;T&gt; SavedStateHandle.getMutableStateFlow(key: String, initialValue: T): MutableStateFlow&lt;T&gt; {{
    val initial = this.get&lt;T&gt;(key) ?: initialValue
    val internalStateFlow = MutableStateFlow(initial)
    return object : MutableStateFlow&lt;T&gt; by internalStateFlow {{
        override var value: T
            get() = internalStateFlow.value
            set(v) {{
                internalStateFlow.value = v
                this@getMutableStateFlow[key] = v
            }}

        override suspend fun emit(v: T) {{
            this@getMutableStateFlow[key] = v
            internalStateFlow.emit(v)
        }}

        override fun compareAndSet(expect: T, update: T): Boolean {{
            val success = internalStateFlow.compareAndSet(expect, update)
            if (success) {{
                this@getMutableStateFlow[key] = update
            }}
            return success
        }}
    }}
}}

class CounterViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {{
    // Usamos SavedStateHandle para que el valor sobreviva incluso a Process Death
    private val _count = savedStateHandle.getMutableStateFlow("counter_key", 0)
    val count = _count.asStateFlow()

    fun increment() {{
        _count.value++
    }}
}}</code></pre>

<!-- PÁGINA 11: CÓDIGO MAIN ACTIVITY -->
<div class="page-break"></div>
<h3>9.2. <code>MainActivity.kt</code></h3>
<pre><code>package com.paulrosero.laboratorio1

import android.app.ActivityManager
import android.app.ApplicationStartInfo
import android.content.Context
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.paulrosero.laboratorio1.ui.theme.Laboratorio1Theme

class MainActivity : ComponentActivity() {{
    private val TAG = "LIFECYCLE_DEBUG"

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate: La Activity se está creando")

        // Reto Android 16: Trazabilidad de Inicio con ApplicationStartInfo
        detectApplicationStartType(savedInstanceState)

        setContent {{
            Laboratorio1Theme {{
                val viewModel: CounterViewModel = viewModel()
                val count by viewModel.count.collectAsState()
                var localCounter by remember {{ mutableStateOf(0) }}

                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {{
                    Column(
                        modifier = Modifier.fillMaxSize().padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {{
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
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
                            shape = RoundedCornerShape(16.dp),
                            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
                        ) {{
                            Column(
                                modifier = Modifier.fillMaxWidth().padding(20.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {{
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
                                Button(onClick = {{ viewModel.increment() }}) {{
                                    Text("Incrementar", fontSize = 16.sp)
                                }}
                            }}
                        }}

                        Spacer(modifier = Modifier.height(20.dp))

                        // Tarjeta Contador Local (Fase 2 - Demostración de Pérdida en Rotación)
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                            shape = RoundedCornerShape(16.dp)
                        ) {{
                            Column(
                                modifier = Modifier.fillMaxWidth().padding(16.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {{
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
                                    onClick = {{ localCounter++ }},
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                                ) {{
                                    Text("Incrementar Local")
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}

    private fun detectApplicationStartType(savedInstanceState: Bundle?) {{
        try {{
            if (Build.VERSION.SDK_INT >= 35) {{ // Android 15 & 16 (API 36)
                val am = getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
                val startInfoList = am?.getHistoricalProcessStartReasons(1)
                if (!startInfoList.isNullOrEmpty()) {{
                    val info = startInfoList[0]
                    val startTypeStr = when (info.startType) {{
                        ApplicationStartInfo.START_TYPE_COLD -> "Fría (Cold Start)"
                        ApplicationStartInfo.START_TYPE_WARM -> "Cálida (Warm Start)"
                        ApplicationStartInfo.START_TYPE_HOT -> "Caliente (Hot Start)"
                        else -> "Tipo desconocido (${{info.startType}})"
                    }}
                    Log.d(TAG, "ApplicationStartInfo (Android 16): Inicio de forma $startTypeStr [Reason: ${{info.reason}}]")
                    return
                }}
            }}
        }} catch (e: Exception) {{
            Log.w(TAG, "Error obteniendo ApplicationStartInfo: ${{e.message}}")
        }}

        val fallbackType = if (savedInstanceState == null) "Fría (Cold Start)" else "Cálida (Warm Start)"
        Log.d(TAG, "Trazabilidad de Inicio: Inicio de forma $fallbackType")
    }}

    override fun onStart() {{ super.onStart(); Log.d(TAG, "onStart: La Activity es visible") }}
    override fun onResume() {{ super.onResume(); Log.d(TAG, "onResume: La Activity tiene el foco (interactuable)") }}
    override fun onPause() {{ super.onPause(); Log.d(TAG, "onPause: La Activity pierde el foco") }}
    override fun onStop() {{ super.onStop(); Log.d(TAG, "onStop: La Activity ya no es visible") }}
    override fun onDestroy() {{ super.onDestroy(); Log.d(TAG, "onDestroy: La Activity va a ser destruida") }}
}}</code></pre>

<div class="page-break"></div>
<h3>9.3. <code>app/build.gradle.kts</code></h3>
<pre><code>plugins {{
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}}

android {{
    namespace = "com.example.laboratorio1"
    compileSdk = 36

    defaultConfig {{
        applicationId = "com.example.laboratorio1"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }}
    kotlinOptions {{
        jvmTarget = "21"
    }}
    buildFeatures {{
        compose = true
    }}
}}

dependencies {{
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)
}}</code></pre>

<h3>9.4. <code>settings.gradle.kts</code></h3>
<pre><code>pluginManagement {{
    repositories {{
        google {{
            content {{
                includeGroupByRegex("com\\.android.*")
                includeGroupByRegex("com\\.google.*")
                includeGroupByRegex("androidx.*")
            }}
        }}
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "LifecycleMaster"
include(":app")</code></pre>

<div class="report-footer">
  <span>RDA1 • Laboratorio 2.1: Dominio del Ciclo de Vida y Persistencia de Estado</span>
  <span>Grupo 1 — Android 16 API 36</span>
</div>

</body>
</html>
"""

with open("capturas/informe_preview.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML generado exitosamente. Generando PDF con Playwright...")

output_pdf = "Informe_Laboratorio_2.1_CicloDeVida_Grupo1.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until="networkidle")
    page.pdf(
        path=output_pdf,
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
    )
    browser.close()

file_size = os.path.getsize(output_pdf)
print(f"PDF generado con exito: {{output_pdf}} ({{file_size}} bytes)")
