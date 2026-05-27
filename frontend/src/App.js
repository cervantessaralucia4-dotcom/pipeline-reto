import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  // ======================
  // AUTH
  // ======================

  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [message, setMessage] = useState("");

  // ======================
  // DASHBOARD DATA
  // ======================

  const [patients, setPatients] = useState([]);

  // ======================
  // CHECK TOKEN
  // ======================

  useEffect(() => {

    const token = localStorage.getItem("token");

    if (token) {

      setIsAuthenticated(true);

      fetchPatients(token);

    }

  }, []);

  // ======================
  // LOGIN
  // ======================

  const handleLogin = async () => {

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/token/",
        {
          username,
          password
        }
      );

      const accessToken = response.data.access;

      localStorage.setItem(
        "token",
        accessToken
      );

      setIsAuthenticated(true);

      setMessage("Login exitoso");

      fetchPatients(accessToken);

    } catch (error) {

      console.error(error);

      setMessage("Credenciales incorrectas");

    }

  };

  // ======================
  // FETCH PATIENTS
  // ======================

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

  // ======================
  // LOGOUT
  // ======================

  const handleLogout = () => {

    localStorage.removeItem("token");

    setIsAuthenticated(false);

    setPatients([]);

  };

  // ======================
  // LOGIN SCREEN
  // ======================

  if (!isAuthenticated) {

    return (

      <div
        style={{
          minHeight: "100vh",
          background: "#f4f6f9",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontFamily: "Arial"
        }}
      >

        <div
          style={{
            background: "white",
            padding: "40px",
            borderRadius: "10px",
            width: "400px",
            boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
          }}
        >

          <h1 style={{ marginBottom: "20px" }}>
            Healthcare Login
          </h1>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px"
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "20px"
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
            Login
          </button>

          {
            message && (
              <p style={{ marginTop: "20px" }}>
                {message}
              </p>
            )
          }

        </div>

      </div>

    );

  }

  // ======================
  // DASHBOARD
  // ======================

  return (

    <div
      style={{
        padding: "30px",
        background: "#f4f6f9",
        minHeight: "100vh",
        fontFamily: "Arial"
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "30px"
        }}
      >

        <h1>
          Healthcare Dashboard
        </h1>

        <button
          onClick={handleLogout}
          style={{
            padding: "10px 20px",
            cursor: "pointer"
          }}
        >
          Logout
        </button>

      </div>

      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "10px"
        }}
      >

        <h2>
          Pacientes Registrados
        </h2>

        <h1>
          {patients.length}
        </h1>

      </div>

      <div
        style={{
          marginTop: "30px",
          background: "white",
          padding: "20px",
          borderRadius: "10px"
        }}
      >

        <h2>
          Lista de Pacientes
        </h2>

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse"
          }}
        >

          <thead>

            <tr style={{ background: "#ddd" }}>
              <th>ID</th>
              <th>Nombre</th>
              <th>Edad</th>
              <th>Riesgo</th>
            </tr>

          </thead>

          <tbody>

            {
              patients.slice(0, 10).map((patient) => (

                <tr key={patient.id}>

                  <td>{patient.id}</td>

                  <td>
                    {patient.nombres}
                  </td>

                  <td>{patient.edad}</td>

                  <td>
                    {patient.riesgo_calculado}
                  </td>

                </tr>

              ))
            }

          </tbody>

        </table>

      </div>

    </div>

  );
}

export default App;