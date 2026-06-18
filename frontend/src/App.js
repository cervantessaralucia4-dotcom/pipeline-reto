// ═══════════════════════════════════════════════════════════════
//  App.js — HealthAnalytics IPS Dashboard
//  React 19 + Axios + Recharts + react-icons
//  Sidebar con 7 secciones + control de roles
// ═══════════════════════════════════════════════════════════════
import { useState, useEffect, useCallback, useMemo } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from "recharts";
import {
  FiActivity, FiUsers, FiAlertTriangle, FiTrendingUp,
  FiCheckCircle, FiDroplet, FiBarChart2, FiLogOut,
  FiRefreshCw, FiHeart, FiDatabase, FiCpu, FiFileText,
  FiShield, FiPlay, FiUser, FiPlusCircle, FiDownload,
} from "react-icons/fi";
import "./App.css";

const API      = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";
const PAGE_SIZE = 10;

const RISK_COLORS = { "Crítico":"#ef4444","Alto":"#f59e0b","Medio":"#3b82f6","Bajo":"#10b77f" };
const RISK_BADGE  = { "Crítico":"badge b-critico","Alto":"badge b-alto","Medio":"badge b-medio","Bajo":"badge b-bajo" };

// ── Axios helper ──────────────────────────────────────────────
function authHeaders() {
  return { Authorization: `Bearer ${localStorage.getItem("token")}` };
}

// ── Tooltip Recharts ──────────────────────────────────────────
const CTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:"#0b1628", border:"0.5px solid rgba(255,255,255,0.13)", borderRadius:8, padding:"8px 12px", fontSize:12, color:"#e8f0ff" }}>
      {label && <p style={{ color:"#8596b3", marginBottom:4 }}>{label}</p>}
      {payload.map((p,i) => <p key={i} style={{ color: p.fill||p.color||"#e8f0ff" }}>{p.name}: <strong>{p.value?.toLocaleString()}</strong></p>)}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════
//  LOGIN
// ═══════════════════════════════════════════════════════════════
function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  const handleSubmit = async () => {
    if (!username || !password) { setError("Completa todos los campos."); return; }
    setLoading(true); setError("");
    try {
      // 1. Obtener token JWT
      const { data } = await axios.post(`${API}/token/`, { username, password });

      // 2. Intentar obtener perfil (puede fallar si no tiene UserProfile aún)
      let userData = { username, is_superuser: true, profile: { rol: "administrador" } };
      try {
        const profile = await axios.get(`${API}/auth/me/`, {
          headers: { Authorization: `Bearer ${data.access}` }
        });
        userData = profile.data;
      } catch {
        // Si falla auth/me, asumimos administrador (superusuario de CLI)
      }

      onLogin(data.access, userData);
    } catch {
      setError("Credenciales incorrectas. Verifica tu usuario y contraseña.");
    } finally { setLoading(false); }
  };

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-logo">
          <div className="login-logo-icon"><FiActivity /></div>
          <span className="login-brand">Health<span>care</span> Analytics</span>
        </div>
        <h1 className="login-title">Iniciar sesión</h1>
        <p className="login-sub">Panel de analítica clínica — HealthAnalytics IPS</p>
        <label className="login-label">Usuario</label>
        <input className="login-input" type="text" placeholder="Tu usuario" value={username}
          onChange={e => setUsername(e.target.value)} onKeyDown={e => e.key==="Enter" && handleSubmit()} />
        <label className="login-label">Contraseña</label>
        <input className="login-input" type="password" placeholder="••••••••" value={password}
          onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key==="Enter" && handleSubmit()} />
        <button className="login-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Ingresando..." : "Ingresar"}
        </button>
        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SIDEBAR
// ═══════════════════════════════════════════════════════════════
function Sidebar({ active, setActive, user, onLogout }) {
  const rol = user?.profile?.rol || "medico";

  const items = [
    { key:"dashboard", label:"Dashboard",       icon:<FiActivity />,  roles:["administrador","medico","analista"] },
    { key:"pacientes", label:"Pacientes",        icon:<FiUsers />,     roles:["administrador","medico","analista"] },
    { key:"etl",       label:"ETL",              icon:<FiDatabase />,  roles:["administrador","analista"] },
    { key:"analytics", label:"Analytics",        icon:<FiBarChart2 />, roles:["administrador","medico","analista"] },
    { key:"ml",        label:"Machine Learning", icon:<FiCpu />,       roles:["administrador","analista"] },
    { key:"reportes",  label:"Reportes",         icon:<FiFileText />,  roles:["administrador","medico","analista"] },
    { key:"usuarios",  label:"Usuarios",         icon:<FiShield />,    roles:["administrador"] },
  ];

  const visible = items.filter(i => i.roles.includes(rol) || user?.is_superuser);

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon"><FiActivity /></div>
        <div className="sidebar-brand">Health<span>care</span><br/>Analytics</div>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-label">Menú principal</div>
        {visible.map(item => (
          <button key={item.key}
            className={`sidebar-item ${active === item.key ? "active" : ""}`}
            onClick={() => setActive(item.key)}
          >
            <span className="sidebar-item-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      <div className="sidebar-bottom">
        <div className="sidebar-user">
          <div className="sidebar-avatar"><FiUser /></div>
          <div className="sidebar-user-info">
            <div className="sidebar-username">{user?.username || "Usuario"}</div>
            <div className="sidebar-role">{rol}</div>
          </div>
        </div>
        <button className="btn-logout" onClick={onLogout}>
          <FiLogOut size={12} /> Cerrar sesión
        </button>
      </div>
    </aside>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: DASHBOARD
// ═══════════════════════════════════════════════════════════════
function SectionDashboard() {
  const [kpis, setKpis]       = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState("");

  const fetch = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const { data } = await axios.get(`${API}/dashboard/kpis/`, { headers: authHeaders() });
      setKpis(data);
    } catch { setError("No se pudieron cargar los KPIs."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    fetch();
    const interval = setInterval(fetch, 30000);
    return () => clearInterval(interval);
  }, [fetch]);

  const chartData = useMemo(() => kpis ? [
    { name:"Crítico", value: kpis.critical_patients },
    { name:"Alto",    value: kpis.high_risk },
    { name:"Medio",   value: kpis.medium_risk },
    { name:"Bajo",    value: kpis.low_risk },
  ] : [], [kpis]);

  const total = chartData.reduce((s,d) => s+d.value, 0);

  const kpiList = [
    { label:"Total Pacientes",     val: kpis?.total_patients,       icon:<FiUsers />,        color:"blue" },
    { label:"Pacientes Críticos",  val: kpis?.critical_patients,    icon:<FiAlertTriangle />, color:"red" },
    { label:"Riesgo Alto",         val: kpis?.high_risk,            icon:<FiTrendingUp />,   color:"amber" },
    { label:"Riesgo Medio",        val: kpis?.medium_risk,          icon:<FiActivity />,     color:"cyan" },
    { label:"Riesgo Bajo",         val: kpis?.low_risk,             icon:<FiCheckCircle />,  color:"green" },
    { label:"Glucosa Promedio",    val: kpis ? `${kpis.average_glucose} mg/dL` : "", icon:<FiDroplet />, color:"purple" },
    { label:"IMC Promedio",        val: kpis?.average_bmi,          icon:<FiBarChart2 />,    color:"teal" },
    { label:"Presión Arterial",    val: kpis ? `${kpis.average_systolic}/${kpis.average_diastolic} mmHg` : "", icon:<FiHeart />, color:"red" },
    { label:"Frec. Cardíaca",      val: kpis?.average_heart_rate,   icon:<FiActivity />,     color:"cyan" },
    { label:"Colesterol Prom.",    val: kpis?.average_cholesterol,  icon:<FiDroplet />,      color:"purple" },
    { label:"Saturación O₂",       val: kpis?.average_oxygen_sat,   icon:<FiBarChart2 />,    color:"teal" },
    { label:"Temperatura Prom.",   val: kpis?.average_temperature,  icon:<FiBarChart2 />,    color:"blue" },
  ];

  return (
    <>
      {error && <div className="alert alert-error">{error}</div>}

      <div>
        <p className="sec-label">Indicadores clave</p>
        <div className="kpi-grid">
          {kpiList.map((k,i) => (
            <div key={i} className={`kpi-card ${k.color}`}>
              <div className="kpi-icon">{k.icon}</div>
              {loading
                ? <div className="skeleton" style={{height:22,width:"60%"}} />
                : <div className="kpi-value">{typeof k.val === "number" ? k.val.toLocaleString() : k.val}</div>
              }
              <div className="kpi-label">{k.label}</div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <p className="sec-label">Visualizaciones</p>
        <div className="charts-row">

          {/* Pie */}
          <div className="chart-card">
            <div className="chart-title ct-green">Distribución de riesgo</div>
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie data={chartData} dataKey="value" innerRadius={45} outerRadius={70} paddingAngle={2}>
                  {chartData.map((e,i) => <Cell key={i} fill={RISK_COLORS[e.name]} />)}
                </Pie>
                <Tooltip content={<CTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pie-legend">
              {chartData.map(d => (
                <div className="leg-item" key={d.name}>
                  <div className="leg-dot" style={{background:RISK_COLORS[d.name]}} />
                  <span className="leg-name">{d.name}</span>
                  <span className="leg-pct">{total > 0 ? ((d.value/total)*100).toFixed(1) : 0}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bar */}
          <div className="chart-card">
            <div className="chart-title ct-blue">Pacientes por nivel de riesgo</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={chartData} barSize={32}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" tick={{fill:"#8596b3",fontSize:11}} axisLine={{stroke:"rgba(255,255,255,0.07)"}} tickLine={false} />
                <YAxis tick={{fill:"#8596b3",fontSize:11}} axisLine={false} tickLine={false} />
                <Tooltip content={<CTooltip />} cursor={{fill:"rgba(255,255,255,0.03)"}} />
                <Bar dataKey="value" name="Pacientes" radius={[4,4,0,0]}>
                  {chartData.map((e,i) => <Cell key={i} fill={RISK_COLORS[e.name]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Clinical */}
          <div className="chart-card">
            <div className="chart-title ct-cyan">Indicadores clínicos</div>
            <div className="clin-stats" style={{gridTemplateColumns:"repeat(2,1fr)"}}>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_glucose ?? "—"}</div><div className="clin-stat-lbl">Glucosa (mg/dL)</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_bmi ?? "—"}</div><div className="clin-stat-lbl">IMC</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_systolic ?? "—"}/{kpis?.average_diastolic ?? "—"}</div><div className="clin-stat-lbl">Presión arterial (mmHg)</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_heart_rate ?? "—"}</div><div className="clin-stat-lbl">Frec. cardíaca (lpm)</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_cholesterol ?? "—"}</div><div className="clin-stat-lbl">Colesterol (mg/dL)</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_oxygen_sat ?? "—"}</div><div className="clin-stat-lbl">Saturación O₂ (%)</div></div>
              <div className="clin-stat"><div className="clin-stat-val">{kpis?.average_temperature ?? "—"}</div><div className="clin-stat-lbl">Temperatura (°C)</div></div>
              <div className="clin-stat">
                <div className="clin-stat-val">{kpis && kpis.total_patients > 0 ? ((kpis.critical_patients/kpis.total_patients)*100).toFixed(1)+"%" : "—"}</div>
                <div className="clin-stat-lbl">% Críticos</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: PACIENTES
// ═══════════════════════════════════════════════════════════════
function SectionPacientes() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");
  const [search, setSearch]     = useState("");
  const [sortKey, setSortKey]   = useState("id");
  const [sortDir, setSortDir]   = useState("asc");
  const [page, setPage]         = useState(0);

  const fetchPatients = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const { data } = await axios.get(`${API}/patients/`, { headers: authHeaders() });
      setPatients(Array.isArray(data) ? data : data.results || []);
    } catch { setError("No se pudieron cargar los pacientes."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    fetchPatients();
    const interval = setInterval(fetchPatients, 30000);
    return () => clearInterval(interval);
  }, [fetchPatients]);

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return patients
      .filter(p => !q || `${p.first_name} ${p.last_name}`.toLowerCase().includes(q) ||
        p.disease_risk?.toLowerCase().includes(q) || String(p.id).includes(q))
      .sort((a,b) => {
        let va = sortKey === "nombre" ? `${a.first_name}${a.last_name}`.toLowerCase() : a[sortKey];
        let vb = sortKey === "nombre" ? `${b.first_name}${b.last_name}`.toLowerCase() : b[sortKey];
        if (va < vb) return sortDir === "asc" ? -1 : 1;
        if (va > vb) return sortDir === "asc" ? 1 : -1;
        return 0;
      });
  }, [patients, search, sortKey, sortDir]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage   = Math.min(page, totalPages - 1);
  const pageData   = filtered.slice(safePage * PAGE_SIZE, (safePage+1)*PAGE_SIZE);

  const handleSort = key => {
    if (key === sortKey) setSortDir(d => d === "asc" ? "desc" : "asc");
    else { setSortKey(key); setSortDir("asc"); }
    setPage(0);
  };

  const arrow = key => (
    <span className={`sort-icon ${sortKey===key?"on":""}`}>
      {sortKey===key ? (sortDir==="asc"?"▲":"▼") : "▲"}
    </span>
  );

  return (
    <>
      {error && <div className="alert alert-error">{error}</div>}
      <div className="table-card">
        <div className="table-header">
          <div className="table-title">
            <FiHeart size={13} style={{color:"#3b82f6"}} />
            Pacientes registrados
            {!loading && <span style={{color:"#4a607e",fontWeight:400}}> ({filtered.length})</span>}
          </div>
          <div className="tbl-actions">
            <input className="table-search" type="text" placeholder="Buscar por nombre, riesgo o ID…"
              value={search} onChange={e => { setSearch(e.target.value); setPage(0); }} />
            <button className="btn btn-ghost" onClick={fetchPatients}><FiRefreshCw size={12}/></button>
          </div>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th className={sortKey==="id"?"sorted":""} onClick={()=>handleSort("id")}>ID {arrow("id")}</th>
                <th className={sortKey==="nombre"?"sorted":""} onClick={()=>handleSort("nombre")}>Paciente {arrow("nombre")}</th>
                <th className={sortKey==="age"?"sorted":""} onClick={()=>handleSort("age")}>Edad {arrow("age")}</th>
                <th>Sexo</th>
                <th>P. Sistólica</th>
                <th>P. Diastólica</th>
                <th>Frec. Cardíaca</th>
                <th>Glucosa</th>
                <th>Colesterol</th>
                <th>Sat. O₂</th>
                <th>Temperatura</th>
                <th>IMC</th>
                <th className={sortKey==="disease_risk"?"sorted":""} onClick={()=>handleSort("disease_risk")}>Riesgo {arrow("disease_risk")}</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={14} style={{textAlign:"center",padding:24,color:"#4a607e"}}>Cargando pacientes…</td></tr>
              ) : pageData.length === 0 ? (
                <tr><td colSpan={14} style={{textAlign:"center",padding:28,color:"#4a607e"}}>No se encontraron pacientes.</td></tr>
              ) : pageData.map(p => (
                <tr key={p.id}>
                  <td className="cell-id">#{String(p.id).padStart(4,"0")}</td>
                  <td className="cell-name">{p.first_name} {p.last_name}</td>
                  <td>{p.age} años</td>
                  <td><span className="b-sex">{p.sex==="M"?"Masc":"Fem"}</span></td>
                  <td>{p.systolic_pressure ?? "—"}</td>
                  <td>{p.diastolic_pressure ?? "—"}</td>
                  <td>{p.heart_rate ?? "—"}</td>
                  <td>{p.glucose ?? "—"}</td>
                  <td>{p.cholesterol ?? "—"}</td>
                  <td>{p.oxygen_saturation ?? "—"}</td>
                  <td>{p.temperature ?? "—"}</td>
                  <td>{p.bmi ?? "—"}</td>
                  <td><span className={RISK_BADGE[p.disease_risk]||"badge"}>{p.disease_risk}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {!loading && filtered.length > PAGE_SIZE && (
          <div className="pagination">
            <span className="pag-info">{safePage*PAGE_SIZE+1}–{Math.min((safePage+1)*PAGE_SIZE,filtered.length)} de {filtered.length}</span>
            <div className="pag-btns">
              <button className="pag-btn" disabled={safePage===0} onClick={()=>setPage(safePage-1)}>Anterior</button>
              <button className="pag-btn" disabled={safePage>=totalPages-1} onClick={()=>setPage(safePage+1)}>Siguiente</button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: ETL
// ═══════════════════════════════════════════════════════════════
function SectionETL() {
  const [running, setRunning]   = useState(false);
  const [result, setResult]     = useState(null);
  const [error, setError]       = useState("");
  const [historial, setHistorial] = useState([]);
  const [hLoading, setHLoading] = useState(true);
  const [calidad, setCalidad]     = useState(null);
  const [calidadLoading, setCalidadLoading] = useState(false);

  const fetchHistorial = useCallback(async () => {
    setHLoading(true);
    try {
      const { data } = await axios.get(`${API}/etl/historial/`, { headers: authHeaders() });
      setHistorial(data);
    } catch {} finally { setHLoading(false); }
  }, []);

  useEffect(() => { fetchHistorial(); }, [fetchHistorial]);

  const runETL = async () => {
    setRunning(true); setError(""); setResult(null);
    try {
      const { data } = await axios.post(`${API}/etl/run/`, {}, { headers: authHeaders() });
      setResult(data);
      fetchHistorial();
    } catch (e) {
      setError(e.response?.data?.mensaje || "Error al ejecutar el ETL.");
    } finally { setRunning(false); }
  };

  return (
    <>
      <div className="etl-run-card">
        <p className="sec-label">Ejecutar pipeline ETL</p>
        <p style={{fontSize:12,color:"#8596b3",marginBottom:14}}>
          Procesa el dataset clínico original: extrae, limpia, transforma y carga los pacientes en la base de datos.
        </p>
        <button className="btn btn-success" onClick={runETL} disabled={running}>
          <FiPlay size={13}/> {running ? "Ejecutando ETL…" : "Ejecutar ETL ahora"}
        </button>

        {error && <div className="alert alert-error" style={{marginTop:12}}>{error}</div>}

        {result && (
          <div style={{marginTop:16}}>
            <div className="alert alert-success" style={{marginBottom:12}}>
              ETL completado en {result.tiempo_ejecucion}s — Log #{result.log_id}
            </div>
            <div className="etl-stats-grid">
              {[
                  {label:"Extraídos",      val:result.registros_extraidos,   color:"#3b82f6"},
                  {label:"Duplicados",     val:result.registros_duplicados,  color:"#f59e0b"},
                  {label:"Nulos tratados", val:result.registros_nulos,       color:"#8b5cf6"},
                  {label:"Fuera de rango", val:result.registros_fuera_rango, color:"#ef4444"},
                  {label:"Géneros correg.",val:result.generos_corregidos,    color:"#06b6d4"},
                  {label:"Cargados en BD", val:result.registros_cargados,    color:"#10b77f"},
                ].map((s,i) => (
                <div key={i} className="etl-stat">
                  <div className="etl-stat-val" style={{color:s.color}}>{s.val?.toLocaleString()}</div>
                  <div className="etl-stat-lbl">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div>
        <p className="sec-label">Historial de ejecuciones</p>
        <div className="table-card">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Log #</th><th>Fecha</th><th>Usuario</th>
                  <th>Extraídos</th><th>Cargados</th><th>Tiempo</th><th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {hLoading ? (
                  <tr><td colSpan={7} style={{textAlign:"center",padding:20,color:"#4a607e"}}>Cargando historial…</td></tr>
                ) : historial.length === 0 ? (
                  <tr><td colSpan={7} style={{textAlign:"center",padding:20,color:"#4a607e"}}>No hay ejecuciones registradas.</td></tr>
                ) : historial.map(log => (
                  <tr key={log.id}>
                    <td className="cell-id">#{log.id}</td>
                    <td>{new Date(log.fecha_inicio).toLocaleString("es-CO")}</td>
                    <td>{log.usuario || "—"}</td>
                    <td>{log.registros_extraidos?.toLocaleString()}</td>
                    <td>{log.registros_cargados?.toLocaleString()}</td>
                    <td>{log.tiempo_ejecucion}s</td>
                    <td><span className={`badge b-${log.estado}`}>{log.estado}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Reporte de Calidad de Datos */}
      <div>
        <p className="sec-label">Calidad de datos del dataset original</p>
        <div className="card" style={{padding:20}}>
          <p style={{fontSize:12,color:"#8596b3",marginBottom:14}}>
            Analiza el archivo Excel original para identificar valores no numéricos,
            nulos y fuera de rango antes de la limpieza del ETL.
          </p>
          <button className="btn btn-ghost" onClick={async () => {
            setCalidadLoading(true); setCalidad(null);
            try {
              const { data } = await axios.get(`${API}/etl/calidad/`, { headers: authHeaders() });
              setCalidad(data);
            } catch { setError("Error al cargar reporte de calidad."); }
            finally { setCalidadLoading(false); }
          }} disabled={calidadLoading}>
            <FiFileText size={13}/> {calidadLoading ? "Analizando…" : "Generar reporte de calidad"}
          </button>

          {calidad && (
            <div style={{marginTop:16}}>
              <div className="etl-stats-grid">
                <div className="etl-stat"><div className="etl-stat-val" style={{color:"#3b82f6"}}>{calidad.total_registros?.toLocaleString()}</div><div className="etl-stat-lbl">Total registros</div></div>
                <div className="etl-stat"><div className="etl-stat-val" style={{color:"#ef4444"}}>{calidad.resumen?.valores_no_numericos?.toLocaleString()}</div><div className="etl-stat-lbl">Valores no numéricos</div></div>
                <div className="etl-stat"><div className="etl-stat-val" style={{color:"#f59e0b"}}>{calidad.resumen?.valores_nulos?.toLocaleString()}</div><div className="etl-stat-lbl">Valores nulos</div></div>
                <div className="etl-stat"><div className="etl-stat-val" style={{color:"#8b5cf6"}}>{calidad.resumen?.valores_fuera_rango?.toLocaleString()}</div><div className="etl-stat-lbl">Fuera de rango</div></div>
              </div>

              {calidad.columnas?.some(c => c.valores_no_numericos > 0 || c.valores_nulos > 0 || c.valores_fuera_rango > 0) && (
                <div className="table-wrap" style={{marginTop:14}}>
                  <table>
                    <thead>
                      <tr>
                        <th>Columna</th>
                        <th>Rango esperado</th>
                        <th>No numéricos</th>
                        <th>Valores texto</th>
                        <th>Nulos</th>
                        <th>Fuera rango</th>
                        <th>Ejemplos</th>
                      </tr>
                    </thead>
                    <tbody>
                      {calidad.columnas?.filter(c => c.valores_no_numericos > 0 || c.valores_nulos > 0 || c.valores_fuera_rango > 0).map((col,i) => (
                        <tr key={i}>
                          <td><strong>{col.nombre}</strong></td>
                          <td style={{fontSize:11}}>{col.rango_esperado}</td>
                          <td style={{color:col.valores_no_numericos > 0 ? "#ef4444" : "#10b77f"}}>{col.valores_no_numericos}</td>
                          <td style={{fontSize:11,maxWidth:140}}>{col.valores_texto_encontrados?.join(", ") || "—"}</td>
                          <td style={{color:col.valores_nulos > 0 ? "#f59e0b" : "#10b77f"}}>{col.valores_nulos}</td>
                          <td style={{color:col.valores_fuera_rango > 0 ? "#8b5cf6" : "#10b77f"}}>{col.valores_fuera_rango}</td>
                          <td style={{fontSize:11,maxWidth:200}}>
                            {col.ejemplos?.length > 0 ? (
                              <div style={{display:"flex",flexDirection:"column",gap:2}}>
                                {col.ejemplos.slice(0,3).map((ex,j) => (
                                  <div key={j} style={{fontSize:10,color:"#ef4444"}}>
                                    Fila {ex.fila}: "<strong>{ex.valor_original}</strong>" ({ex.paciente})
                                  </div>
                                ))}
                              </div>
                            ) : col.valores_fuera_rango > 0 ? (
                              col.ejemplos_fuera_rango?.slice(0,3).join(", ")
                            ) : "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              <p style={{fontSize:11,color:"#8596b3",marginTop:8}}>
                Total de anomalías detectadas: <strong>{calidad.resumen?.total_anomalias?.toLocaleString()}</strong>
                {calidad.resumen?.total_anomalias > 0 && (
                  <span style={{color:"#10b77f"}}> — Corregidas por el ETL antes de cargar a la BD</span>
                )}
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: ANALYTICS
// ═══════════════════════════════════════════════════════════════
function SectionAnalytics() {
  const [kpis, setKpis]         = useState(null);
  const [stats, setStats]       = useState(null);
  const [seg, setSeg]           = useState(null);
  const [criticos, setCriticos] = useState(null);
  const [loading, setLoading]   = useState(true);
  const [filtroActivo, setFiltroActivo] = useState(null);
  const [filtroPacientes, setFiltroPacientes] = useState([]);
  const [filtroCargando, setFiltroCargando] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [filtroError, setFiltroError] = useState("");
  const [filtroSearch, setFiltroSearch] = useState("");
  const [exportando, setExportando] = useState(null);

  useEffect(() => {
    const h = authHeaders();
    Promise.allSettled([
      axios.get(`${API}/analytics/kpis/`, { headers:h }),
      axios.get(`${API}/analytics/estadisticas/`, { headers:h }),
      axios.get(`${API}/analytics/segmentacion/`, { headers:h }),
      axios.get(`${API}/analytics/criticos/`, { headers:h }),
    ]).then(([k,s,sg,c]) => {
      if (k.status === 'fulfilled') setKpis(k.value.data);
      if (s.status === 'fulfilled') setStats(s.value.data);
      if (sg.status === 'fulfilled') setSeg(sg.value.data);
      if (c.status === 'fulfilled') setCriticos(c.value.data);
    }).finally(() => setLoading(false));
  }, []);

  const abrirFiltro = async (filtro) => {
    setFiltroActivo(filtro); setFiltroCargando(true); setFiltroError(""); setFiltroSearch("");
    try {
      const { data } = await axios.get(`${API}/analytics/pacientes-por-filtro/?filtro=${filtro}`, { headers: authHeaders() });
      setFiltroPacientes(data.pacientes || []);
    } catch {
      setFiltroError("Error al cargar pacientes.");
      setFiltroPacientes([]);
    } finally { setFiltroCargando(false); }
  };

  const cerrarFiltro = () => { setFiltroActivo(null); setFiltroPacientes([]); setFiltroSearch(""); };

  if (loading) return <div style={{color:"#4a607e",padding:24}}>Cargando analítica…</div>;

  const exportFiltro = async (filtro, formato) => {
    setExportando(`${filtro}-${formato}`);
    try {
      const response = await axios.get(`${API}/analytics/export/${formato}/?filtro=${filtro}`, {
        headers: authHeaders(),
        responseType: 'blob',
      });
      const ext = formato === 'csv' ? 'csv' : 'pdf';
      const mime = formato === 'csv' ? 'text/csv;charset=utf-8-sig' : 'application/pdf';
      const url = window.URL.createObjectURL(new Blob([response.data], { type: mime }));
      const link = document.createElement('a'); link.href = url; link.download = `${filtro}.${ext}`; link.click();
      window.URL.revokeObjectURL(url);
    } catch {} finally { setExportando(null); }
  };

  const kpiMed = [
    {label:"Hipertensos",     filtro:"hipertensos",      cant:kpis?.hipertensos?.cantidad,      pct:kpis?.hipertensos?.porcentaje,      c:"c1"},
    {label:"Normotensos",     filtro:"normotensos",      cant:kpis?.normotensos?.cantidad,      pct:kpis?.normotensos?.porcentaje,      c:"c2"},
    {label:"Prehipertensos",  filtro:"prehipertensos",   cant:kpis?.prehipertensos?.cantidad,   pct:kpis?.prehipertensos?.porcentaje,   c:"c3"},
    {label:"Diabéticos",      filtro:"diabeticos",       cant:kpis?.diabeticos?.cantidad,       pct:kpis?.diabeticos?.porcentaje,       c:"c4"},
    {label:"Fumadores",       filtro:"fumadores",        cant:kpis?.fumadores?.cantidad,        pct:kpis?.fumadores?.porcentaje,        c:"c5"},
    {label:"Con antecedentes",filtro:"con_antecedentes", cant:kpis?.con_antecedentes?.cantidad, pct:kpis?.con_antecedentes?.porcentaje, c:"c6"},
    {label:"Alcoholismo",     filtro:"alcoholismo",      cant:kpis?.alcoholismo?.cantidad,      pct:kpis?.alcoholismo?.porcentaje,      c:"c7"},
    {label:"Obesidad",        filtro:"obesidad",         cant:kpis?.obesidad?.cantidad,         pct:kpis?.obesidad?.porcentaje,         c:"c8"},
    {label:"Saturación baja", filtro:"saturacion_baja",  cant:kpis?.saturacion_baja?.cantidad,  pct:kpis?.saturacion_baja?.porcentaje,  c:"c9"},
  ];

  const filtroFiltrados = filtroPacientes.filter(p => {
    const q = filtroSearch.toLowerCase();
    return !q || `${p.first_name} ${p.last_name}`.toLowerCase().includes(q) ||
      p.disease_risk?.toLowerCase().includes(q) || String(p.id).includes(q);
  });

  const statsKeys = ["glucosa","imc","edad","presion_sistolica","presion_diastolica","frecuencia_cardiaca","colesterol","temperatura","saturacion_oxigeno"];

  const totalRiesgo = seg?.por_riesgo?.reduce((s,r) => s+r.cantidad, 0) || 1;

  return (
    <>
      {/* KPIs médicos */}
      <div>
        <p className="sec-label">KPIs médicos — {kpis?.total_pacientes?.toLocaleString()} pacientes</p>
        <div className="kpi-med-grid">
          {kpiMed.map((k,i) => (
            <div key={i} className={`kpi-med-card ${k.c}`}>
              <div style={{cursor:"pointer"}} onClick={() => abrirFiltro(k.filtro)} title="Ver pacientes">
                <div className="kpi-med-val">{k.cant?.toLocaleString() ?? "—"}</div>
                <div className="kpi-med-pct">{k.pct}% del total</div>
                <div className="kpi-med-lbl">{k.label}</div>
              </div>
              <div className="kpi-med-actions">
                <button className="btn btn-xs" onClick={(e) => { e.stopPropagation(); exportFiltro(k.filtro, 'csv'); }}
                  disabled={exportando === `${k.filtro}-csv`} title="Exportar CSV">
                  CSV
                </button>
                <button className="btn btn-xs" onClick={(e) => { e.stopPropagation(); exportFiltro(k.filtro, 'pdf'); }}
                  disabled={exportando === `${k.filtro}-pdf`} title="Exportar PDF">
                  PDF
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Modal de pacientes por filtro */}
      {filtroActivo && (
        <div className="modal-overlay" onClick={cerrarFiltro}>
          <div className="modal modal-filtro" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title">
                Pacientes: {kpiMed.find(k => k.filtro === filtroActivo)?.label || filtroActivo}
                <span style={{fontSize:12,color:"#8596b3",fontWeight:400,marginLeft:8}}>
                  ({filtroPacientes.length} registros)
                </span>
              </div>
              <button className="btn btn-ghost" onClick={cerrarFiltro} style={{padding:"4px 10px",fontSize:14}}>✕</button>
            </div>
            <div className="tbl-actions" style={{marginBottom:10}}>
              <input className="table-search" type="text" placeholder="Buscar por nombre, riesgo o ID..."
                value={filtroSearch} onChange={e => setFiltroSearch(e.target.value)} />
            </div>
            <div className="table-wrap" style={{maxHeight:360,overflowY:"auto"}}>
              {filtroCargando ? (
                <div style={{textAlign:"center",padding:24,color:"#4a607e"}}>Cargando pacientes…</div>
              ) : filtroFiltrados.length === 0 ? (
                <div style={{textAlign:"center",padding:24,color:"#4a607e"}}>No se encontraron pacientes.</div>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>ID</th><th>Paciente</th><th>Edad</th><th>Sexo</th><th>P. Sistólica</th><th>P. Diastólica</th><th>Glucosa</th><th>Colesterol</th><th>Sat. O₂</th><th>IMC</th><th>Riesgo</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtroFiltrados.map(p => (
                      <tr key={p.id}>
                        <td className="cell-id">#{String(p.id).padStart(4,"0")}</td>
                        <td className="cell-name">{p.first_name} {p.last_name}</td>
                        <td>{p.age} años</td>
                        <td><span className="b-sex">{p.sex==="M"?"Masc":"Fem"}</span></td>
                        <td>{p.systolic_pressure ?? "—"}</td>
                        <td>{p.diastolic_pressure ?? "—"}</td>
                        <td>{p.glucose ?? "—"}</td>
                        <td>{p.cholesterol ?? "—"}</td>
                        <td>{p.oxygen_saturation ?? "—"}</td>
                        <td>{p.bmi ?? "—"}</td>
                        <td><span className={RISK_BADGE[p.disease_risk]||"badge"}>{p.disease_risk}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Estadística descriptiva */}
      <div>
        <p className="sec-label">Estadística descriptiva</p>
        <div className="stats-grid">
          {statsKeys.map(k => {
            const d = stats?.[k];
            if (!d) return null;
            return (
              <div key={k} className="stat-card">
                <div className="stat-card-title">{k.replace(/_/g," ").replace(/\b\w/g,l=>l.toUpperCase())}</div>
                {[["Media",d.media],["Mediana",d.mediana],["Moda",d.moda],["Desv. estándar",d.desviacion_estandar],["Mínimo",d.minimo],["Máximo",d.maximo]].map(([label,val])=>(
                  <div key={label} className="stat-row">
                    <span className="stat-row-label">{label}</span>
                    <span className="stat-row-val">{val ?? "—"}</span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>

      {/* Segmentación */}
      <div>
        <p className="sec-label">Segmentación de pacientes</p>
        <div className="seg-row">

          <div className="card" style={{padding:16}}>
            <div className="chart-title ct-green" style={{marginBottom:12}}>Por nivel de riesgo</div>
            <div className="progress-bar-wrap">
              {seg?.por_riesgo?.map(r => (
                <div key={r.disease_risk} className="pb-row">
                  <div className="pb-meta">
                    <span className="pb-label">{r.disease_risk}</span>
                    <span className="pb-val">{r.cantidad?.toLocaleString()}</span>
                  </div>
                  <div className="pb-track">
                    <div className="pb-fill" style={{width:`${(r.cantidad/totalRiesgo)*100}%`, background:RISK_COLORS[r.disease_risk]||"#3b82f6"}} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card" style={{padding:16}}>
            <div className="chart-title ct-blue" style={{marginBottom:12}}>Por grupo de edad</div>
            <div className="progress-bar-wrap">
              {Object.entries(seg?.por_grupo_edad||{}).map(([rango,cant]) => (
                <div key={rango} className="pb-row">
                  <div className="pb-meta">
                    <span className="pb-label">{rango} años</span>
                    <span className="pb-val">{cant?.toLocaleString()}</span>
                  </div>
                  <div className="pb-track">
                    <div className="pb-fill" style={{width:`${(cant/(kpis?.total_pacientes||1))*100}%`, background:"#3b82f6"}} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card" style={{padding:16}}>
            <div className="chart-title ct-cyan" style={{marginBottom:12}}>Clasificación IMC</div>
            <div className="progress-bar-wrap">
              {[["Bajo peso","bajo_peso","#06b6d4"],["Normal","normal","#10b77f"],["Sobrepeso","sobrepeso","#f59e0b"],["Obesidad","obesidad","#ef4444"]].map(([label,key,color]) => (
                <div key={key} className="pb-row">
                  <div className="pb-meta">
                    <span className="pb-label">{label}</span>
                    <span className="pb-val">{seg?.por_imc?.[key]?.toLocaleString()}</span>
                  </div>
                  <div className="pb-track">
                    <div className="pb-fill" style={{width:`${((seg?.por_imc?.[key]||0)/(kpis?.total_pacientes||1))*100}%`,background:color}} />
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* Pacientes críticos */}
      <div>
        <p className="sec-label">Alertas clínicas</p>
        <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10,marginBottom:14}}>
          {[
            {label:"Presión sistólica > 180", val:criticos?.alertas?.presion_sistolica_gt_180, color:"#ef4444"},
            {label:"Glucosa > 300",           val:criticos?.alertas?.glucosa_gt_300,           color:"#f59e0b"},
            {label:"Saturación < 85%",        val:criticos?.alertas?.saturacion_lt_85,         color:"#8b5cf6"},
          ].map((a,i) => (
            <div key={i} className="card" style={{padding:14,display:"flex",flexDirection:"column",gap:6}}>
              <div style={{fontFamily:"'Syne',sans-serif",fontSize:22,fontWeight:700,color:a.color}}>{a.val?.toLocaleString() ?? "—"}</div>
              <div style={{fontSize:11,color:"#8596b3"}}>{a.label}</div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: MACHINE LEARNING
// ═══════════════════════════════════════════════════════════════
function SectionML({ user }) {
  const rol = user?.profile?.rol || "medico";
  const [metrics, setMetrics] = useState(null);
  const [training, setTraining] = useState(false);
  const [trainMsg, setTrainMsg] = useState("");
  const [predForm, setPredForm] = useState({ edad:"", IMC:"", glucosa:"", colesterol:"", "presión_sistólica":"", frecuencia_cardiaca:"" });
  const [predResult, setPredResult] = useState(null);
  const [predLoading, setPredLoading] = useState(false);
  const [predError, setPredError] = useState("");

  const fetchMetrics = useCallback(async () => {
    try {
      const { data } = await axios.get(`${API}/ml/metrics/`, { headers: authHeaders() });
      setMetrics(data);
    } catch {}
  }, []);

  useEffect(() => { fetchMetrics(); }, [fetchMetrics]);

  const train = async () => {
    setTraining(true); setTrainMsg("");
    try {
      const { data } = await axios.post(`${API}/ml/train/`, {}, { headers: authHeaders() });
      setTrainMsg(`✓ Modelo entrenado — Accuracy: ${(data.accuracy*100).toFixed(2)}%`);
      fetchMetrics();
    } catch { setTrainMsg("Error al entrenar el modelo."); }
    finally { setTraining(false); }
  };

  const predict = async () => {
    setPredLoading(true); setPredError(""); setPredResult(null);
    try {
      const body = Object.fromEntries(Object.entries(predForm).map(([k,v]) => [k, parseFloat(v)]));
      const { data } = await axios.post(`${API}/ml/predict/`, body, { headers: authHeaders() });
      setPredResult(data);
    } catch (e) {
      setPredError(e.response?.data?.error || "Error en la predicción.");
    } finally { setPredLoading(false); }
  };

  const riesgoColor = r => ({ "Crítico":"critico","Alto":"alto","Medio":"medio","Bajo":"bajo" }[r] || "bajo");

  return (
    <>
      {/* Métricas */}
      <div>
        <p className="sec-label">Métricas del modelo</p>
        {(rol === "analista" || rol === "administrador" || user?.is_superuser) && (
          <div style={{marginBottom:14,display:"flex",alignItems:"center",gap:10,flexWrap:"wrap"}}>
            <button className="btn btn-success" onClick={train} disabled={training}>
              <FiPlay size={13}/> {training ? "Entrenando…" : "Reentrenar modelo"}
            </button>
            {trainMsg && <span style={{fontSize:12,color:"#6ee7b7"}}>{trainMsg}</span>}
          </div>
        )}
        {metrics ? (
          <>
            <div className="ml-metrics-grid">
              {[
                {label:"Accuracy",  val:`${(metrics.accuracy*100).toFixed(2)}%`},
                {label:"Precision", val:`${(metrics.precision*100).toFixed(2)}%`},
                {label:"Recall",    val:`${(metrics.recall*100).toFixed(2)}%`},
                {label:"F1 Score",  val:`${(metrics.f1_score*100).toFixed(2)}%`},
              ].map((m,i) => (
                <div key={i} className="ml-metric">
                  <div className="ml-metric-val">{m.val}</div>
                  <div className="ml-metric-lbl">{m.label}</div>
                </div>
              ))}
            </div>

            <div className="ml-row" style={{marginTop:12}}>
              {/* Importancia de variables */}
              <div className="card" style={{padding:16}}>
                <div className="chart-title ct-green" style={{marginBottom:12}}>Importancia de variables</div>
                <div className="progress-bar-wrap">
                  {Object.entries(metrics.importancia||{}).sort((a,b)=>b[1]-a[1]).map(([k,v])=>(
                    <div key={k} className="pb-row">
                      <div className="pb-meta">
                        <span className="pb-label">{k}</span>
                        <span className="pb-val">{(v*100).toFixed(1)}%</span>
                      </div>
                      <div className="pb-track">
                        <div className="pb-fill" style={{width:`${v*100}%`,background:"#10b77f"}} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Info entrenamiento */}
              <div className="card" style={{padding:16}}>
                <div className="chart-title ct-blue" style={{marginBottom:12}}>Detalles del entrenamiento</div>
                {[
                  ["Modelo",           metrics.modelo],
                  ["Total registros",  metrics.total_registros?.toLocaleString()],
                  ["Set entrenamiento",metrics.registros_train?.toLocaleString()],
                  ["Set prueba",       metrics.registros_test?.toLocaleString()],
                  ["Fecha",            new Date(metrics.fecha_entrenamiento).toLocaleString("es-CO")],
                ].map(([label,val]) => (
                  <div key={label} className="stat-row">
                    <span className="stat-row-label">{label}</span>
                    <span className="stat-row-val">{val}</span>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="alert alert-info">No hay métricas disponibles. Ejecuta el entrenamiento primero.</div>
        )}
      </div>

      {/* Predicción individual */}
      <div>
        <p className="sec-label">Predicción individual de riesgo</p>
        <div className="card" style={{padding:20}}>
          <p style={{fontSize:12,color:"#8596b3",marginBottom:16}}>
            Ingresa los datos clínicos del paciente para predecir su nivel de riesgo.
          </p>
          <div className="form-grid" style={{marginBottom:14}}>
            {[
              ["edad","Edad (años)","45"],
              ["IMC","IMC","27.5"],
              ["glucosa","Glucosa (mg/dL)","130"],
              ["colesterol","Colesterol (mg/dL)","210"],
              ["presión_sistólica","Presión sistólica","145"],
              ["frecuencia_cardiaca","Frecuencia cardíaca","88"],
            ].map(([key,label,ph]) => (
              <div key={key} className="form-field">
                <label className="form-label">{label}</label>
                <input className="form-input" type="number" placeholder={ph}
                  value={predForm[key]} onChange={e => setPredForm(f => ({...f,[key]:e.target.value}))} />
              </div>
            ))}
          </div>
          <button className="btn btn-primary" onClick={predict} disabled={predLoading}>
            <FiCpu size={13}/> {predLoading ? "Prediciendo…" : "Predecir riesgo"}
          </button>
          {predError && <div className="alert alert-error" style={{marginTop:12}}>{predError}</div>}
          {predResult && (
            <div className={`predict-result ${riesgoColor(predResult.riesgo_predicho)}`} style={{marginTop:14}}>
              <div className="predict-label">Riesgo: {predResult.riesgo_predicho}</div>
              <div style={{fontSize:12,color:"#8596b3",marginBottom:8}}>Probabilidades por clase:</div>
              <div className="predict-probs">
                {Object.entries(predResult.probabilidades||{}).map(([clase,prob]) => (
                  <div key={clase} className="predict-prob-item">
                    <strong>{clase}</strong>: {(prob*100).toFixed(1)}%
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: REPORTES
// ═══════════════════════════════════════════════════════════════
function SectionReportes() {
  const [reporte, setReporte] = useState(null);
  const [loading, setLoading] = useState(true);
  const [csvError, setCsvError] = useState("");
  const [csvLoading, setCsvLoading] = useState(false);
  const [excelLoading, setExcelLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);

  useEffect(() => {
    axios.get(`${API}/reportes/`, { headers: authHeaders() })
      .then(({ data }) => setReporte(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const exportCSV = async () => {
    setCsvError(""); setCsvLoading(true);
    try {
      const response = await axios.get(`${API}/patients/export/csv/`, {
        headers: authHeaders(),
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'text/csv;charset=utf-8-sig' }));
      const link = document.createElement('a'); link.href = url; link.download = 'pacientes.csv'; link.click();
      window.URL.revokeObjectURL(url);
    } catch {
      setCsvError("Error al exportar CSV. Intenta de nuevo.");
    } finally { setCsvLoading(false); }
  };

  const exportExcel = async () => {
    setExcelLoading(true);
    try {
      const response = await axios.get(`${API}/patients/export/excel/`, {
        headers: authHeaders(),
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a'); link.href = url; link.download = 'reporte_pacientes.xlsx'; link.click();
      window.URL.revokeObjectURL(url);
    } catch {
      setCsvError("Error al exportar Excel.");
    } finally { setExcelLoading(false); }
  };

  const exportPDF = async () => {
    setPdfLoading(true);
    try {
      const response = await axios.get(`${API}/patients/export/pdf/`, {
        headers: authHeaders(),
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      const link = document.createElement('a'); link.href = url; link.download = 'reporte_pacientes.pdf'; link.click();
      window.URL.revokeObjectURL(url);
    } catch {
      setCsvError("Error al exportar PDF.");
    } finally { setPdfLoading(false); }
  };

  return (
    <>
      <div>
        <p className="sec-label no-print">Resumen ejecutivo</p>
        {loading ? (
          <div style={{color:"#4a607e"}}>Cargando reporte…</div>
        ) : (
          <div className="report-print-area" style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(180px,1fr))",gap:10}}>
            {[
              {label:"Total pacientes",      val:reporte?.total_patients,          color:"blue"},
              {label:"Pacientes críticos",   val:reporte?.critical_patients,       color:"red"},
              {label:"Glucosa promedio",     val:`${reporte?.average_glucose} mg/dL`, color:"purple"},
              {label:"IMC promedio",         val:reporte?.average_bmi,             color:"teal"},
              {label:"Presión sistólica",    val:reporte?.average_systolic,        color:"red"},
              {label:"Presión diastólica",   val:reporte?.average_diastolic,       color:"amber"},
              {label:"Frec. cardíaca",       val:reporte?.average_heart_rate,      color:"cyan"},
              {label:"Colesterol promedio",  val:reporte?.average_cholesterol,     color:"purple"},
              {label:"Saturación O₂",        val:reporte?.average_oxygen_sat,      color:"teal"},
              {label:"Temperatura promedio", val:reporte?.average_temperature,     color:"blue"},
            ].map((r,i) => (
              <div key={i} className={`kpi-card ${r.color}`}>
                <div className="kpi-value">{typeof r.val === "number" ? r.val?.toLocaleString() : r.val}</div>
                <div className="kpi-label">{r.label}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="no-print">
        <p className="sec-label">Exportar datos</p>
        <div className="card" style={{padding:20,display:"flex",flexDirection:"column",gap:12}}>
          <p style={{fontSize:12,color:"#8596b3"}}>
            Descarga los datos del sistema en los formatos disponibles.
          </p>
          {csvError && <div className="alert alert-error" style={{fontSize:12}}>{csvError}</div>}
          <div style={{display:"flex",gap:10,flexWrap:"wrap"}}>
            <button className="btn btn-ghost" onClick={exportCSV} disabled={csvLoading}>
              <FiDownload size={13}/> {csvLoading ? "Exportando…" : "CSV"}
            </button>
            <button className="btn btn-ghost" onClick={exportExcel} disabled={excelLoading}>
              <FiDownload size={13}/> {excelLoading ? "Exportando…" : "Excel"}
            </button>
            <button className="btn btn-primary" onClick={exportPDF} disabled={pdfLoading}>
              <FiFileText size={13}/> {pdfLoading ? "Exportando…" : "PDF"}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  SECCIÓN: USUARIOS (solo admin)
// ═══════════════════════════════════════════════════════════════
function SectionUsuarios() {
  const [users, setUsers]   = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm]     = useState({ username:"", email:"", first_name:"", last_name:"", password:"", password2:"", rol:"medico" });
  const [saving, setSaving] = useState(false);
  const [msg, setMsg]       = useState("");

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/auth/users/`, { headers: authHeaders() });
      setUsers(data);
    } catch {} finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchUsers(); }, [fetchUsers]);

  const createUser = async () => {
    setSaving(true); setMsg("");
    try {
      await axios.post(`${API}/auth/register/`, form, { headers: authHeaders() });
      setMsg("Usuario creado correctamente.");
      setShowModal(false);
      setForm({ username:"", email:"", first_name:"", last_name:"", password:"", password2:"", rol:"medico" });
      fetchUsers();
    } catch (e) {
      setMsg(Object.values(e.response?.data||{}).flat().join(" ") || "Error al crear usuario.");
    } finally { setSaving(false); }
  };

  const changeRol = async (id, rol) => {
    try {
      await axios.put(`${API}/auth/users/${id}/rol/`, { rol }, { headers: authHeaders() });
      fetchUsers();
    } catch {}
  };

  return (
    <>
      {msg && <div className={`alert ${msg.includes("Error") ? "alert-error" : "alert-success"}`}>{msg}</div>}

      <div className="table-card">
        <div className="table-header">
          <div className="table-title">Gestión de usuarios</div>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <FiPlusCircle size={13}/> Nuevo usuario
          </button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Usuario</th><th>Nombre</th><th>Email</th><th>Rol</th><th>Activo</th><th>Cambiar rol</th></tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={7} style={{textAlign:"center",padding:20,color:"#4a607e"}}>Cargando…</td></tr>
              ) : users.map(u => (
                <tr key={u.id}>
                  <td className="cell-id">#{u.id}</td>
                  <td className="cell-name">{u.username}</td>
                  <td>{u.first_name} {u.last_name}</td>
                  <td>{u.email || "—"}</td>
                  <td><span className="badge b-medio">{u.profile?.rol || "—"}</span></td>
                  <td>{u.is_active ? <span className="badge b-bajo">Activo</span> : <span className="badge b-fallido">Inactivo</span>}</td>
                  <td>
                    <select className="form-select" style={{padding:"4px 8px",fontSize:11,width:"auto"}}
                      value={u.profile?.rol || "medico"}
                      onChange={e => changeRol(u.id, e.target.value)}>
                      <option value="administrador">Administrador</option>
                      <option value="medico">Médico</option>
                      <option value="analista">Analista</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-title"><FiPlusCircle /> Crear nuevo usuario</div>
            <div className="form-grid">
              {[["username","Usuario"],["email","Email"],["first_name","Nombre"],["last_name","Apellido"],["password","Contraseña"],["password2","Confirmar contraseña"]].map(([k,l]) => (
                <div key={k} className="form-field">
                  <label className="form-label">{l}</label>
                  <input className="form-input" type={k.includes("password")?"password":"text"}
                    value={form[k]} onChange={e => setForm(f=>({...f,[k]:e.target.value}))} />
                </div>
              ))}
              <div className="form-field">
                <label className="form-label">Rol</label>
                <select className="form-select" value={form.rol} onChange={e => setForm(f=>({...f,rol:e.target.value}))}>
                  <option value="administrador">Administrador</option>
                  <option value="medico">Médico</option>
                  <option value="analista">Analista</option>
                </select>
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancelar</button>
              <button className="btn btn-primary" onClick={createUser} disabled={saving}>
                {saving ? "Guardando…" : "Crear usuario"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
//  DASHBOARD (layout principal con sidebar)
// ═══════════════════════════════════════════════════════════════
const SECTION_TITLES = {
  dashboard: "Dashboard Principal",
  pacientes: "Gestión de Pacientes",
  etl:       "Pipeline ETL",
  analytics: "Analítica de Datos",
  ml:        "Machine Learning",
  reportes:  "Reportes",
  usuarios:  "Gestión de Usuarios",
};

function Dashboard({ user, onLogout }) {
  const [active, setActive] = useState("dashboard");

  const renderSection = () => {
    switch(active) {
      case "dashboard": return <SectionDashboard />;
      case "pacientes": return <SectionPacientes user={user} />;
      case "etl":       return <SectionETL />;
      case "analytics": return <SectionAnalytics />;
      case "ml":        return <SectionML user={user} />;
      case "reportes":  return <SectionReportes />;
      case "usuarios":  return <SectionUsuarios />;
      default:          return <SectionDashboard />;
    }
  };

  return (
    <div className="app-layout">
      <Sidebar active={active} setActive={setActive} user={user} onLogout={onLogout} />
      <div className="main-content">
        <div className="topbar">
          <div className="topbar-title">{SECTION_TITLES[active]}</div>
          <div className="topbar-right">
            <span className="badge-live">En vivo</span>
          </div>
        </div>
        <div className="page-content">
          {renderSection()}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
//  APP ROOT
// ═══════════════════════════════════════════════════════════════
export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user,  setUser]  = useState(() => {
    try { return JSON.parse(localStorage.getItem("user")); } catch { return null; }
  });

  const handleLogin = (access, userData) => {
    localStorage.setItem("token", access);
    localStorage.setItem("user", JSON.stringify(userData));
    setToken(access);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return token
    ? <Dashboard user={user} onLogout={handleLogout} />
    : <Login onLogin={handleLogin} />;
}