import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

function App() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [patients, setPatients] = useState([]);

  const [kpis, setKpis] = useState({
    total_patients: 0,
    critical_patients: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
    average_glucose: 0,
    average_bmi: 0
  });

  const [message, setMessage] = useState("");

  useEffect(() => {

    const token = localStorage.getItem("token");

    if (token) {

      setIsAuthenticated(true);

      fetchPatients(token);

      fetchKpis(token);

    }

  }, []);

  const handleLogin = async () => {

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/token/",
        {
          username,
          password
        }
      );

      const token = response.data.access;

      localStorage.setItem("token", token);

      setIsAuthenticated(true);

      fetchPatients(token);

      fetchKpis(token);

      setMessage("");

    } catch (error) {

      console.error(error);

      setMessage("Credenciales incorrectas");

    }

  };

  const fetchPatients = async (token) => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/patients/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setPatients(response.data);

    } catch (error) {

      console.error(error);

    }

  };

  const fetchKpis = async (token) => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/api/dashboard/kpis/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setKpis(response.data);

    } catch (error) {

      console.error(error);

    }

  };

  const handleLogout = () => {

    localStorage.removeItem("token");

    setPatients([]);

    setIsAuthenticated(false);

  };

  const chartData = [
    {
      name: "Crítico",
      value: kpis.critical_patients
    },
    {
      name: "Alto",
      value: kpis.high_risk
    },
    {
      name: "Medio",
      value: kpis.medium_risk
    },
    {
      name: "Bajo",
      value: kpis.low_risk
    }
  ];

  const COLORS = [
    "#dc2626",
    "#ea580c",
    "#eab308",
    "#16a34a"
  ];

  if (!isAuthenticated) {

    return (

      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "#f4f6f9"
        }}
      >

        <div
          style={{
            width: "400px",
            background: "white",
            padding: "30px",
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.1)"
          }}
        >

          <h2>Healthcare Login</h2>

          <input
            type="text"
            placeholder="Usuario"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px"
            }}
          />

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px"
            }}
          />

          <button
            onClick={handleLogin}
            style={{
              width: "100%",
              padding: "10px",
              cursor: "pointer"
            }}
          >
            Ingresar
          </button>

          <p>{message}</p>

        </div>

      </div>

    );

  }

  return (

    <div
      style={{
        padding: "30px",
        background: "#f4f6f9",
        minHeight: "100vh"
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "30px"
        }}
      >

        <h1>Healthcare Analytics Dashboard</h1>

        <button onClick={handleLogout}>
          Logout
        </button>

      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <div style={cardStyle}>
          <h3>Total Pacientes</h3>
          <h1>{kpis.total_patients}</h1>
        </div>

        <div style={cardStyle}>
          <h3>Pacientes Críticos</h3>
          <h1>{kpis.critical_patients}</h1>
        </div>

        <div style={cardStyle}>
          <h3>Glucosa Promedio</h3>
          <h1>{kpis.average_glucose}</h1>
        </div>

        <div style={cardStyle}>
          <h3>IMC Promedio</h3>
          <h1>{kpis.average_bmi}</h1>
        </div>

      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <div style={cardStyle}>

          <h2>Distribución de Riesgo</h2>

          <ResponsiveContainer width="100%" height={350}>

            <PieChart>

              <Pie
                data={chartData}
                dataKey="value"
                outerRadius={120}
                label
              >

                {chartData.map((entry, index) => (

                  <Cell
                    key={index}
                    fill={COLORS[index]}
                  />

                ))}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div style={cardStyle}>

          <h2>Pacientes por Riesgo</h2>

          <ResponsiveContainer width="100%" height={350}>

            <BarChart data={chartData}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="name" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="value" />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      <div style={cardStyle}>

        <h2>Últimos Pacientes</h2>

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse"
          }}
        >

          <thead>

            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Edad</th>
              <th>Riesgo</th>
            </tr>

          </thead>

          <tbody>

            {patients.slice(0, 15).map((patient) => (

              <tr key={patient.id}>

                <td>{patient.id}</td>
                <td>{patient.nombres}</td>
                <td>{patient.apellidos}</td>
                <td>{patient.edad}</td>
                <td>{patient.riesgo_calculado}</td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>

  );

}

const cardStyle = {
  background: "white",
  padding: "24px",
  borderRadius: "16px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.08)"
};

export default App;