// ═══════════════════════════════════════════════════════════════
//  App.js — Healthcare Analytics Dashboard
//  Compatible con React 19 + Recharts + Axios + react-icons
//  API: Django REST Framework + JWT (tu backend actual)
// ═══════════════════════════════════════════════════════════════

import { useEffect, useState, useCallback, useMemo } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from "recharts";
import {
  FiActivity, FiUsers, FiAlertTriangle, FiTrendingUp,
  FiCheckCircle, FiDroplet, FiBarChart2, FiLogOut,
  FiSearch, FiRefreshCw, FiHeart,
} from "react-icons/fi";
import "./App.css";

// ── Constantes ───────────────────────────────────────────────
const API = "http://127.0.0.1:8000/api";
const PAGE_SIZE = 10;

const RISK_COLORS = {
  "Crítico": "#ef4444",
  "Alto":    "#f59e0b",
  "Medio":   "#3b82f6",
  "Bajo":    "#10b77f",
};

const RISK_BADGE = {
  "Crítico": "badge badge-critico",
  "Alto":    "badge badge-alto",
  "Medio":   "badge badge-medio",
  "Bajo":    "badge badge-bajo",
};

// ─────────────────────────────────────────────────────────────
//  CUSTOM TOOLTIP para recharts
// ─────────────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "#0b1628",
      border: "0.5px solid rgba(255,255,255,0.13)",
      borderRadius: 8,
      padding: "8px 12px",
      fontSize: 12,
      color: "#e8f0ff",
      fontFamily: "'DM Sans', sans-serif",
    }}>
      {label && <p style={{ color: "#8596b3", marginBottom: 4 }}>{label}</p>}
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.fill || p.color || "#e8f0ff" }}>
          {p.name}: <strong>{p.value?.toLocaleString()}</strong>
        </p>
      ))}
    </div>
  );
};

// ─────────────────────────────────────────────────────────────
//  LOGIN
// ─────────────────────────────────────────────────────────────
function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  const handleSubmit = async () => {
    if (!username || !password) { setError("Completa todos los campos."); return; }
    setLoading(true);
    setError("");
    try {
      const { data } = await axios.post(`${API}/token/`, { username, password });
      onLogin(data.access);
    } catch {
      setError("Credenciales incorrectas. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => { if (e.key === "Enter") handleSubmit(); };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <div className="login-logo">
          <div className="login-logo-icon"><FiActivity /></div>
          <span className="login-brand">Health<span>care</span> Analytics</span>
        </div>
        <h1 className="login-title">Iniciar sesión</h1>
        <p className="login-subtitle">Accede al panel de analítica clínica</p>

        <div className="login-field">
          <label className="login-label">Usuario</label>
          <input
            className="login-input"
            type="text"
            placeholder="Tu usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={handleKey}
            autoComplete="username"
          />
        </div>

        <div className="login-field">
          <label className="login-label">Contraseña</label>
          <input
            className="login-input"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKey}
            autoComplete="current-password"
          />
        </div>

        <button className="login-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Ingresando..." : "Ingresar"}
        </button>

        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
//  KPI CARD
// ─────────────────────────────────────────────────────────────
function KPICard({ label, value, icon: Icon, color, loading }) {
  return (
    <div className={`kpi-card ${color}`}>
      <div className="kpi-icon"><Icon size={15} /></div>
      {loading
        ? <div className="skeleton" style={{ height: 22, width: "60%", borderRadius: 6 }} />
        : <div className="kpi-value">{value}</div>
      }
      <div className="kpi-label">{label}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
//  DASHBOARD
// ─────────────────────────────────────────────────────────────
function Dashboard({ onLogout }) {
  const [kpis, setKpis]           = useState(null);
  const [kpiLoading, setKpiLoading] = useState(true);
  const [kpiError, setKpiError]   = useState("");

  const [patients, setPatients]   = useState([]);
  const [patLoading, setPatLoading] = useState(true);
  const [patError, setPatError]   = useState("");

  const [search, setSearch]       = useState("");
  const [sortKey, setSortKey]     = useState("id");
  const [sortDir, setSortDir]     = useState("asc");
  const [page, setPage]           = useState(0);

  // ── Fetch KPIs ─────────────────────────────────────────────
  const fetchKpis = useCallback(async () => {
    setKpiLoading(true);
    setKpiError("");
    try {
      const token = localStorage.getItem("token");
      const { data } = await axios.get(`${API}/dashboard/kpis/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setKpis(data);
    } catch {
      setKpiError("No se pudieron cargar los KPIs.");
    } finally {
      setKpiLoading(false);
    }
  }, []);

  // ── Fetch Patients ─────────────────────────────────────────
  const fetchPatients = useCallback(async () => {
    setPatLoading(true);
    setPatError("");
    try {
      const token = localStorage.getItem("token");
      const { data } = await axios.get(`${API}/patients/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPatients(Array.isArray(data) ? data : data.results || []);
    } catch {
      setPatError("No se pudieron cargar los pacientes.");
    } finally {
      setPatLoading(false);
    }
  }, []);

  useEffect(() => { fetchKpis(); fetchPatients(); }, [fetchKpis, fetchPatients]);

  // ── Chart data ─────────────────────────────────────────────
  const chartData = useMemo(() => {
    if (!kpis) return [];
    return [
      { name: "Crítico", value: kpis.critical_patients },
      { name: "Alto",    value: kpis.high_risk },
      { name: "Medio",   value: kpis.medium_risk },
      { name: "Bajo",    value: kpis.low_risk },
    ];
  }, [kpis]);

  const totalRisk = chartData.reduce((s, d) => s + d.value, 0);

  // ── Table filtering / sorting / pagination ──────────────────
  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return patients
      .filter((p) =>
        !q ||
        p.nombres?.toLowerCase().includes(q) ||
        p.apellidos?.toLowerCase().includes(q) ||
        p.riesgo_calculado?.toLowerCase().includes(q) ||
        String(p.id).includes(q)
      )
      .sort((a, b) => {
        let va, vb;
        if (sortKey === "nombre") {
          va = `${a.nombres} ${a.apellidos}`.toLowerCase();
          vb = `${b.nombres} ${b.apellidos}`.toLowerCase();
        } else {
          va = a[sortKey];
          vb = b[sortKey];
        }
        if (va < vb) return sortDir === "asc" ? -1 : 1;
        if (va > vb) return sortDir === "asc" ? 1 : -1;
        return 0;
      });
  }, [patients, search, sortKey, sortDir]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage   = Math.min(page, totalPages - 1);
  const pageData   = filtered.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  const handleSort = (key) => {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(key); setSortDir("asc"); }
    setPage(0);
  };

  const sortArrow = (key) => (
    <span className={`sort-icon ${sortKey === key ? "active" : ""}`}>
      {sortKey === key ? (sortDir === "asc" ? "▲" : "▼") : "▲"}
    </span>
  );

  // ── Render ─────────────────────────────────────────────────
  return (
    <div className="dashboard-root">

      {/* ── HEADER ── */}
      <header className="header">
        <div className="header-logo">
          <div className="header-logo-icon"><FiActivity /></div>
          <span className="header-brand">Health<span>care</span> Analytics</span>
        </div>
        <div className="header-right">
          <span className="badge-live">En vivo</span>
          <button
            className="btn-logout"
            title="Recargar datos"
            onClick={() => { fetchKpis(); fetchPatients(); }}
            style={{ gap: 5 }}
          >
            <FiRefreshCw size={12} />
          </button>
          <button className="btn-logout" onClick={onLogout}>
            <FiLogOut size={12} /> Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">

        {/* ── KPI SECTION ── */}
        <section>
          <p className="section-label">Indicadores clave</p>
          {kpiError && <div className="error-box">{kpiError}</div>}
          <div className="kpi-grid">
            <KPICard label="Total Pacientes"    value={kpis?.total_patients?.toLocaleString()}      icon={FiUsers}        color="blue"   loading={kpiLoading} />
            <KPICard label="Pacientes Críticos" value={kpis?.critical_patients?.toLocaleString()}   icon={FiAlertTriangle} color="red"    loading={kpiLoading} />
            <KPICard label="Riesgo Alto"        value={kpis?.high_risk?.toLocaleString()}           icon={FiTrendingUp}   color="amber"  loading={kpiLoading} />
            <KPICard label="Riesgo Medio"       value={kpis?.medium_risk?.toLocaleString()}         icon={FiActivity}     color="cyan"   loading={kpiLoading} />
            <KPICard label="Riesgo Bajo"        value={kpis?.low_risk?.toLocaleString()}            icon={FiCheckCircle}  color="green"  loading={kpiLoading} />
            <KPICard label="Glucosa Promedio"   value={kpis ? `${kpis.average_glucose} mg/dL` : ""} icon={FiDroplet}      color="purple" loading={kpiLoading} />
            <KPICard label="IMC Promedio"       value={kpis ? `${kpis.average_bmi}` : ""}          icon={FiBarChart2}    color="teal"   loading={kpiLoading} />
          </div>
        </section>

        {/* ── CHARTS SECTION ── */}
        <section>
          <p className="section-label">Visualizaciones</p>
          <div className="charts-row">

            {/* Pie chart */}
            <div className="chart-card">
              <div className="chart-title green">Distribución de riesgo</div>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    innerRadius={45}
                    outerRadius={70}
                    paddingAngle={2}
                  >
                    {chartData.map((entry, i) => (
                      <Cell key={i} fill={RISK_COLORS[entry.name]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
              <div className="pie-legend">
                {chartData.map((d) => (
                  <div className="legend-item" key={d.name}>
                    <div className="legend-dot" style={{ background: RISK_COLORS[d.name] }} />
                    <span className="legend-name">{d.name}</span>
                    <span className="legend-pct">
                      {totalRisk > 0 ? ((d.value / totalRisk) * 100).toFixed(1) : 0}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Bar chart */}
            <div className="chart-card">
              <div className="chart-title blue">Pacientes por nivel de riesgo</div>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={chartData} barSize={32}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: "#8596b3", fontSize: 11, fontFamily: "'DM Sans'" }}
                    axisLine={{ stroke: "rgba(255,255,255,0.07)" }}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fill: "#8596b3", fontSize: 11, fontFamily: "'DM Sans'" }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
                  <Bar dataKey="value" name="Pacientes" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry, i) => (
                      <Cell key={i} fill={RISK_COLORS[entry.name]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Clinical indicators */}
            <div className="chart-card">
              <div className="chart-title cyan">Indicadores clínicos</div>
              <ResponsiveContainer width="100%" height={140}>
                <BarChart
                  data={[
                    { name: "Glucosa", value: kpis?.average_glucose || 0, fill: "#8b5cf6" },
                    { name: "IMC",     value: kpis?.average_bmi || 0,     fill: "#14b8a6" },
                  ]}
                  barSize={28}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" tick={{ fill: "#8596b3", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: "#8596b3", fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
                  <Bar dataKey="value" name="Valor" radius={[4, 4, 0, 0]}>
                    {[{ fill: "#8b5cf6" }, { fill: "#14b8a6" }].map((e, i) => (
                      <Cell key={i} fill={e.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="clinical-stats">
                <div className="clinical-stat">
                  <div className="clinical-stat-value">{kpis?.average_glucose ?? "—"}</div>
                  <div className="clinical-stat-label">Glucosa mg/dL</div>
                </div>
                <div className="clinical-stat">
                  <div className="clinical-stat-value">{kpis?.average_bmi ?? "—"}</div>
                  <div className="clinical-stat-label">IMC promedio</div>
                </div>
                <div className="clinical-stat">
                  <div className="clinical-stat-value">
                    {kpis && kpis.total_patients > 0
                      ? ((kpis.critical_patients / kpis.total_patients) * 100).toFixed(1) + "%"
                      : "—"}
                  </div>
                  <div className="clinical-stat-label">% Críticos</div>
                </div>
                <div className="clinical-stat">
                  <div className="clinical-stat-value">
                    {kpis && kpis.total_patients > 0
                      ? ((kpis.high_risk / kpis.total_patients) * 100).toFixed(1) + "%"
                      : "—"}
                  </div>
                  <div className="clinical-stat-label">% Riesgo alto</div>
                </div>
              </div>
            </div>

          </div>
        </section>

        {/* ── PATIENTS TABLE ── */}
        <section>
          <p className="section-label">Listado de pacientes</p>
          <div className="table-card">

            <div className="table-header">
              <div className="table-title">
                <FiHeart size={13} style={{ marginRight: 4, color: "#3b82f6" }} />
                Pacientes registrados
                {!patLoading && (
                  <span style={{ color: "#4a607e", fontWeight: 400, fontFamily: "'DM Sans'" }}>
                    &nbsp;({filtered.length})
                  </span>
                )}
              </div>
              <input
                className="table-search"
                type="text"
                placeholder="Buscar por nombre, riesgo o ID…"
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(0); }}
              />
            </div>

            {patError && <div className="error-box" style={{ margin: "12px 16px" }}>{patError}</div>}

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th className={sortKey === "id"     ? "sorted" : ""} onClick={() => handleSort("id")}>
                      ID {sortArrow("id")}
                    </th>
                    <th className={sortKey === "nombre" ? "sorted" : ""} onClick={() => handleSort("nombre")}>
                      Paciente {sortArrow("nombre")}
                    </th>
                    <th className={sortKey === "edad"   ? "sorted" : ""} onClick={() => handleSort("edad")}>
                      Edad {sortArrow("edad")}
                    </th>
                    <th>Sexo</th>
                    <th>Glucosa</th>
                    <th>IMC</th>
                    <th className={sortKey === "riesgo_calculado" ? "sorted" : ""} onClick={() => handleSort("riesgo_calculado")}>
                      Riesgo {sortArrow("riesgo_calculado")}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {patLoading ? (
                    <tr className="loading-row">
                      <td colSpan={7}>Cargando pacientes…</td>
                    </tr>
                  ) : pageData.length === 0 ? (
                    <tr className="empty-row">
                      <td colSpan={7}>No se encontraron pacientes.</td>
                    </tr>
                  ) : (
                    pageData.map((p) => (
                      <tr key={p.id}>
                        <td className="cell-id">#{String(p.id).padStart(4, "0")}</td>
                        <td className="cell-name">{p.nombres} {p.apellidos}</td>
                        <td>{p.edad} años</td>
                        <td>
                          <span className="badge-sex">
                            {p.sexo === "M" ? "Masc" : "Fem"}
                          </span>
                        </td>
                        <td>{p.glucosa ?? "—"}</td>
                        <td>{p.imc ?? "—"}</td>
                        <td>
                          <span className={RISK_BADGE[p.riesgo_calculado] || "badge"}>
                            {p.riesgo_calculado}
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {!patLoading && filtered.length > PAGE_SIZE && (
              <div className="pagination">
                <span className="pag-info">
                  {safePage * PAGE_SIZE + 1}–{Math.min((safePage + 1) * PAGE_SIZE, filtered.length)} de {filtered.length}
                </span>
                <div className="pag-btns">
                  <button className="pag-btn" disabled={safePage === 0} onClick={() => setPage(safePage - 1)}>‹</button>
                  {Array.from({ length: totalPages }, (_, i) => (
                    <button
                      key={i}
                      className={`pag-btn ${i === safePage ? "active" : ""}`}
                      onClick={() => setPage(i)}
                    >
                      {i + 1}
                    </button>
                  ))}
                  <button className="pag-btn" disabled={safePage >= totalPages - 1} onClick={() => setPage(safePage + 1)}>›</button>
                </div>
              </div>
            )}

          </div>
        </section>

      </main>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
//  APP ROOT
// ─────────────────────────────────────────────────────────────
export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  const handleLogin = (access) => {
    localStorage.setItem("token", access);
    setToken(access);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return token
    ? <Dashboard onLogout={handleLogout} />
    : <Login onLogin={handleLogin} />;
}