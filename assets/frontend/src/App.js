import { HashRouter as Router, Route, Routes } from "react-router-dom";
import SideNav from "./components/SideNav";
import HomeScreen from "./screens/HomeScreen";

function App() {
  return (
    <div>
      <SideNav />
      <main className="main-content position-relative border-radius-lg ">
        <Router>
          <Routes>
            <Route path="/" element={<HomeScreen />} />
          </Routes>
        </Router>
      </main>
    </div>
  );
}

export default App;
